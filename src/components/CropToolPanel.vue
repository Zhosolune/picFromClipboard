<template>
  <div class="crop-tool-panel">
    <!-- 模式选择 -->
    <div class="property-section">
      <div class="section-title">裁剪模式</div>
      <a-segmented 
        v-model:value="selectedMode" 
        :options="segmentedOptions" 
        @change="handleModeChange"
        block
      >
        <template #label="{ title, value }">
          <div style="display: flex; align-items: center; gap: 4px;">
            <CropInterim24Regular v-if="value === 'free'" style="width: 16px; height: 16px;" />
            <Crop24Regular v-if="value === 'ratio'" style="width: 16px; height: 16px;" />
            <span>{{ title }}</span>
          </div>
        </template>
      </a-segmented>
    </div>

    <!-- 自由裁剪 -->
    <div v-if="selectedMode === 'free'" class="property-section">
      <div class="section-title">自由裁剪</div>
      <a-space direction="vertical" style="width: 100%">
        <a-button type="primary" block @click="applyCrop">
          <template #icon><Checkmark24Regular class="button-icon" /></template>
          应用裁剪
        </a-button>
        <a-button block @click="cancelCrop">
          <template #icon><Dismiss24Regular class="button-icon" /></template>
          取消裁剪
        </a-button>
      </a-space>
    </div>

    <!-- 固定比例裁剪 -->
    <div v-else-if="selectedMode === 'ratio'" class="property-section">
      <div class="section-title">固定比例裁剪</div>
      <a-space direction="vertical" style="width: 100%">
        <div class="form-item">
          <label>裁剪比例</label>
          <a-select 
            v-model:value="cropRatio" 
            style="width: 100%"
            @change="handleCropRatioChange"
          >
            <a-select-option value="free">自由比例</a-select-option>
            <a-select-option value="1:1">1:1 (正方形)</a-select-option>
            <a-select-option value="4:3">4:3</a-select-option>
            <a-select-option value="16:9">16:9</a-select-option>
            <a-select-option value="3:2">3:2</a-select-option>
            <a-select-option value="custom">自定义</a-select-option>
          </a-select>
        </div>
        
        <div v-if="cropRatio === 'custom'" class="form-item">
          <label>自定义比例</label>
          <a-input-group compact>
            <a-input-number 
              v-model:value="customRatio.width" 
              :min="1" 
              style="width: 45%"
              placeholder="宽"
            />
            <a-input 
              style="width: 10%; text-align: center; pointer-events: none" 
              value=":" 
              disabled 
            />
            <a-input-number 
              v-model:value="customRatio.height" 
              :min="1" 
              style="width: 45%"
              placeholder="高"
            />
          </a-input-group>
        </div>

        <a-space direction="vertical" style="width: 100%">
          <a-button type="primary" block @click="applyCrop">
            <template #icon><Checkmark24Regular class="button-icon" /></template>
            应用裁剪
          </a-button>
          <a-button block @click="cancelCrop">
            <template #icon><Dismiss24Regular class="button-icon" /></template>
            取消裁剪
          </a-button>
        </a-space>
      </a-space>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, h } from 'vue'
import { message } from 'ant-design-vue'
import {
  Checkmark24Regular,
  Dismiss24Regular,
  CropInterim24Regular,
  Crop24Regular
} from '@vicons/fluent'

/**
 * 裁剪工具属性面板
 * 功能：
 * - 支持自由裁剪和固定比例裁剪两种模式
 * - 提供多种预设比例选项和自定义比例
 * - 处理裁剪应用和取消操作
 * - 向父组件传递裁剪参数和操作事件
 */

// Props
const props = defineProps({
  currentTool: {
    type: String,
    required: true
  },
  imageData: {
    type: Object,
    default: null
  },
  canvasRef: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['options-change', 'image-change', 'switch-tool'])

// 裁剪相关响应式数据
const selectedMode = ref('free')
const cropRatio = ref('free')
const customRatio = ref({ width: 1, height: 1 })

// Segmented组件选项配置
const segmentedOptions = [
  {
    title: '自由裁剪',
    value: 'free'
  },
  {
    title: '固定比例',
    value: 'ratio'
  }
]

/**
 * 模式切换处理
 * 当用户在属性面板切换自由/固定比例时调用
 */
const handleModeChange = () => {
  // 切换到固定比例模式时，若当前为自由比例，则默认设置为 1:1
  if (selectedMode.value === 'ratio' && cropRatio.value === 'free') {
    cropRatio.value = '1:1'
  }
  // 切换到自由裁剪时，比例恢复为自由
  if (selectedMode.value === 'free') {
    cropRatio.value = 'free'
  }
}

// 监听属性变化并发送给父组件
watch([selectedMode, cropRatio, customRatio], () => {
  emit('options-change', {
    cropMode: selectedMode.value,
    cropRatio: cropRatio.value,
    customRatio: customRatio.value
  })
}, { deep: true })

/**
 * 应用裁剪
 * 调用ImageCanvas的applyCrop方法进行图像裁剪处理
 * 成功后通过 image-change 向父级回传新图像
 */
const applyCrop = async () => {
  try {
    if (!props.canvasRef) {
      message.error('Canvas reference not available')
      return
    }
    
    // 调用ImageCanvas的applyCrop方法
    const croppedBlob = await props.canvasRef.applyCrop()
    
    if (croppedBlob) {
      // 创建新的图像URL
      const imageUrl = URL.createObjectURL(croppedBlob)
      
      // 发送裁剪完成事件
      emit('image-change', {
        imageUrl,
        blob: croppedBlob,
        mode: selectedMode.value,
        ratio: selectedMode.value === 'ratio' ? cropRatio.value : null,
        customRatio: selectedMode.value === 'ratio' && cropRatio.value === 'custom' ? customRatio.value : null
      })
      
      message.success('裁剪成功')
    } else {
      message.error('裁剪失败：无法获取裁剪结果')
    }
  } catch (error) {
    message.error('裁剪失败: ' + error.message)
  }
}

/**
 * 取消裁剪，重置为选择工具
 * 向父组件发送工具切换事件（通过选项变更告知）
 */
const cancelCrop = () => {
  emit('switch-tool', null) // 切换到默认工具
  emit('options-change', { tool: 'select' })
}

/**
 * 处理裁剪比例变更
 * 当用户选择不同的裁剪比例时触发
 * @param {string} value - 选择的裁剪比例值
 */
const handleCropRatioChange = (value) => {
  cropRatio.value = value
}
</script>

<style scoped>
.crop-tool-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.property-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 14px;
  font-weight: 500;
  color: #262626;
  margin-bottom: 12px;
}

.form-item {
  margin-bottom: 16px;
}

.form-item label {
  display: block;
  font-size: 12px;
  color: #595959;
  margin-bottom: 8px;
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
</style>