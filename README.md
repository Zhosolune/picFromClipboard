# 剪贴板图像处理工具

基于Electron和Python的Windows桌面应用程序，实现剪贴板图像处理功能。

## 项目概述

这是一个现代化的桌面图像处理工具，专门用于处理剪贴板中的图像。应用程序采用前后端分离的架构设计，前端使用Electron + Vue 3 + Ant Design Vue构建用户界面，后端使用Python + Pillow处理图像操作。

## 技术栈

### 前端技术栈
- **Electron 37.3.1** - 跨平台桌面应用框架
- **Vue 3.5.18** - 渐进式JavaScript框架
- **Ant Design Vue 4.2.6** - 企业级UI组件库
- **Vite 5.4.19** - 现代化构建工具
- **@vicons/fluent** - Fluent设计风格图标库

### 后端技术栈
- **Python 3.12.11** - 编程语言
- **Pillow 10.0.0+** - Python图像处理库

## 核心功能

### 1. 剪贴板监控系统
- 实时监控剪贴板内容变化
- 自动检测图像数据（PNG、JPG、BMP、GIF等格式）
- 支持Ctrl+V快捷键手动触发

### 2. 图像预览与导入
- 高质量图像预览显示
- 图像缩放适配（支持鼠标滚轮缩放）
- 图像基本信息显示（尺寸、格式、文件大小）
- 支持拖拽平移查看

### 3. 图像编辑功能
- **裁剪工具**：自由选区裁剪和固定比例裁剪（1:1、4:3、16:9等）
- **旋转功能**：90°、180°、270°快速旋转和自定义角度旋转
- **翻转操作**：水平翻转和垂直翻转
- **文字标注**：支持添加文本，可调整字体、大小、颜色、位置
- **图形绘制**：支持添加矩形、圆形、直线、箭头等基本图形

### 4. 文件保存系统
- 支持多种输出格式（PNG、JPG、BMP、GIF）
- 自定义文件名和保存路径
- 图像质量和压缩选项设置
- 预估文件大小显示

### 5. 用户界面特性
- **现代化设计**：采用Ant Design设计语言
- **响应式布局**：适配不同窗口尺寸
- **无边框窗口**：自定义标题栏设计
- **实时预览**：所有操作提供实时预览
- **撤销重做**：支持Ctrl+Z/Ctrl+Y快捷键

## 项目结构

```
picFromClipboard/
├── src/                          # 前端源码
│   ├── components/               # Vue组件
│   │   ├── ImageCanvas.vue       # 图像画布组件
│   │   ├── PropertyPanel.vue     # 属性面板组件
│   │   ├── SavePanel.vue         # 保存面板组件
│   │   └── ToolBar.vue           # 工具栏组件
│   ├── views/                    # 视图组件
│   │   └── MainView.vue          # 主视图
│   ├── utils/                    # 工具函数
│   │   └── clipboard.js          # 剪贴板工具
│   ├── styles/                   # 样式文件
│   │   └── global.css            # 全局样式
│   ├── App.vue                   # 根组件
│   ├── main.js                   # 主进程入口
│   ├── preload.js                # 预加载脚本
│   └── renderer.js               # 渲染进程入口
├── python-backend/               # Python后端
│   ├── image_processor.py        # 图像处理核心模块
│   └── requirements.txt          # Python依赖
├── package.json                  # 项目配置
├── forge.config.js               # Electron Forge配置
├── vite.renderer.config.mjs      # Vite渲染进程配置
├── vite.main.config.mjs          # Vite主进程配置
├── vite.preload.config.mjs       # Vite预加载配置
└── README.md                     # 项目说明
```

## 开发环境搭建

### 前置要求
- Node.js 18.3+
- Python 3.12.11
- npm 或 yarn

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd picFromClipboard
   ```

2. **安装前端依赖**
   ```bash
   npm install
   ```

3. **安装Python依赖**
   ```bash
   cd python-backend
   pip install -r requirements.txt
   cd ..
   ```

4. **启动开发服务器**
   ```bash
   npm start
   ```

## 构建和打包

### 开发模式
```bash
npm start
```

### 构建应用
```bash
npm run make
```

### 打包发布
```bash
npm run publish
```

## 使用说明

1. **启动应用**：运行应用程序后，主窗口将显示等待剪贴板图像的界面

2. **导入图像**：
   - 复制任意图像到剪贴板，应用会自动检测并显示
   - 或者按Ctrl+V手动粘贴图像

3. **编辑图像**：
   - 使用左侧工具栏选择编辑工具
   - 在右侧属性面板调整工具参数
   - 在中央画布区域进行编辑操作

4. **保存图像**：
   - 在底部保存面板选择输出格式和质量
   - 设置文件名和保存路径
   - 点击保存按钮完成保存

## 快捷键

- `Ctrl + V` - 粘贴剪贴板图像
- `Ctrl + Z` - 撤销操作
- `Ctrl + Y` - 重做操作
- `Ctrl + 滚轮` - 缩放图像
- `中键拖拽` - 平移图像

## 开发计划

- [x] 项目基础架构搭建
- [/] 剪贴板监控系统实现
- [ ] 图像预览与导入功能
- [ ] Python图像处理后端开发
- [ ] 图像编辑功能实现
- [ ] 文件保存系统开发
- [ ] 用户界面设计与实现
- [ ] 交互体验优化
- [ ] 测试与性能优化

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

如有问题或建议，请通过以下方式联系：
- 邮箱：1564228136@qq.com
- 项目Issues：[GitHub Issues](https://github.com/your-repo/issues)

---

**注意**：本项目目前处于开发阶段，部分功能可能尚未完全实现。
