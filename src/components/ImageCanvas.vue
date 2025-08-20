<template>
  <div class="image-canvas-container">
    <!-- 空状态 -->
    <div v-if="!imageData" class="empty-state">
      <div class="empty-content">
        <Copy24Regular class="empty-icon" />
        <h3>等待剪贴板图像</h3>
        <p>复制图像到剪贴板，或按 Ctrl+V 粘贴图像</p>
        <a-button type="primary" @click="handlePasteClick">
          <template #icon><ClipboardPaste24Regular class="button-icon" /></template>
          粘贴图像
        </a-button>
      </div>
    </div>

    <!-- 图像编辑区域 -->
    <div v-else class="canvas-area">
      <!-- 工具栏 -->
      <div class="canvas-toolbar">
        <div class="toolbar-left">
          <a-space>
            <span class="image-info">
              {{ imageInfo.width }} × {{ imageInfo.height }} px
            </span>
            <span class="image-size">
              {{ formatFileSize(imageInfo.size) }}
            </span>
            <span class="image-format">
              {{ imageInfo.format.toUpperCase() }}
            </span>
          </a-space>
        </div>
        
        <div class="toolbar-right">
          <a-space>
            <a-button size="small" @click="zoomOut">
              <template #icon><ZoomOut24Regular class="button-icon" /></template>
            </a-button>
            <span class="zoom-level">{{ Math.round(zoomLevel * 100) }}%</span>
            <a-button size="small" @click="zoomIn">
              <template #icon><ZoomIn24Regular class="button-icon" /></template>
            </a-button>
            <a-button size="small" @click="resetZoom">
              <template #icon><FullScreenMaximize24Regular class="button-icon" /></template>
              适合窗口
            </a-button>
          </a-space>
        </div>
      </div>

      <!-- 画布容器 -->
      <div 
        ref="canvasContainer" 
        class="canvas-container"
        @wheel="handleWheel"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
        @mouseleave="handleMouseLeave"
      >
        <!-- 主画布 -->
        <canvas
          ref="mainCanvas"
          class="main-canvas"
          :style="canvasStyle"
        ></canvas>
        
        <!-- 覆盖层画布（用于绘制工具预览） -->
        <canvas
          ref="overlayCanvas"
          class="overlay-canvas"
          :style="canvasStyle"
        ></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { message } from 'ant-design-vue'
import {
  Copy24Regular,
  ClipboardPaste24Regular,
  ZoomIn24Regular,
  ZoomOut24Regular,
  FullScreenMaximize24Regular
} from '@vicons/fluent'

// Props
const props = defineProps({
  imageData: {
    type: Object,
    default: null
  },
  currentTool: {
    type: String,
    default: 'select'
  },
  toolOptions: {
    type: Object,
    default: () => ({})
  }
})

// Emits
const emit = defineEmits(['image-change'])

// 响应式数据
const canvasContainer = ref(null)
const mainCanvas = ref(null)
const overlayCanvas = ref(null)
const zoomLevel = ref(1)
const panOffset = ref({ x: 0, y: 0 })
const isDragging = ref(false)
const lastMousePos = ref({ x: 0, y: 0 })

// 图像信息
const imageInfo = computed(() => {
  if (!props.imageData) return {}
  
  return {
    width: props.imageData.width || 0,
    height: props.imageData.height || 0,
    size: props.imageData.size || 0,
    format: props.imageData.format || 'unknown'
  }
})

// 画布样式
const canvasStyle = computed(() => ({
  transform: `translate(-50%, -50%) scale(${zoomLevel.value})`,
  transformOrigin: 'center center'
}))

// 监听图像数据变化
watch(() => props.imageData, (newData) => {
  if (newData) {
    loadImage(newData)
  }
}, { immediate: true })

// 加载图像到画布
const loadImage = async (imageData) => {
  try {
    console.log('开始加载图像:', imageData)
    const img = new Image()
    img.onload = () => {
      console.log('图像加载成功:', img.width, 'x', img.height)
      const canvas = mainCanvas.value
      const ctx = canvas.getContext('2d')

      // 清除画布
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // 设置画布尺寸
      canvas.width = img.width
      canvas.height = img.height

      // 设置覆盖层画布尺寸
      const overlayCanvasEl = overlayCanvas.value
      overlayCanvasEl.width = img.width
      overlayCanvasEl.height = img.height

      // 绘制图像
      ctx.drawImage(img, 0, 0)
      console.log('图像已绘制到画布')

      // 检查Canvas内容
      const imageData = ctx.getImageData(0, 0, Math.min(10, img.width), Math.min(10, img.height))
      console.log('Canvas像素数据样本:', imageData.data.slice(0, 20))
      console.log('Canvas元素尺寸:', canvas.offsetWidth, 'x', canvas.offsetHeight)
      console.log('Canvas样式:', window.getComputedStyle(canvas).transform)

      // 自适应缩放
      nextTick(() => {
        fitToWindow()
        console.log('缩放级别:', zoomLevel.value)
      })
    }

    img.onerror = (error) => {
      console.error('图像加载失败:', error)
      message.error('图像加载失败')
    }

    // 设置图像源
    if (imageData.data.startsWith('data:')) {
      img.src = imageData.data
    } else {
      img.src = `data:image/${imageData.format};base64,${imageData.data}`
    }
    console.log('图像源已设置')
  } catch (error) {
    console.error('加载图像失败:', error)
    message.error('图像加载失败')
  }
}

// 缩放控制
const zoomIn = () => {
  zoomLevel.value = Math.min(zoomLevel.value * 1.2, 5)
}

const zoomOut = () => {
  zoomLevel.value = Math.max(zoomLevel.value / 1.2, 0.1)
}

const resetZoom = () => {
  zoomLevel.value = 1
  panOffset.value = { x: 0, y: 0 }
}

const fitToWindow = () => {
  if (!canvasContainer.value || !mainCanvas.value) return

  const container = canvasContainer.value
  const canvas = mainCanvas.value

  const containerWidth = container.clientWidth - 40
  const containerHeight = container.clientHeight - 80
  const canvasWidth = canvas.width
  const canvasHeight = canvas.height

  console.log('容器尺寸:', containerWidth, 'x', containerHeight)
  console.log('画布尺寸:', canvasWidth, 'x', canvasHeight)

  if (canvasWidth > 0 && canvasHeight > 0) {
    const scaleX = containerWidth / canvasWidth
    const scaleY = containerHeight / canvasHeight
    const scale = Math.min(scaleX, scaleY, 1)

    zoomLevel.value = scale
    panOffset.value = { x: 0, y: 0 }
    console.log('计算的缩放比例:', scale)
  }
}

// 鼠标事件处理
const handleWheel = (event) => {
  event.preventDefault()
  
  if (event.ctrlKey) {
    // Ctrl + 滚轮缩放
    const delta = event.deltaY > 0 ? 0.9 : 1.1
    zoomLevel.value = Math.max(0.1, Math.min(5, zoomLevel.value * delta))
  } else {
    // 滚轮平移
    panOffset.value.x -= event.deltaX * 0.5
    panOffset.value.y -= event.deltaY * 0.5
  }
}

const handleMouseDown = (event) => {
  if (event.button === 1 || (event.button === 0 && event.ctrlKey)) {
    // 中键或Ctrl+左键拖拽
    isDragging.value = true
    lastMousePos.value = { x: event.clientX, y: event.clientY }
    event.preventDefault()
  }
}

const handleMouseMove = (event) => {
  if (isDragging.value) {
    const deltaX = event.clientX - lastMousePos.value.x
    const deltaY = event.clientY - lastMousePos.value.y
    
    panOffset.value.x += deltaX
    panOffset.value.y += deltaY
    
    lastMousePos.value = { x: event.clientX, y: event.clientY }
  }
}

const handleMouseUp = () => {
  isDragging.value = false
}

const handleMouseLeave = () => {
  isDragging.value = false
}

// 粘贴按钮点击
const handlePasteClick = async () => {
  try {
    if (window.electronAPI && window.electronAPI.clipboard) {
      const clipboardData = await window.electronAPI.clipboard.readImage()
      if (clipboardData) {
        emit('image-change', clipboardData)
        message.success('图像粘贴成功')
      } else {
        message.info('剪贴板中没有图像数据')
      }
    } else {
      message.error('无法访问剪贴板API')
    }
  } catch (error) {
    message.error('粘贴失败: ' + error.message)
  }
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 组件挂载
onMounted(() => {
  // 监听窗口大小变化
  window.addEventListener('resize', fitToWindow)
})
</script>

<style scoped>
.image-canvas-container {
  height: 100%;
  background: #fafafa;
  position: relative;
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-content {
  text-align: center;
  color: #8c8c8c;
}

.empty-icon {
  width: 64px !important;
  height: 64px !important;
  font-size: 64px !important;
  margin-bottom: 16px;
  color: #d9d9d9;
}

.empty-content h3 {
  margin-bottom: 8px;
  color: #595959;
}

.empty-content p {
  margin-bottom: 24px;
}

.canvas-area {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.canvas-toolbar {
  height: 40px;
  background: #ffffff;
  border-bottom: 1px solid #e8e8e8;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.toolbar-left .image-info,
.toolbar-left .image-size,
.toolbar-left .image-format {
  font-size: 12px;
  color: #8c8c8c;
}

.zoom-level {
  font-size: 12px;
  color: #595959;
  min-width: 40px;
  text-align: center;
}

.canvas-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  cursor: grab;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}

/* 降级方案 */
@supports not (backdrop-filter: blur(5px)) {
  .canvas-container {
    background: rgba(255, 255, 255, 0.3);
  }
}

.canvas-container:active {
  cursor: grabbing;
}

.main-canvas {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-origin: center center;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: #ffffff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  z-index: 1;
}

.overlay-canvas {
  position: absolute;
  top: 50%;
  left: 50%;
  transform-origin: center center;
  z-index: 2;
}

.overlay-canvas {
  pointer-events: none;
  border: none;
  box-shadow: none;
  background: transparent !important;
}

/* 按钮图标样式 */
.button-icon {
  width: 14px !important;
  height: 14px !important;
  font-size: 14px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}
</style>
