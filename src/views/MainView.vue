<template>
  <div class="main-layout">
    <!-- 顶部标题栏 -->
    <div class="title-bar">
      <div class="title-content">
        <h1>剪贴板图像处理工具</h1>
        <div class="title-actions">
          <a-button type="text" size="small" @click="minimizeWindow">
            <template #icon><Subtract24Regular class="title-icon" /></template>
          </a-button>
          <a-button type="text" size="small" @click="maximizeWindow">
            <template #icon><Maximize24Regular class="title-icon" /></template>
          </a-button>
          <a-button type="text" size="small" danger @click="closeWindow">
            <template #icon><Dismiss24Regular class="title-icon" /></template>
          </a-button>
        </div>
      </div>
    </div>

    <!-- 新增：全局Header（置于 title-bar 下方） -->
    <AppHeader
        :current-tool="currentTool"
        @theme-change="handleThemeChange"
        @tool-change="handleToolChange"
        @undo="handleUndo"
        @redo="handleRedo"
        @clear="handleClear"
        @save="handleSaveButtonClick"
      />

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 左侧工具栏 -->
      <div class="toolbar">
        <ToolBar 
          :current-tool="currentTool" 
          @tool-change="handleToolChange"
        />
      </div>

      <!-- 中央编辑区域 -->
      <div class="edit-area" ref="editAreaRef">
        <ImageCanvas 
          ref="imageCanvasRef"
          :image-data="imageData"
          :current-tool="currentTool"
          :tool-options="toolOptions"
          @image-change="handleImageChange"
        />
      </div>

      <!-- 右侧属性面板：挤压式展开，独立于编辑区域 -->
      <transition name="panel-expand" @before-enter="onPanelBeforeEnter" @after-enter="onPanelAfterEnter" @before-leave="onPanelBeforeLeave" @after-leave="onPanelAfterLeave">
        <div class="property-panel" v-show="propertyPanelVisible">
          <PropertyPanel
            :current-tool="currentTool"
            :tool-options="toolOptions"
            :image-data="imageData"
            :canvas-ref="imageCanvasRef"
            @options-change="handleOptionsChange"
            @image-change="handleImageChange"
            @clear="handleClear"
            @tool-change="handleToolChange"
          />
        </div>
      </transition>

      <!-- 覆盖式保存面板（限制在 main-content 内，不遮盖 Footer） -->
      <transition name="overlay-fade">
        <div class="save-panel-overlay" v-show="savePanelVisible">
          <div class="save-panel-backdrop" @click="savePanelVisible = false"></div>
          <div class="save-panel">
            <SavePanel 
              :image-data="imageData"
              @save="handleSave"
              @update:last-save-time="updateLastSaveTime"
              @update:estimated-size="updateEstimatedSize"
              @close="savePanelVisible = false"
            />
          </div>
        </div>
      </transition>
    </div>

    <!-- 新增：全局Footer -->
    <AppFooter :estimated-size="estimatedSize" :last-save-time="lastSaveTime" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { Subtract24Regular, Maximize24Regular, Dismiss24Regular } from '@vicons/fluent'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'
import ToolBar from '../components/ToolBar.vue'
import ImageCanvas from '../components/ImageCanvas.vue'
import PropertyPanel from '../components/PropertyPanel.vue'
import SavePanel from '../components/SavePanel.vue'
import { useClipboard } from '../utils/clipboard.js'
import { readClipboardImage, clearClipboard } from '../utils/clipboard.js'

// 响应式数据
const currentTool = ref('select')
const imageData = ref(null)
const toolOptions = ref({})
// 新增：保存面板可见性（常态下隐藏）
const savePanelVisible = ref(false)
// 新增：属性面板可见性（常态下隐藏）
const propertyPanelVisible = ref(false)
// 新增：属性面板展开状态（用于区分隐藏和折叠）
const propertyPanelExpanded = ref(false)

// 新增：用于维护可视宽度的ref
const imageCanvasRef = ref(null)
const editAreaRef = ref(null)
let prevEditAreaWidth = 0

// Footer状态数据
const lastSaveTime = ref(null)
const estimatedSize = ref('')

// 由header发起的主题变化
const handleThemeChange = (theme) => {
  // 这里可扩展：同步到Ant Design主题或全局样式
}

// 供SavePanel更新footer状态
const updateLastSaveTime = (time) => {
  lastSaveTime.value = time
}

const updateEstimatedSize = (size) => {
  estimatedSize.value = size
}

// 剪贴板监控
const { startMonitoring, stopMonitoring } = useClipboard()

// 工具切换处理
const handleToolChange = (tool) => {
  const previousTool = currentTool.value
  
  // 如果点击的是同一个工具按钮
  if (previousTool === tool) {
    // 切换属性面板的折叠/展开状态
    if (propertyPanelVisible.value) {
      propertyPanelVisible.value = false
      propertyPanelExpanded.value = false
    } else {
      propertyPanelVisible.value = true
      propertyPanelExpanded.value = true
    }
  } else {
    // 切换到不同的工具
    currentTool.value = tool
    
    // 如果当前属性面板为折叠状态，展开对应的属性面板
    if (!propertyPanelVisible.value) {
      propertyPanelVisible.value = true
      propertyPanelExpanded.value = true
    }
    // 如果当前属性面板为展开状态，直接切换到新工具对应的面板（保持展开）
    // propertyPanelVisible.value 保持 true，只是内容会根据 currentTool 变化
  }
}

// 工具选项变更处理
const handleOptionsChange = (options) => {
  toolOptions.value = { ...toolOptions.value, ...options }
}

// 图像变更处理
const handleImageChange = (newImageData) => {
  console.log('接收到图像变更事件:', newImageData)
  
  // 如果是裁剪工具发送的数据，需要转换格式
  if (newImageData && typeof newImageData === 'object' && newImageData.imageUrl && newImageData.blob) {
    console.log('处理裁剪工具发送的新图像数据:', newImageData)
    
    // 从blob创建新的URL，避免URL格式混乱
    const blobUrl = URL.createObjectURL(newImageData.blob)
    
    // 裁剪后的数据格式转换
    const convertedData = {
      data: blobUrl,
      width: 0, // 将通过图像加载获取
      height: 0, // 将通过图像加载获取
      size: newImageData.blob.size,
      format: 'png', // 裁剪后默认为PNG格式
      blob: newImageData.blob
    }
    
    // 获取图像尺寸
    const img = new Image()
    img.onload = () => {
      convertedData.width = img.width
      convertedData.height = img.height
      imageData.value = convertedData
      console.log('裁剪后图像数据已更新:', convertedData)
    }
    img.onerror = (error) => {
      console.error('裁剪后图像加载失败:', error)
    }
    img.src = blobUrl
  } else {
    // 普通图像数据直接赋值
    imageData.value = newImageData
  }
}

// 新增：属性面板过渡钩子，保持图像可视宽度
/**
 * 在属性面板展开/收起的过渡期间，保持图像可视宽度一致
 * 通过在过渡前记录编辑区域宽度，在过渡后根据宽度变化成比例调整缩放
 */
const onPanelBeforeEnter = () => {
  prevEditAreaWidth = editAreaRef.value ? editAreaRef.value.clientWidth : 0
}
const onPanelAfterEnter = () => {
  if (!editAreaRef.value || !imageCanvasRef.value) return
  const newWidth = editAreaRef.value.clientWidth
  if (prevEditAreaWidth > 0 && newWidth > 0) {
    const ratio = newWidth / prevEditAreaWidth
    // 容器变窄=>ratio<1 缩小图像；容器变宽=>ratio>1 放大图像
    imageCanvasRef.value.adjustZoomBy?.(ratio)
  }
}
const onPanelBeforeLeave = () => {
  prevEditAreaWidth = editAreaRef.value ? editAreaRef.value.clientWidth : 0
}
const onPanelAfterLeave = () => {
  if (!editAreaRef.value || !imageCanvasRef.value) return
  const newWidth = editAreaRef.value.clientWidth
  if (prevEditAreaWidth > 0 && newWidth > 0) {
    const ratio = newWidth / prevEditAreaWidth
    imageCanvasRef.value.adjustZoomBy?.(ratio)
  }
}

// 新增：Header 撤销事件处理
/**
 * 处理撤销操作
 * - 用于响应 AppHeader 发出的 undo 事件
 */
const handleUndo = () => {
  // TODO: 实现撤销功能
  message.info('撤销功能开发中...')
}

// 新增：Header 重做事件处理
/**
 * 处理重做操作
 * - 用于响应 AppHeader 发出的 redo 事件
 */
const handleRedo = () => {
  // TODO: 实现重做功能
  message.info('重做功能开发中...')
}

// 新增：Header 保存事件处理
/**
 * 处理保存按钮点击操作
 */
const handleSaveButtonClick = () => {
  if (imageData.value) {
    savePanelVisible.value = true
    message.success('打开保存面板')
  } else {
    message.warning('没有图像可保存')
  }
}

// 新增：Header 清空事件处理
/**
 * 清空当前图像并隐藏保存面板
 * - 用于响应 AppHeader 发出的 clear 事件
 */
const handleClear = () => {
  imageData.value = null
  savePanelVisible.value = false
  // 新增：清空时隐藏属性面板
  propertyPanelVisible.value = false
  propertyPanelExpanded.value = false
  message.success('已清空当前图像')
}

// 保存处理
/**
 * 处理保存逻辑
 */
const handleSave = async (saveOptions) => {
  try {
    if (!imageData.value) {
      message.warning('没有图像数据可保存')
      return
    }

    // 调用Python后端保存图像
    if (window.electronAPI && window.electronAPI.python) {
      const result = await window.electronAPI.python.execute('save', {
        input: imageData.value.data,
        output: saveOptions.fullPath,
        format: saveOptions.format.toUpperCase(),
        quality: saveOptions.quality
      })

      if (result.success) {
        message.success('图像保存成功')
        lastSaveTime.value = new Date()
      } else {
        message.error('保存失败: ' + (result.error || '未知错误'))
      }
    } else {
      message.error('无法访问Python后端')
    }
  } catch (error) {
    console.error('保存失败:', error)
    message.error('保存失败: ' + error.message)
  }
}

// 窗口控制
const minimizeWindow = () => {
  window.electronAPI?.minimizeWindow()
}

const maximizeWindow = () => {
  window.electronAPI?.maximizeWindow()
}

const closeWindow = () => {
  window.electronAPI?.closeWindow()
}

/**
 * 手动触发粘贴动作
 * 功能：
 * - 主动读取系统剪贴板中的图像数据
 * - 若存在图像，更新 imageData 并唤起保存面板
 * - 粘贴成功后清空剪贴板
 * 依赖：readClipboardImage(), clearClipboard()
 */
const handlePasteAction = async () => {
  try {
    const clipboardImage = await readClipboardImage()
    if (clipboardImage && clipboardImage.data) {
      imageData.value = clipboardImage
      // 移除：不再自动唤起保存面板和属性面板
      message.success('粘贴成功')
      
      // 粘贴成功后清空剪贴板，防止重复检测
      try {
        await clearClipboard()
        console.log('手动粘贴后剪贴板已清空')
      } catch (error) {
        console.error('清空剪贴板失败:', error)
      }
    } else {
      message.warning('剪贴板中没有图像')
    }
  } catch (error) {
    console.error('粘贴失败:', error)
    message.error('粘贴失败')
  }
}

// 组件挂载
onMounted(() => {
  // 启动剪贴板监控
  startMonitoring(async (clipboardImage) => {
    imageData.value = clipboardImage
    // 移除：不再自动唤起保存面板和属性面板
    message.success('检测到剪贴板图像')
    
    // 粘贴成功后清空剪贴板，防止重复检测
    try {
      await clearClipboard()
      console.log('剪贴板已清空')
    } catch (error) {
      console.error('清空剪贴板失败:', error)
    }
  })

  // 监听键盘事件
  document.addEventListener('keydown', handleKeyDown)
})

// 键盘事件处理
const handleKeyDown = (event) => {
  // Ctrl+V 粘贴
  if (event.ctrlKey && event.key === 'v') {
    event.preventDefault()
    handlePasteAction()
  }
  
  // Ctrl+Z 撤销
  if (event.ctrlKey && event.key === 'z') {
    event.preventDefault()
    // TODO: 实现撤销功能
  }
  
  // Ctrl+Y 重做
  if (event.ctrlKey && event.key === 'y') {
    event.preventDefault()
    // TODO: 实现重做功能
  }
}
</script>

<style scoped>
.main-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
}

.main-layout::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.title-bar {
  height: 40px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  -webkit-app-region: drag;
  position: relative;
  z-index: 10;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 降级方案 */
@supports not (backdrop-filter: blur(20px)) {
  .title-bar {
    background: rgba(255, 255, 255, 0.95);
  }
}

.title-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 6px 0 16px;
}

.title-content h1 {
  font-size: 14px;
  font-weight: 500;
  color: #262626;
  margin: 0;
}

.title-actions {
  display: flex;
  gap: 6px;
  -webkit-app-region: no-drag;
}

.title-actions .ant-btn {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  color: #666;
  transition: background-color 0.2s ease, color 0.2s ease;
  padding: 2px;
  min-width: 30px;
  height: 30px;
  box-sizing: border-box;
}

.title-actions .ant-btn:hover {
  background-color: rgba(0, 0, 0, 0.08) !important;
  color: #333;
}

.title-actions .ant-btn:active {
  background-color: rgba(0, 0, 0, 0.12) !important;
}

.title-actions .ant-btn-dangerous {
  color: #ff4d4f;
}

.title-actions .ant-btn-dangerous:hover {
  background-color: rgba(255, 77, 79, 0.12) !important;
  color: #ff4d4f;
}

.title-actions .ant-btn-dangerous:active {
  background-color: rgba(255, 77, 79, 0.2) !important;
}

/* 暗色主题适配 */
@media (prefers-color-scheme: dark) {
  .title-content h1 {
    color: #e8e8e8;
  }

  .title-actions .ant-btn {
    color: #bbb;
  }

  .title-actions .ant-btn:hover {
    background-color: rgba(255, 255, 255, 0.08) !important;
    color: #fff;
  }

  .title-actions .ant-btn:active {
    background-color: rgba(255, 255, 255, 0.12) !important;
  }

  .title-actions .ant-btn-dangerous {
    color: #ff7875;
  }

  .title-actions .ant-btn-dangerous:hover {
    background-color: rgba(255, 120, 117, 0.12) !important;
    color: #ff7875;
  }

  .title-actions .ant-btn-dangerous:active {
    background-color: rgba(255, 120, 117, 0.2) !important;
  }
}

.main-content {
  flex: 1;
  display: flex;
  min-height: 0;
  position: relative;
  z-index: 1;
  overflow: clip;  /* 避免产生滚动条但不阻断子层滚动 */
}

.save-panel-overlay {
  pointer-events: none; /* 默认不拦截事件，避免影响画布滚动等 */
}
.save-panel-backdrop,
.save-panel {
  pointer-events: auto; /* 背景和面板本身可交互 */
}
.toolbar {
  width: 72px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-right: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  z-index: 5;
  box-shadow: 1px 0 3px rgba(0, 0, 0, 0.1);
}

/* 降级方案 */
@supports not (backdrop-filter: blur(15px)) {
  .toolbar {
    background: rgba(255, 255, 255, 0.9);
  }
}

/* 删除 content-wrapper 相关样式，改为主内容下直接两列布局 */

.edit-area {
  flex: 1;
  min-width: 0;
  transition: all 0.3s ease; /* 为挤压效果添加过渡 */
}

.property-panel {
  width: 300px;
  height: 100%; /* 撑满剩余高度 */
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-left: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  z-index: 5;
  box-shadow: -1px 0 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

/* 降级方案 */
@supports not (backdrop-filter: blur(15px)) {
  .property-panel {
    background: rgba(255, 255, 255, 0.9);
  }
}

/* 覆盖式保存面板样式 */
.save-panel-overlay {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0; /* 覆盖主内容区域（不遮盖Footer） */
  z-index: 20;
  display: flex;               /* 作为弹性容器 */
  flex-direction: column;      /* 纵向排列 */
  justify-content: flex-end;   /* 子元素靠底对齐 */
}
.save-panel-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.2);
  z-index: 0; /* 背景层在下 */
}
.save-panel {
  position: relative;          /* 使用相对定位，避免绝对定位的高度计算陷阱 */
  width: 100%;                 /* 占满宽度 */
  min-height: 150px;           /* 常态基线高度 */
  max-height: 100%;            /* 不超过可视容器高度 */
  overflow-y: auto;            /* 内容超出时内部滚动 */
  -webkit-overflow-scrolling: touch;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  z-index: 1;                  /* 高于背景层 */
  box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.1);
}

/* 覆盖式过渡动画 */
.overlay-fade-enter-active, .overlay-fade-leave-active {
  transition: opacity 0.2s ease;
}
.overlay-fade-enter-from, .overlay-fade-leave-to {
  opacity: 0;
}
.overlay-fade-enter-to, .overlay-fade-leave-from {
  opacity: 1;
}

/* 属性面板挤压式过渡动画 */
.panel-expand-enter-active,
.panel-expand-leave-active {
  transition: width 0.3s ease;
  overflow: hidden;
}

.panel-expand-enter-from,
.panel-expand-leave-to {
  width: 0;
}

.panel-expand-enter-to,
.panel-expand-leave-from {
  width: 300px;
}

/* 图标样式优化 */
.title-icon {
  width: 12px !important;
  height: 12px !important;
  font-size: 12px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

/* 响应式布局优化 */
@media (max-width: 1000px) {
  .property-panel {
    width: 250px;
  }

  /* 移除 .save-panel 的 max-height 限制，保持与桌面一致的自适应策略 */
}

@media (max-width: 800px) {
  .main-content {
    flex-direction: column;
  }

  .property-panel {
    width: 100%;
    height: auto;
    max-height: 200px;
    overflow-y: auto;
  }

  /* 移除 .save-panel 的 max-height 限制，保持与桌面一致的自适应策略 */
}
</style>
