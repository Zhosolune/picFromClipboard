<template>
  <div v-if="currentTool === 'text'" class="property-section">
    <div class="section-title">文字</div>
    <a-space direction="vertical" style="width: 100%">
      <div class="form-item">
        <label>文字内容</label>
        <a-textarea 
          v-model:value="textContent"
          placeholder="请输入文字内容"
          :rows="3"
        />
      </div>
      
      <div class="form-item">
        <label>字体大小</label>
        <a-slider 
          v-model:value="fontSize"
          :min="12"
          :max="72"
          :marks="{ 12: '12px', 24: '24px', 36: '36px', 48: '48px', 72: '72px' }"
        />
      </div>
      
      <div class="form-item">
        <label>字体颜色</label>
        <a-input 
          v-model:value="textColor"
          type="color"
          style="width: 100%"
        />
      </div>
      
      <div class="form-item">
        <label>字体样式</label>
        <a-space>
          <a-button 
            :type="textBold ? 'primary' : 'default'"
            @click="textBold = !textBold"
          >
            <strong>B</strong>
          </a-button>
          <a-button 
            :type="textItalic ? 'primary' : 'default'"
            @click="textItalic = !textItalic"
          >
            <em>I</em>
          </a-button>
        </a-space>
      </div>
    </a-space>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

// Props
const props = defineProps({
  currentTool: {
    type: String,
    default: 'select'
  }
})

// Emits
const emit = defineEmits(['options-change'])

// 文字相关响应式数据
const textContent = ref('')
const fontSize = ref(24)
const textColor = ref('#000000')
const textBold = ref(false)
const textItalic = ref(false)

/**
 * 监听文字属性变化并发送给父组件
 */
watch([
  textContent, fontSize, textColor, 
  textBold, textItalic
], () => {
  emit('options-change', {
    textContent: textContent.value,
    fontSize: fontSize.value,
    textColor: textColor.value,
    textBold: textBold.value,
    textItalic: textItalic.value
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
</style>