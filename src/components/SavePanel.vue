<template>
  <div class="save-panel">
    <div class="save-content">
      <!-- 关闭按钮 -->
      <a-button
        type="text"
        size="small"
        @click="handleClose"
        class="close-btn"
        title="关闭"
        aria-label="关闭"
      >
        <template #icon>
          <Dismiss24Regular class="close-icon" />
        </template>
      </a-button>
      <!-- 第一行：文件名 + 保存路径 + 浏览按钮 -->
      <div class="save-row first-row">
        <div class="input-group">
          <label class="input-label">重命名:</label>
          <a-input
            v-model:value="fileName"
            placeholder="输入文件名"
            class="filename-input"
            @blur="validateFileName"
          />
          <span class="file-extension">.{{ outputFormat }}</span>
        </div>

        <div class="input-group path-group">
          <label class="input-label">保存路径:</label>
          <a-input
            v-model:value="savePath"
            placeholder="选择保存路径"
            class="path-input"
          />
        </div>

        <a-button
          @click="selectSavePath"
          class="browse-btn"
          size="default"
        >
          浏览
        </a-button>
      </div>

      <!-- 第二行：选择格式 + 保存按钮 -->
      <div class="save-row second-row">
        <div class="format-group">
          <span class="format-label">选择格式:</span>
          <a-select
            v-model:value="outputFormat"
            class="format-select"
            @change="handleFormatChange"
          >
            <a-select-option value="png">PNG</a-select-option>
            <a-select-option value="jpg">JPG</a-select-option>
            <a-select-option value="bmp">BMP</a-select-option>
            <a-select-option value="gif">GIF</a-select-option>
          </a-select>
        </div>

        <a-button
          type="primary"
          :loading="saving"
          :disabled="!canSave"
          @click="handleSave"
          class="save-button"
          size="default"
        >
          保存
        </a-button>
      </div>

      <!-- 质量设置（仅JPG格式时显示） -->
      <div v-if="outputFormat === 'jpg'" class="quality-row">
        <label class="quality-label">图像质量:</label>
        <a-slider
          v-model:value="quality"
          :min="10"
          :max="100"
          :step="10"
          :marks="{ 10: '10%', 50: '50%', 80: '80%', 100: '100%' }"
          class="quality-slider"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { message } from 'ant-design-vue'
import {
  FolderOpen24Regular,
  Save24Regular,
  ShareAndroid24Regular,
  Image24Regular,
  Clock24Regular,
  Dismiss24Regular
} from '@vicons/fluent'

// Props
const props = defineProps({
  imageData: {
    type: Object,
    default: null
  }
})

// Emits - 添加状态更新事件
const emit = defineEmits(['save', 'update:last-save-time', 'update:estimated-size', 'close'])

// 响应式数据
const outputFormat = ref('png')
const quality = ref(80)
const fileName = ref('')
const savePath = ref('')
const saving = ref(false)
const lastSaveTime = ref(null)

// 计算属性
const canSave = computed(() => {
  return props.imageData && fileName.value.trim() && savePath.value
})

// 监听图像数据变化，自动生成文件名
watch(() => props.imageData, (newData) => {
  if (newData && !fileName.value) {
    generateFileName()
  }
  // 更新预估大小到父组件
  updateEstimatedSize()
}, { immediate: true })

// 监听格式和质量变化，更新预估大小
watch([outputFormat, quality], () => {
  updateEstimatedSize()
})

// 生成默认文件名
const generateFileName = () => {
  const now = new Date()
  const timestamp = now.toISOString().replace(/[:.]/g, '-').slice(0, -5)
  fileName.value = `clipboard-image-${timestamp}`
}

// 格式变更处理
const handleFormatChange = (format) => {
  outputFormat.value = format
  
  // JPG格式默认质量80%，其他格式不需要质量设置
  if (format === 'jpg' && quality.value === 100) {
    quality.value = 80
  }
}

// 验证文件名
const validateFileName = () => {
  const invalidChars = /[<>:"/\\|?*]/g
  if (invalidChars.test(fileName.value)) {
    fileName.value = fileName.value.replace(invalidChars, '')
    message.warning('文件名包含非法字符，已自动移除')
  }
  
  if (!fileName.value.trim()) {
    generateFileName()
  }
}

// 选择保存路径
const selectSavePath = async () => {
  try {
    if (window.electronAPI && window.electronAPI.dialog) {
      const result = await window.electronAPI.dialog.showSaveDialog({
        title: '选择保存路径',
        defaultPath: fileName.value + '.' + outputFormat.value,
        filters: [
          { name: '图像文件', extensions: [outputFormat.value] },
          { name: '所有文件', extensions: ['*'] }
        ]
      })
      
      if (!result.canceled && result.filePath) {
        const path = result.filePath
        const lastSlashIndex = path.lastIndexOf('\\')
        savePath.value = path.substring(0, lastSlashIndex)
        
        // 提取文件名（不含扩展名）
        const fullFileName = path.substring(lastSlashIndex + 1)
        const dotIndex = fullFileName.lastIndexOf('.')
        if (dotIndex > 0) {
          fileName.value = fullFileName.substring(0, dotIndex)
        }
      }
    } else {
      // 降级处理：使用默认路径
      savePath.value = 'C:\\Users\\User\\Pictures'
      message.info('使用默认保存路径: ' + savePath.value)
    }
  } catch (error) {
    console.error('选择保存路径失败:', error)
    message.error('选择保存路径失败')
  }
}

// 保存处理
const handleSave = async () => {
  if (!canSave.value) {
    message.warning('请完善保存信息')
    return
  }

  saving.value = true
  
  try {
    const saveOptions = {
      format: outputFormat.value,
      quality: outputFormat.value === 'jpg' ? quality.value : 100,
      fileName: fileName.value,
      savePath: savePath.value,
      fullPath: `${savePath.value}\\${fileName.value}.${outputFormat.value}`
    }
    
    await emit('save', saveOptions)
    lastSaveTime.value = new Date()
    
    // 向父组件更新保存时间
    emit('update:last-save-time', lastSaveTime.value)
    
    message.success('图像保存成功')
  } catch (error) {
    console.error('保存失败:', error)
    message.error('保存失败: ' + error.message)
  } finally {
    saving.value = false
  }
}

// 另存为处理
const handleSaveAs = async () => {
  await selectSavePath()
  if (canSave.value) {
    await handleSave()
  }
}

// 关闭面板处理
const handleClose = () => {
  emit('close')
}

// 获取预估文件大小
function getEstimatedSize() {
  if (!props.imageData) return '0 KB'
  
  let estimatedSize = props.imageData.size || 0
  
  // 根据格式调整预估大小
  switch (outputFormat.value) {
    case 'png':
      estimatedSize *= 1.2 // PNG通常比原始大一些
      break
    case 'jpg':
      estimatedSize *= (quality.value / 100) * 0.8 // JPG压缩
      break
    case 'bmp':
      estimatedSize *= 3 // BMP无压缩，较大
      break
    case 'gif':
      estimatedSize *= 0.6 // GIF有压缩
      break
  }
  
  return formatFileSize(Math.round(estimatedSize))
}

// 更新预估大小到父组件
function updateEstimatedSize() {
  const size = getEstimatedSize()
  emit('update:estimated-size', size)
}

// 格式化文件大小
function formatFileSize(bytes) {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 格式化时间
const formatTime = (date) => {
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 初始化默认保存路径
const initDefaultPath = () => {
  if (!savePath.value) {
    // 在渲染进程中使用默认路径，不依赖process.env
    savePath.value = 'C:\\Users\\User\\Pictures'
  }
}

// 组件挂载时初始化
initDefaultPath()
</script>

<style scoped>
.save-panel {
  background: transparent;
  padding: 0;
  margin: 0;
  width: 100%;
  box-sizing: border-box;
}

.save-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 24px 36px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  align-items: flex-end;
  width: fit-content;
  margin-left: auto;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 2px;
  right: 4px; /* 更靠右上角 */
  width: 24px;
  height: 24px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  color: #999; /* 默认灰色 */
  background: transparent !important; /* 无背景 */
  border: none; /* 无边框 */
  cursor: pointer;
  z-index: 10;
  transition: color 0.15s ease, transform 0.15s ease, filter 0.15s ease;
}

.close-btn:hover {
  color: #333;
  transform: scale(1.08);
}

.close-icon {
  width: 16px;
  height: 16px;
  color: inherit;
}

.save-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.first-row {
  /* 第一行：文件名 + 保存路径 + 浏览按钮 */
}

.second-row {
  /* 第二行：选择格式 + 保存按钮 */
  gap: 16px;
}

.input-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.path-group {
  margin-left: 12px;
  margin-right: 12px;
}

.format-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.input-label,
.format-label,
.quality-label {
  font-size: 14px;
  color: #333;
  white-space: nowrap;
  font-weight: 500;
}

.filename-input {
  width: 280px;
  background: rgba(255, 255, 255, 0.9) !important;
  border: 1px solid rgba(0, 0, 0, 0.2) !important;
}

.path-input {
  width: 280px;
  background: rgba(255, 255, 255, 0.9) !important;
  border: 1px solid rgba(0, 0, 0, 0.2) !important;
}

.file-extension {
  font-size: 14px;
  margin-left: 4px;
}

.browse-btn {
  flex-shrink: 0;
  border-radius: 6px;
  height: 32px;
}

.format-select {
  width: 80px;
}

.format-select .ant-select-selector {
  background: transparent !important;
}

.save-button {
  flex-shrink: 0;
  border-radius: 6px;
  font-weight: 500;
  height: 32px;
}

.quality-row {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 8px;
  padding: 8px 0;
}

.quality-label {
  font-size: 14px;
  color: #333;
  white-space: nowrap;
  font-weight: 500;
  min-width: 80px;
}

.quality-slider {
  flex: 1;
  max-width: 300px;
}

.save-info {
  display: flex;
  align-items: center;
  padding-top: 8px;
  border-top: 1px solid #f0f0f0;
}

.info-item {
  font-size: 12px;
  color: #8c8c8c;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 图标样式优化 */
.button-icon {
  width: 14px !important;
  height: 14px !important;
  font-size: 14px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.info-icon {
  width: 12px !important;
  height: 12px !important;
  font-size: 12px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

/* 输入框响应式样式 */
.file-name-input {
  width: 200px;
}

.save-path-input {
  width: 300px;
}

/* 响应式布局 */
@media (max-width: 1200px) {
  .filename-input {
    width: 240px;
  }

  .path-input {
    width: 240px;
  }
}

@media (max-width: 900px) {
  .save-content {
    width: 100%;
    margin-left: 0;
  }

  .first-row {
    flex-wrap: wrap;
    gap: 8px;
  }

  .path-group {
    margin: 4px 8px;
  }

  .filename-input {
    width: 200px;
  }

  .path-input {
    width: 200px;
  }
}

@media (max-width: 600px) {
  .save-panel {
    padding: 12px;
  }

  .save-content {
    padding: 6px;
    align-items: stretch;
  }

  .save-row {
    flex-direction: column;
    align-items: stretch;
    gap: 6px;
  }

  .input-group,
  .format-group {
    justify-content: space-between;
  }

  .filename-input,
  .path-input {
    flex: 1;
  }

  .format-select {
    width: 80px;
  }

  .save-button {
    width: 100%;
  }

  .input-label,
  .format-label,
  .quality-label {
    font-size: 13px;
  }
}
</style>
