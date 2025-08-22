/**
 * Preload脚本
 *
 * 功能描述：
 * - 在渲染进程中暴露安全的API
 * - 提供剪贴板、窗口控制、文件对话框等功能
 * - 确保主进程和渲染进程之间的安全通信
 *
 * @author AI Assistant
 * @version 1.0.0
 */

const { contextBridge, ipcRenderer } = require('electron');

// 暴露安全的API给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  // 剪贴板API
  clipboard: {
    /**
     * 读取剪贴板中的图像
     *
     * @returns {Promise<Object|null>} 图像数据对象或null
     */
    readImage: () => ipcRenderer.invoke('clipboard:read-image'),
    
    /**
     * 清空剪贴板
     *
     * @returns {Promise<boolean>} 清空是否成功
     */
    clear: () => ipcRenderer.invoke('clipboard:clear')
  },

  // 窗口控制API
  minimizeWindow: () => ipcRenderer.invoke('window:minimize'),
  maximizeWindow: () => ipcRenderer.invoke('window:maximize'),
  closeWindow: () => ipcRenderer.invoke('window:close'),

  // 文件对话框API
  dialog: {
    /**
     * 显示保存文件对话框
     *
     * @param {Object} options - 对话框选项
     * @returns {Promise<Object>} 对话框结果
     */
    showSaveDialog: (options) => ipcRenderer.invoke('dialog:show-save-dialog', options)
  },

  // Python后端API
  python: {
    /**
     * 执行Python命令
     *
     * @param {string} command - 命令名称
     * @param {Object} options - 命令选项
     * @returns {Promise<Object>} 执行结果
     */
    execute: (command, options) => ipcRenderer.invoke('python:execute', command, options)
  },

  // 系统信息API
  platform: process.platform,
  version: process.versions.electron
});

// 开发环境下的调试信息
if (process.env.NODE_ENV === 'development') {
  console.log('🔧 Preload script loaded');
  console.log('Platform:', process.platform);
  console.log('Electron version:', process.versions.electron);
}
