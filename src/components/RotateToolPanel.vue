<template>
  <div class="property-section">
    <div class="section-title">旋转</div>
    <a-space direction="vertical" style="width: 100%">
      <div class="quick-actions">
        <a-button @click="rotate(90)">90°</a-button>
        <a-button @click="rotate(180)">180°</a-button>
        <a-button @click="rotate(270)">270°</a-button>
      </div>
      
      <div class="form-item">
        <label>自定义角度</label>
        <a-slider 
          v-model:value="rotateAngle"
          :min="-180"
          :max="180"
          :marks="{ '-180': '-180°', '-90': '-90°', '0': '0°', '90': '90°', '180': '180°' }"
          @change="handleRotateChange"
        />
      </div>
    </a-space>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { message } from 'ant-design-vue'

// Props
const props = defineProps({
  currentTool: {
    type: String,
    default: 'rotate'
  },
  imageData: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['image-change'])

// 旋转相关
const rotateAngle = ref(0)

/**
 * 旋转图像
 * @param {number} angle - 旋转角度
 */
const rotate = async (angle) => {
  if (!props.imageData) {
    message.warning('没有图像数据')
    return
  }

  try {
    const result = await window.electronAPI.python.execute('rotate', {
      input: props.imageData.data,
      params: { angle }
    })

    if (result.success) {
      // 更新图像数据
      const newImageData = { ...props.imageData, ...result }
      emit('image-change', newImageData)
      message.success(`旋转${angle}°成功`)
    } else {
      message.error('旋转失败: ' + (result.error || '未知错误'))
    }
  } catch (error) {
    message.error('旋转失败: ' + error.message)
  }
}

/**
 * 旋转角度滑动回调
 * @param {number} value - 滑块值
 */
const handleRotateChange = async (value) => {
  rotateAngle.value = value
  await rotate(value)
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

.quick-actions {
  display: flex;
  gap: 8px;
  justify-content: space-between;
}

.quick-actions .ant-btn {
  flex: 1;
}

.form-item {
  margin-bottom: 16px;
}

.form-item:last-child {
  margin-bottom: 0;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #595959;
}
</style>