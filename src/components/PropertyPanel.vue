<template>
  <div class="property-panel">
    <div class="panel-header">
      <h3>工具属性</h3>
    </div>
    
    <div class="panel-content">
      <!-- 选择工具（提取为独立组件） -->
      <SelectToolPanel v-if="currentTool === 'select'" />

      <!-- 裁剪工具（提取为独立组件） -->
      <CropToolPanel 
        v-if="currentTool === 'crop'" 
        :current-tool="currentTool"
        :image-data="imageData"
        :canvas-ref="canvasRef"
        @options-change="handleOptionsChange"
        @image-change="handleImageChange"
        @switch-tool="handleSwitchTool"
      />

      <!-- 旋转工具 -->
      <RotateToolPanel 
        v-else-if="currentTool === 'rotate'"
        :current-tool="currentTool"
        :image-data="imageData"
        @image-change="handleImageChange"
      />

      <!-- 翻转工具 -->
      <FlipToolPanel 
        v-else-if="currentTool === 'flip'"
        :current-tool="currentTool"
        :image-data="imageData"
        @image-change="handleImageChange"
      />

      <!-- 文字工具 -->
      <TextToolPanel 
        v-if="currentTool === 'text'"
        :current-tool="currentTool"
        @options-change="handleOptionsChange"
      />

      <!-- 图形工具 -->
      <ShapeToolPanel 
        v-if="currentTool === 'shape' || ['rectangle', 'circle', 'line', 'arrow'].includes(currentTool)"
        :current-tool="currentTool"
        @options-change="handleOptionsChange"
        @shape-change="handleShapeChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { message } from 'ant-design-vue'

import SelectToolPanel from './SelectToolPanel.vue'
import CropToolPanel from './CropToolPanel.vue'
import RotateToolPanel from './RotateToolPanel.vue'
import FlipToolPanel from './FlipToolPanel.vue'
import TextToolPanel from './TextToolPanel.vue'
import ShapeToolPanel from './ShapeToolPanel.vue'

// Props
const props = defineProps({
  currentTool: {
    type: String,
    default: 'select'
  },
  toolOptions: {
    type: Object,
    default: () => ({})
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
const emit = defineEmits(['options-change', 'image-change', 'clear', 'tool-change'])

/**
 * 处理工具切换
 * 当子组件请求切换工具时调用
 */
const handleSwitchTool = (tool) => {
  emit('tool-change', tool)
}

/**
 * 处理图形工具类型切换
 * 当用户在 ShapeToolPanel 中切换图形类型时调用
 */
const handleShapeChange = (shapeType) => {
  // 通知父组件切换当前工具
  emit('tool-change', shapeType)
}

/**
 * 处理子组件的选项变更事件
 * 统一处理来自各个工具面板的选项变更
 */
const handleOptionsChange = (options) => {
  // 如果子组件通过 options 中携带了 tool 字段，表示请求切换工具
  if (options && options.tool) {
    emit('tool-change', options.tool)
    return
  }
  emit('options-change', options)
}

/**
 * 处理子组件的图像变更事件
 * 统一处理来自各个工具面板的图像变更
 */
const handleImageChange = (imageData) => {
  emit('image-change', imageData)
}

/**
 * 处理"清空"按钮点击：
 * 向父组件派发 clear 事件，由父组件统一清空图像并隐藏保存面板
 */
const handleClear = () => {
  emit('clear')
}
</script>

<style scoped>
.property-panel {
  background: transparent;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.panel-header {
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
  color: #262626;
}

.panel-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
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

.section-desc {
  font-size: 12px;
  color: #8c8c8c;
  margin: 0;
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

.quick-actions {
  display: flex;
  gap: 8px;
}

.quick-actions .ant-btn {
  flex: 1;
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
