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
    <AppHeader @theme-change="handleThemeChange" />

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
      <div class="edit-area">
        <ImageCanvas 
          :image-data="imageData"
          :current-tool="currentTool"
          :tool-options="toolOptions"
          @image-change="handleImageChange"
        />
      </div>

      <!-- 右侧属性面板 -->
      <div class="property-panel">
        <PropertyPanel
          :current-tool="currentTool"
          :tool-options="toolOptions"
          :image-data="imageData"
          @options-change="handleOptionsChange"
          @image-change="handleImageChange"
        />
      </div>
    </div>

    <!-- 底部保存面板 -->
    <div class="save-panel">
      <SavePanel 
        :image-data="imageData"
        @save="handleSave"
        @update:last-save-time="updateLastSaveTime"
        @update:estimated-size="updateEstimatedSize"
      />
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

// 响应式数据
const currentTool = ref('select')
const imageData = ref(null)
const toolOptions = ref({})

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
  currentTool.value = tool
}

// 工具选项变更处理
const handleOptionsChange = (options) => {
  toolOptions.value = { ...toolOptions.value, ...options }
}

// 图像变更处理
const handleImageChange = (newImageData) => {
  imageData.value = newImageData
}

// 保存处理
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

// 组件挂载
onMounted(() => {
  // 启动剪贴板监控
  startMonitoring((clipboardImage) => {
    imageData.value = clipboardImage
    message.success('检测到剪贴板图像')
  })

  // 监听键盘事件
  document.addEventListener('keydown', handleKeyDown)
})

// 键盘事件处理
const handleKeyDown = (event) => {
  // Ctrl+V 粘贴
  if (event.ctrlKey && event.key === 'v') {
    event.preventDefault()
    // TODO: 手动触发剪贴板检查
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

.edit-area {
  flex: 1;
  min-width: 0;
}

.property-panel {
  width: 300px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border-left: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  z-index: 5;
  box-shadow: -1px 0 3px rgba(0, 0, 0, 0.1);
}

/* 降级方案 */
@supports not (backdrop-filter: blur(15px)) {
  .property-panel {
    background: rgba(255, 255, 255, 0.9);
  }
}

.save-panel {
  min-height: 70px;
  flex-shrink: 0;
  max-height: 150px;
  overflow-y: auto;
  width: 100%;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  z-index: 10;
  box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.1);
  margin: 0;
  padding: 0;
}

/* 降级方案 */
@supports not (backdrop-filter: blur(20px)) {
  .save-panel {
    background: rgba(255, 255, 255, 0.95);
  }
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

  .save-panel {
    max-height: 250px;
  }
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

  .save-panel {
    max-height: 300px;
  }
}
</style>
