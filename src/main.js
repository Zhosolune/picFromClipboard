import { app, BrowserWindow, clipboard, ipcMain, dialog } from 'electron';
import { spawn } from 'child_process';
import path from 'node:path';
import started from 'electron-squirrel-startup';

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (started) {
  app.quit();
}

// 全局变量
let mainWindow = null;

const createWindow = () => {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 1024,
    height: 768,
    minWidth: 800,
    minHeight: 600,
    frame: false, // 无边框窗口，使用自定义标题栏
    titleBarStyle: 'hidden',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      enableRemoteModule: false,
      nodeIntegration: false,
    },
  });

  // and load the index.html of the app.
  if (MAIN_WINDOW_VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(MAIN_WINDOW_VITE_DEV_SERVER_URL);
  } else {
    mainWindow.loadFile(path.join(__dirname, `../renderer/${MAIN_WINDOW_VITE_NAME}/index.html`));
  }

  // 开发环境下打开开发者工具
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
};

// IPC 事件处理
ipcMain.handle('clipboard:read-image', async () => {
  try {
    const image = clipboard.readImage();
    if (image.isEmpty()) {
      return null;
    }

    const buffer = image.toPNG();
    const base64 = buffer.toString('base64');
    const size = image.getSize();

    return {
      data: `data:image/png;base64,${base64}`,
      width: size.width,
      height: size.height,
      size: buffer.length,
      format: 'png',
      timestamp: Date.now()
    };
  } catch (error) {
    console.error('读取剪贴板图像失败:', error);
    return null;
  }
});

// 窗口控制
ipcMain.handle('window:minimize', () => {
  if (mainWindow) {
    mainWindow.minimize();
  }
});

ipcMain.handle('window:maximize', () => {
  if (mainWindow) {
    if (mainWindow.isMaximized()) {
      mainWindow.unmaximize();
    } else {
      mainWindow.maximize();
    }
  }
});

ipcMain.handle('window:close', () => {
  if (mainWindow) {
    mainWindow.close();
  }
});

// 文件对话框
ipcMain.handle('dialog:show-save-dialog', async (event, options) => {
  try {
    const result = await dialog.showSaveDialog(mainWindow, options);
    return result;
  } catch (error) {
    console.error('显示保存对话框失败:', error);
    return { canceled: true };
  }
});

// Python后端调用
ipcMain.handle('python:execute', async (event, command, options = {}) => {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(__dirname, '../python-backend/image_processor.py');
    const args = [scriptPath, command];

    // 添加命令参数
    if (options.input) {
      args.push('--input', options.input);
    }
    if (options.output) {
      args.push('--output', options.output);
    }
    if (options.format) {
      args.push('--format', options.format);
    }
    if (options.quality) {
      args.push('--quality', options.quality.toString());
    }
    if (options.params) {
      args.push('--params', JSON.stringify(options.params));
    }

    console.log('执行Python命令:', args.join(' '));

    const pythonProcess = spawn('python', args);
    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(stdout);
          resolve(result);
        } catch (error) {
          reject(new Error(`解析Python输出失败: ${error.message}\n输出: ${stdout}`));
        }
      } else {
        reject(new Error(`Python进程退出，代码: ${code}\n错误: ${stderr}`));
      }
    });

    pythonProcess.on('error', (error) => {
      reject(new Error(`启动Python进程失败: ${error.message}`));
    });
  });
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow();

  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// 应用程序安全设置
app.on('web-contents-created', (event, contents) => {
  contents.on('new-window', (event, navigationUrl) => {
    event.preventDefault();
  });
});
