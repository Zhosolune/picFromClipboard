<template>
  <div v-if="currentTool === 'shape' || ['rectangle', 'circle', 'line', 'arrow'].includes(currentTool)" class="property-section">
    <div class="section-title">图形工具</div>
    <a-space direction="vertical" style="width: 100%">
      <!-- 子工具选择 -->
      <div class="form-item">
        <label>图形类型</label>
        <a-radio-group v-model:value="selectedShape" @change="handleShapeChange">
          <a-radio-button value="rectangle">矩形</a-radio-button>
          <a-radio-button value="circle">圆形</a-radio-button>
          <a-radio-button value="line">直线</a-radio-button>
          <a-radio-button value="arrow">箭头</a-radio-button>
        </a-radio-group>
      </div>
      
      <div class="form-item">
        <label>线条粗细</label>
        <a-slider 
          v-model:value="strokeWidth"
          :min="1"
          :max="20"
          :marks="{ 1: '1px', 5: '5px', 10: '10px', 20: '20px' }"
        />
      </div>
      
      <div class="form-item">
        <label>线条颜色</label>
        <a-input 
          v-model:value="strokeColor"
          type="color"
          style="width: 100%"
        />
      </div>
      
      <!-- 填充选项仅对矩形和圆形显示 -->
      <div v-if="['rectangle', 'circle'].includes(selectedShape)" class="form-item">
        <label>填充颜色</label>
        <a-space>
          <a-switch v-model:checked="hasFill" />
          <a-input 
            v-model:value="fillColor"
            type="color"
            :disabled="!hasFill"
            style="flex: 1"
          />
        </a-space>
      </div>
    </a-space>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

// Props
const props = defineProps({
  currentTool: {
    type: String,
    default: 'select'
  }
})

// Emits
const emit = defineEmits(['options-change', 'shape-change'])

// 图形相关响应式数据
const strokeWidth = ref(2)
const strokeColor = ref('#000000')
const fillColor = ref('#ffffff')
const hasFill = ref(false)

// 当前选中的图形类型
const selectedShape = ref(props.currentTool === 'shape' ? 'rectangle' : props.currentTool)

// 监听 currentTool 变化，同步更新 selectedShape
watch(() => props.currentTool, (newTool) => {
  if (newTool === 'shape') {
    // 如果是新的 shape 工具，默认选择矩形
    selectedShape.value = 'rectangle'
  } else if (['rectangle', 'circle', 'line', 'arrow'].includes(newTool)) {
    // 如果是具体的图形工具，直接设置
    selectedShape.value = newTool
  }
})

/**
 * 处理图形类型变更
 */
const handleShapeChange = () => {
  // 通知父组件切换工具
  emit('shape-change', selectedShape.value)
}

/**
 * 监听图形属性变化并发送给父组件
 */
watch([
  strokeWidth, strokeColor, fillColor, hasFill, selectedShape
], () => {
  emit('options-change', {
    selectedShape: selectedShape.value,
    strokeWidth: strokeWidth.value,
    strokeColor: strokeColor.value,
    fillColor: fillColor.value,
    hasFill: hasFill.value
  })
}, { deep: true })
</script>

<style scoped>
.property-section {
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.section-title {
  font-weight: 600;
  margin-bottom: 16px;
  color: #262626;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-item label {
  font-size: 14px;
  color: #595959;
  font-weight: 500;
}

.ant-radio-group {
  width: 100%;
}

.ant-radio-button-wrapper {
  flex: 1;
  text-align: center;
}
</style>