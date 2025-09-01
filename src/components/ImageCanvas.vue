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
const currentImage = ref(null)
const imageSize = ref({ width: 0, height: 0 })

// 裁剪相关状态
const cropBox = ref(null) // 裁剪框 { x, y, width, height }
const isCropping = ref(false)
const cropStartPos = ref({ x: 0, y: 0 })
const cropResizeHandle = ref(null) // 当前调整的控制点
const cropHandles = ref([]) // 裁剪框控制点

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

// 监听工具变化
watch(() => props.currentTool, (newTool) => {
  if (newTool === 'crop') {
    initCropMode()
  } else {
    exitCropMode()
  }
})

// 监听工具选项变化
watch(() => props.toolOptions, (newOptions) => {
  if (props.currentTool === 'crop' && newOptions) {
    updateCropOptions(newOptions)
  }
}, { deep: true })

// 加载图像到画布
const loadImage = async (imageData) => {
  try {
    console.log('开始加载图像:', imageData)
    const img = new Image()
    img.onload = () => {
        console.log('图像加载成功:', img.width, 'x', img.height)
        
        // 保存当前图像引用和尺寸
        currentImage.value = img
        imageSize.value = { width: img.width, height: img.height }
        
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

      // 在图像加载后，如果处于裁剪模式且已有裁剪框，重新绘制覆盖层，确保缩放后覆盖层与主画布保持一致
      if (props.currentTool === 'crop' && cropBox.value) {
        drawCropOverlay()
      }
    }

    img.onerror = (error) => {
      console.error('图像加载失败:', error)
      message.error('图像加载失败')
    }

    // 设置图像源
    if (imageData.data.startsWith('data:')) {
      img.src = imageData.data
    } else if (imageData.data.startsWith('blob:')) {
      // 处理blob URL
      img.src = imageData.data
    } else {
      // 处理base64数据
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

/**
 * 按倍数调整缩放
 * @param {number} factor 缩放倍数，>1 放大，<1 缩小
 */
const adjustZoomBy = (factor) => {
  if (typeof factor !== 'number' || !isFinite(factor) || factor <= 0) return
  const next = zoomLevel.value * factor
  zoomLevel.value = Math.max(0.1, Math.min(5, next))
}

/**
 * 设置绝对缩放值
 * @param {number} value 目标缩放值，范围[0.1,5]
 */
const setZoom = (value) => {
  if (typeof value !== 'number' || !isFinite(value)) return
  zoomLevel.value = Math.max(0.1, Math.min(5, value))
}

// 裁剪相关方法
/**
 * 初始化裁剪模式
 * - 自由裁剪：初始裁剪框铺满整个图像
 * - 固定比例：以图像中心为基准创建默认框，并按所选比例调整
 */
const initCropMode = () => {
  if (!mainCanvas.value || !currentImage.value) {
    console.log('无法初始化裁剪模式：', {
      hasCanvas: !!mainCanvas.value,
      hasImage: !!currentImage.value
    })
    return
  }
  
  const imgWidth = currentImage.value.width
  const imgHeight = currentImage.value.height
  
  console.log('初始化裁剪模式，图像尺寸：', imgWidth, 'x', imgHeight)
  
  // 更新图像尺寸
  imageSize.value = { width: imgWidth, height: imgHeight }
  
  // 自由裁剪：初始铺满整图；固定比例：保留原有默认中心框
  const isFixedRatio = props.toolOptions?.cropMode === 'ratio' && props.toolOptions?.cropRatio !== 'free'
  if (!isFixedRatio) {
    // 自由裁剪：覆盖整张图像
    cropBox.value = {
      x: 0,
      y: 0,
      width: imgWidth,
      height: imgHeight
    }
  } else {
    const defaultSize = Math.min(imgWidth, imgHeight) * 0.6
    cropBox.value = {
      x: (imgWidth - defaultSize) / 2,
      y: (imgHeight - defaultSize) / 2,
      width: defaultSize,
      height: defaultSize
    }
    // 按比例调整一次
    applyCropRatio(props.toolOptions.cropRatio, props.toolOptions.customRatio)
  }
  
  console.log('创建裁剪框：', cropBox.value)
  drawCropOverlay()
}

/**
 * 退出裁剪模式
 */
const exitCropMode = () => {
  cropBox.value = null
  isCropping.value = false
  cropResizeHandle.value = null
  clearOverlay()
  // 重置光标样式
  if (canvasContainer.value) {
    canvasContainer.value.style.cursor = 'grab'
  }
}

/**
 * 更新裁剪选项
 * @param {Object} options 裁剪选项
 */
const updateCropOptions = (options) => {
  if (!cropBox.value || !options) return
  
  if (options.cropMode === 'ratio' && options.cropRatio !== 'free') {
    applyCropRatio(options.cropRatio, options.customRatio)
  }
}

/**
 * 应用裁剪比例
 * @param {string} ratio 比例字符串
 * @param {Object} customRatio 自定义比例
 */
const applyCropRatio = (ratio, customRatio) => {
  if (!cropBox.value) return
  
  let aspectRatio = 1
  
  if (ratio === 'custom' && customRatio) {
    aspectRatio = customRatio.width / customRatio.height
  } else {
    const ratioMap = {
      '1:1': 1,
      '4:3': 4/3,
      '16:9': 16/9,
      '3:2': 3/2
    }
    aspectRatio = ratioMap[ratio] || 1
  }
  
  // 保持裁剪框中心位置，调整尺寸以匹配比例
  const centerX = cropBox.value.x + cropBox.value.width / 2
  const centerY = cropBox.value.y + cropBox.value.height / 2
  
  let newWidth = cropBox.value.width
  let newHeight = cropBox.value.height
  
  if (newWidth / newHeight > aspectRatio) {
    newWidth = newHeight * aspectRatio
  } else {
    newHeight = newWidth / aspectRatio
  }
  
  cropBox.value = {
    x: centerX - newWidth / 2,
    y: centerY - newHeight / 2,
    width: newWidth,
    height: newHeight
  }
  
  drawCropOverlay()
}

/**
 * 绘制裁剪覆盖层
 */
const drawCropOverlay = () => {
  if (!overlayCanvas.value || !cropBox.value) {
    console.log('无法绘制裁剪覆盖层：', {
      hasOverlayCanvas: !!overlayCanvas.value,
      hasCropBox: !!cropBox.value
    })
    return
  }
  
  const canvas = overlayCanvas.value
  const ctx = canvas.getContext('2d')
  
  console.log('绘制裁剪覆盖层，画布尺寸：', canvas.width, 'x', canvas.height)
  console.log('裁剪框：', cropBox.value)
  
  // 清除画布
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  // 绘制遮罩
  ctx.fillStyle = 'rgba(0, 0, 0, 0.5)'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  
  // 清除裁剪区域
  ctx.globalCompositeOperation = 'destination-out'
  ctx.fillRect(cropBox.value.x, cropBox.value.y, cropBox.value.width, cropBox.value.height)
  
  // 绘制裁剪框边框
  ctx.globalCompositeOperation = 'source-over'
  ctx.strokeStyle = '#1890ff'
  ctx.lineWidth = 2
  ctx.strokeRect(cropBox.value.x, cropBox.value.y, cropBox.value.width, cropBox.value.height)
  
  // 绘制控制点
  drawCropHandles(ctx)
}

/**
 * 绘制裁剪框控制点
 * @param {CanvasRenderingContext2D} ctx 画布上下文
 */
const drawCropHandles = (ctx) => {
  if (!cropBox.value) return
  
  const { x, y, width, height } = cropBox.value
  const handleSize = 8
  
  const handles = [
    { x: x - handleSize/2, y: y - handleSize/2, type: 'nw' },
    { x: x + width/2 - handleSize/2, y: y - handleSize/2, type: 'n' },
    { x: x + width - handleSize/2, y: y - handleSize/2, type: 'ne' },
    { x: x + width - handleSize/2, y: y + height/2 - handleSize/2, type: 'e' },
    { x: x + width - handleSize/2, y: y + height - handleSize/2, type: 'se' },
    { x: x + width/2 - handleSize/2, y: y + height - handleSize/2, type: 's' },
    { x: x - handleSize/2, y: y + height - handleSize/2, type: 'sw' },
    { x: x - handleSize/2, y: y + height/2 - handleSize/2, type: 'w' }
  ]
  
  cropHandles.value = handles
  
  ctx.fillStyle = '#1890ff'
  ctx.strokeStyle = '#ffffff'
  ctx.lineWidth = 1
  
  handles.forEach(handle => {
    ctx.fillRect(handle.x, handle.y, handleSize, handleSize)
    ctx.strokeRect(handle.x, handle.y, handleSize, handleSize)
  })
}

/**
 * 清除覆盖层
 */
const clearOverlay = () => {
  if (!overlayCanvas.value) return
  const ctx = overlayCanvas.value.getContext('2d')
  ctx.clearRect(0, 0, overlayCanvas.value.width, overlayCanvas.value.height)
}

/**
 * 获取画布坐标
 * @param {MouseEvent} event 鼠标事件
 * @returns {Object} 画布坐标 {x, y}
 */
const getCanvasCoordinates = (event) => {
  if (!mainCanvas.value) return { x: 0, y: 0 }
  
  const canvas = mainCanvas.value
  const rect = canvas.getBoundingClientRect()
  const scaleX = canvas.width / rect.width
  const scaleY = canvas.height / rect.height
  
  return {
    x: (event.clientX - rect.left) * scaleX,
    y: (event.clientY - rect.top) * scaleY
  }
}

/**
 * 检查点击是否在裁剪框控制点上
 * @param {Object} pos 点击位置 {x, y}
 * @returns {Object|null} 控制点信息或null
 */
const getClickedHandle = (pos) => {
  if (!cropHandles.value.length) return null
  
  const handleSize = 8
  return cropHandles.value.find(handle => {
    return pos.x >= handle.x && pos.x <= handle.x + handleSize &&
           pos.y >= handle.y && pos.y <= handle.y + handleSize
  })
}

/**
 * 检查点击是否在裁剪框内
 * @param {Object} pos 点击位置 {x, y}
 * @returns {boolean} 是否在裁剪框内
 */
const isInsideCropBox = (pos) => {
  if (!cropBox.value) return false
  
  const { x, y, width, height } = cropBox.value
  return pos.x >= x && pos.x <= x + width && pos.y >= y && pos.y <= y + height
}

/**
 * 根据鼠标位置更新光标样式
 * @param {Object} pos 鼠标位置 {x, y}
 */
const updateCursor = (pos) => {
  if (!canvasContainer.value || !cropBox.value) return
  
  const clickedHandle = getClickedHandle(pos)
  
  if (clickedHandle) {
    // 根据控制点类型设置光标
    const cursorMap = {
      'nw': 'nw-resize',
      'n': 'n-resize',
      'ne': 'ne-resize',
      'e': 'e-resize',
      'se': 'se-resize',
      's': 's-resize',
      'sw': 'sw-resize',
      'w': 'w-resize'
    }
    canvasContainer.value.style.cursor = cursorMap[clickedHandle.type] || 'default'
  } else if (isInsideCropBox(pos)) {
    // 在裁剪框内部，显示移动光标
    canvasContainer.value.style.cursor = 'move'
  } else {
    // 默认光标
    canvasContainer.value.style.cursor = 'default'
  }
}

/**
 * 移动裁剪框
 * @param {Object} currentPos 当前鼠标位置
 */
const moveCropBox = (currentPos) => {
  if (!cropBox.value || !cropStartPos.value) return
  
  const newX = currentPos.x - cropStartPos.value.x
  const newY = currentPos.y - cropStartPos.value.y
  
  // 限制裁剪框在图像范围内
  const maxX = imageSize.value.width - cropBox.value.width
  const maxY = imageSize.value.height - cropBox.value.height
  
  cropBox.value.x = Math.max(0, Math.min(newX, maxX))
  cropBox.value.y = Math.max(0, Math.min(newY, maxY))
}

/**
 * 调整裁剪框大小
 * @param {Object} currentPos 当前鼠标位置
 */
const resizeCropBox = (currentPos) => {
  if (!cropBox.value || !cropStartPos.value || !cropResizeHandle.value) return
  
  const handle = cropResizeHandle.value.type
  const deltaX = currentPos.x - cropStartPos.value.x
  const deltaY = currentPos.y - cropStartPos.value.y
  
  let newX = cropBox.value.x
  let newY = cropBox.value.y
  let newWidth = cropBox.value.width
  let newHeight = cropBox.value.height
  
  // 根据控制点调整裁剪框
  switch (handle) {
    case 'nw': // 左上角
      newX += deltaX
      newY += deltaY
      newWidth -= deltaX
      newHeight -= deltaY
      break
    case 'n': // 上边
      newY += deltaY
      newHeight -= deltaY
      break
    case 'ne': // 右上角
      newY += deltaY
      newWidth += deltaX
      newHeight -= deltaY
      break
    case 'e': // 右边
      newWidth += deltaX
      break
    case 'se': // 右下角
      newWidth += deltaX
      newHeight += deltaY
      break
    case 's': // 下边
      newHeight += deltaY
      break
    case 'sw': // 左下角
      newX += deltaX
      newWidth -= deltaX
      newHeight += deltaY
      break
    case 'w': // 左边
      newX += deltaX
      newWidth -= deltaX
      break
  }
  
  // 如果是固定比例模式，保持宽高比
  if (props.toolOptions?.cropMode === 'ratio' && props.toolOptions?.cropRatio !== 'free') {
    let aspectRatio = 1
    
    if (props.toolOptions.cropRatio === 'custom' && props.toolOptions.customRatio) {
      aspectRatio = props.toolOptions.customRatio.width / props.toolOptions.customRatio.height
    } else {
      const ratioMap = {
        '1:1': 1,
        '4:3': 4/3,
        '16:9': 16/9,
        '3:2': 3/2
      }
      aspectRatio = ratioMap[props.toolOptions.cropRatio] || 1
    }
    
    // 根据宽度调整高度，或根据高度调整宽度
    if (['e', 'w', 'ne', 'nw', 'se', 'sw'].includes(handle)) {
      newHeight = newWidth / aspectRatio
    } else if (['n', 's'].includes(handle)) {
      newWidth = newHeight * aspectRatio
    }
  }
  
  // 确保最小尺寸
  const minSize = 20
  newWidth = Math.max(minSize, newWidth)
  newHeight = Math.max(minSize, newHeight)
  
  // 确保裁剪框不超出图像边界
  // 如果调整后的尺寸超出图像范围，则限制尺寸
  if (newX < 0) {
    newWidth += newX
    newX = 0
  }
  if (newY < 0) {
    newHeight += newY
    newY = 0
  }
  if (newX + newWidth > imageSize.value.width) {
    newWidth = imageSize.value.width - newX
  }
  if (newY + newHeight > imageSize.value.height) {
    newHeight = imageSize.value.height - newY
  }
  
  // 再次确保最小尺寸（防止边界限制后尺寸过小）
  newWidth = Math.max(minSize, newWidth)
  newHeight = Math.max(minSize, newHeight)
  
  // 最终位置限制
  newX = Math.max(0, Math.min(newX, imageSize.value.width - newWidth))
  newY = Math.max(0, Math.min(newY, imageSize.value.height - newHeight))
  
  // 更新裁剪框
  cropBox.value = {
    x: newX,
    y: newY,
    width: newWidth,
    height: newHeight
  }
  
  // 更新起始位置
  cropStartPos.value = currentPos
}

// 鼠标事件处理
const handleWheel = (event) => {
  event.preventDefault()
  
  // 获取鼠标在画布上的位置（用于缩放时保持鼠标位置不变）
  const rect = mainCanvas.value.getBoundingClientRect()
  const mouseX = event.clientX - rect.left
  const mouseY = event.clientY - rect.top
  
  // 交换默认行为：默认滚轮缩放，按住Shift键时平移
  if (event.shiftKey) {
    // Shift + 滚轮平移
    panOffset.value.x -= event.deltaX * 0.5
    panOffset.value.y -= event.deltaY * 0.5
  } else {
    // 默认滚轮缩放
    const delta = event.deltaY > 0 ? 0.9 : 1.1
    const oldZoom = zoomLevel.value
    const newZoom = Math.max(0.1, Math.min(5, zoomLevel.value * delta))
    
    // 计算缩放前后的鼠标位置差异，调整平移偏移以保持鼠标位置不变
    // 这样缩放会以鼠标位置为中心点
    if (mainCanvas.value) {
      const canvasWidth = mainCanvas.value.width
      const canvasHeight = mainCanvas.value.height
      
      // 计算鼠标在画布坐标系中的相对位置（0-1范围）
      const relativeX = mouseX / rect.width
      const relativeY = mouseY / rect.height
      
      // 调整平移偏移，使缩放以鼠标位置为中心
      panOffset.value.x -= (newZoom - oldZoom) * canvasWidth * relativeX / oldZoom
      panOffset.value.y -= (newZoom - oldZoom) * canvasHeight * relativeY / oldZoom
    }
    
    zoomLevel.value = newZoom
    
    // 如果处于裁剪模式且有裁剪框，重新绘制覆盖层以适应新的缩放级别
    if (props.currentTool === 'crop' && cropBox.value) {
      drawCropOverlay()
    }
  }
}

const handleMouseDown = (event) => {
  // 裁剪模式下的鼠标处理
  if (props.currentTool === 'crop' && cropBox.value) {
    const canvasPos = getCanvasCoordinates(event)
    const clickedHandle = getClickedHandle(canvasPos)
    
    if (clickedHandle) {
      // 点击了控制点，开始调整大小
      cropResizeHandle.value = clickedHandle
      isCropping.value = true
      cropStartPos.value = canvasPos
      event.preventDefault()
      return
    } else if (isInsideCropBox(canvasPos)) {
      // 点击了裁剪框内部，开始移动
      isCropping.value = true
      cropStartPos.value = {
        x: canvasPos.x - cropBox.value.x,
        y: canvasPos.y - cropBox.value.y
      }
      event.preventDefault()
      return
    }
  }
  
  if (event.button === 1 || (event.button === 0 && event.ctrlKey)) {
    // 中键或Ctrl+左键拖拽
    isDragging.value = true
    lastMousePos.value = { x: event.clientX, y: event.clientY }
    event.preventDefault()
  }
}

const handleMouseMove = (event) => {
  // 裁剪模式下的鼠标移动处理
  if (props.currentTool === 'crop' && cropBox.value) {
    const canvasPos = getCanvasCoordinates(event)
    
    if (isCropping.value) {
      if (cropResizeHandle.value) {
        // 调整裁剪框大小
        resizeCropBox(canvasPos)
      } else {
        // 移动裁剪框
        moveCropBox(canvasPos)
      }
      drawCropOverlay()
    } else {
      // 更新光标样式
      updateCursor(canvasPos)
    }
    return
  }
  
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
  isCropping.value = false
  cropResizeHandle.value = null
}

const handleMouseLeave = () => {
  isDragging.value = false
  isCropping.value = false
  cropResizeHandle.value = null
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

// 应用裁剪
const applyCrop = () => {
  if (!cropBox.value || !mainCanvas.value) {
    console.warn('No crop box or canvas available')
    return null
  }
  
  const canvas = mainCanvas.value
  const ctx = canvas.getContext('2d')
  
  // 保存当前裁剪框信息用于后续调整
  const originalCropBox = { ...cropBox.value }
  const originalImageSize = { ...imageSize.value }
  
  // 创建新的canvas来存储裁剪结果
  const croppedCanvas = document.createElement('canvas')
  const croppedCtx = croppedCanvas.getContext('2d')
  
  // 设置裁剪后的canvas尺寸
  croppedCanvas.width = cropBox.value.width
  croppedCanvas.height = cropBox.value.height
  
  // 从原canvas中复制裁剪区域
  croppedCtx.drawImage(
    canvas,
    cropBox.value.x, cropBox.value.y, cropBox.value.width, cropBox.value.height,
    0, 0, cropBox.value.width, cropBox.value.height
  )
  
  // 将裁剪结果转换为blob
  return new Promise((resolve) => {
    croppedCanvas.toBlob((blob) => {
      // 裁剪完成后，调整裁剪框以适应新的图像尺寸
      setTimeout(() => {
        adjustCropBoxAfterCrop(originalCropBox, originalImageSize)
      }, 100) // 延迟执行，确保新图像已加载
      
      resolve(blob)
    }, 'image/png')
  })
}

/**
 * 裁剪后调整裁剪框位置和大小
 * @param {Object} originalCropBox 原始裁剪框
 * @param {Object} originalImageSize 原始图像尺寸
 */
const adjustCropBoxAfterCrop = (originalCropBox, originalImageSize) => {
  if (!currentImage.value || !props.currentTool === 'crop') return
  
  // 新图像尺寸就是裁剪框的尺寸
  const newImageSize = {
    width: originalCropBox.width,
    height: originalCropBox.height
  }
  
  // 更新图像尺寸（立即同步本地状态，后续 loadImage 仍会以真实图像尺寸覆盖一次）
  imageSize.value = newImageSize
  
  // 裁剪后将裁剪框设置为覆盖新图像的全部区域
  // 这样无论界面如何缩放（fitToWindow/手动缩放），裁剪框形状都会随图像等比例缩放
  cropBox.value = {
    x: 0,
    y: 0,
    width: newImageSize.width,
    height: newImageSize.height
  }
  
  // 重新绘制裁剪覆盖层
  drawCropOverlay()
}

// 向父组件暴露方法
defineExpose({
  adjustZoomBy,
  setZoom,
  fitToWindow,
  applyCrop
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
