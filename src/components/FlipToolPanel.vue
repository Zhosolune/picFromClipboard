<template>
  <div class="property-section">
    <div class="section-title">翻转</div>
    <a-space direction="vertical" style="width: 100%">
      <a-button block @click="flipHorizontal">
        <template #icon><ArrowSwap24Regular class="button-icon" /></template>
        水平翻转
      </a-button>
      <a-button block @click="flipVertical">
        <template #icon><ArrowSwap24Regular class="button-icon" style="transform: rotate(90deg)" /></template>
        垂直翻转
      </a-button>
    </a-space>
  </div>
</template>

<script setup>
import { message } from 'ant-design-vue'
import { ArrowSwap24Regular } from '@vicons/fluent'

// Props
const props = defineProps({
  currentTool: {
    type: String,
    default: 'flip'
  },
  imageData: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['image-change'])

/**
 * 水平翻转
 */
const flipHorizontal = async () => {
  if (!props.imageData) {
    message.warning('没有图像数据')
    return
  }

  try {
    const result = await window.electronAPI.python.execute('flip_horizontal', {
      input: props.imageData.data
    })

    if (result.success) {
      const newImageData = { ...props.imageData, ...result }
      emit('image-change', newImageData)
      message.success('水平翻转成功')
    } else {
      message.error('翻转失败: ' + (result.error || '未知错误'))
    }
  } catch (error) {
    message.error('翻转失败: ' + error.message)
  }
}

/**
 * 垂直翻转
 */
const flipVertical = async () => {
  if (!props.imageData) {
    message.warning('没有图像数据')
    return
  }

  try {
    const result = await window.electronAPI.python.execute('flip_vertical', {
      input: props.imageData.data
    })

    if (result.success) {
      const newImageData = { ...props.imageData, ...result }
      emit('image-change', newImageData)
      message.success('垂直翻转成功')
    } else {
      message.error('翻转失败: ' + (result.error || '未知错误'))
    }
  } catch (error) {
    message.error('翻转失败: ' + error.message)
  }
}
</script>

<style scoped>
.property-section {
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  margin-bottom: 16px;
}

.section-title {
  font-weight: 600;
  margin-bottom: 12px;
  color: #262626;
}

.button-icon {
  width: 16px;
  height: 16px;
}
</style>