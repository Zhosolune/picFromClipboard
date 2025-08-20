<template>
  <div class="toolbar">
    <div class="tool-group">
      <div class="tool-group-title">选择</div>
      <a-tooltip title="选择工具" placement="right">
        <div
          class="toolbar-button"
          :class="{ active: currentTool === 'select' }"
          @click="$emit('tool-change', 'select')"
        >
          <Cursor24Regular class="tool-icon" />
        </div>
      </a-tooltip>
    </div>

    <div class="tool-group">
      <div class="tool-group-title">裁剪</div>
      <a-tooltip title="自由裁剪" placement="right">
        <div
          class="toolbar-button"
          :class="{ active: currentTool === 'crop' }"
          @click="$emit('tool-change', 'crop')"
        >
          <Cut24Regular class="tool-icon" />
        </div>
      </a-tooltip>

      <a-tooltip title="固定比例裁剪" placement="right">
        <div
          class="toolbar-button"
          :class="{ active: currentTool === 'crop-ratio' }"
          @click="$emit('tool-change', 'crop-ratio')"
        >
          <CropInterim24Regular class="tool-icon" />
        </div>
      </a-tooltip>
    </div>

    <div class="tool-group">
      <div class="tool-group-title">变换</div>
      <a-tooltip title="旋转" placement="right">
        <div
          class="toolbar-button"
          :class="{ active: currentTool === 'rotate' }"
          @click="$emit('tool-change', 'rotate')"
        >
          <ArrowRotateClockwise24Regular class="tool-icon" />
        </div>
      </a-tooltip>

      <a-tooltip title="翻转" placement="right">
        <div
          class="toolbar-button"
          :class="{ active: currentTool === 'flip' }"
          @click="$emit('tool-change', 'flip')"
        >
          <FlipHorizontal24Regular class="tool-icon" />
        </div>
      </a-tooltip>
    </div>

    <div class="tool-group">
      <div class="tool-group-title">标注</div>
      <a-tooltip title="文字标注" placement="right">
        <div 
          class="toolbar-button"
          :class="{ active: currentTool === 'text' }"
          @click="$emit('tool-change', 'text')"
        >
          <TextFont24Regular class="tool-icon" />
        </div>
      </a-tooltip>
      
      <a-tooltip title="矩形" placement="right">
        <div 
          class="toolbar-button"
          :class="{ active: currentTool === 'rectangle' }"
          @click="$emit('tool-change', 'rectangle')"
        >
          <RectangleLandscape24Regular class="tool-icon" />
        </div>
      </a-tooltip>
      
      <a-tooltip title="圆形" placement="right">
        <div 
          class="toolbar-button"
          :class="{ active: currentTool === 'circle' }"
          @click="$emit('tool-change', 'circle')"
        >
          <Circle24Regular class="tool-icon" />
        </div>
      </a-tooltip>
      
      <a-tooltip title="直线" placement="right">
        <div 
          class="toolbar-button"
          :class="{ active: currentTool === 'line' }"
          @click="$emit('tool-change', 'line')"
        >
          <Line24Regular class="tool-icon" />
        </div>
      </a-tooltip>
      
      <a-tooltip title="箭头" placement="right">
        <div 
          class="toolbar-button"
          :class="{ active: currentTool === 'arrow' }"
          @click="$emit('tool-change', 'arrow')"
        >
          <ArrowRight24Regular class="tool-icon" />
        </div>
      </a-tooltip>
    </div>

    <div class="tool-group">
      <div class="tool-group-title">操作</div>
      <a-tooltip title="撤销 (Ctrl+Z)" placement="right">
        <div 
          class="toolbar-button"
          @click="$emit('tool-change', 'undo')"
        >
          <ArrowUndo24Regular class="tool-icon" />
        </div>
      </a-tooltip>
      
      <a-tooltip title="重做 (Ctrl+Y)" placement="right">
        <div 
          class="toolbar-button"
          @click="$emit('tool-change', 'redo')"
        >
          <ArrowRedo24Regular class="tool-icon" />
        </div>
      </a-tooltip>
    </div>
  </div>
</template>

<script setup>
import {
  Cursor24Regular,
  Cut24Regular,
  CropInterim24Regular,
  ArrowRotateClockwise24Regular,
  FlipHorizontal24Regular,
  TextFont24Regular,
  RectangleLandscape24Regular,
  Circle24Regular,
  Line24Regular,
  ArrowRight24Regular,
  ArrowUndo24Regular,
  ArrowRedo24Regular
} from '@vicons/fluent'

// Props
defineProps({
  currentTool: {
    type: String,
    default: 'select'
  }
})

// Emits
defineEmits(['tool-change'])
</script>

<style scoped>
.toolbar {
  background: transparent;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  height: 100%;
  overflow-y: auto;
}

.tool-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.tool-group-title {
  font-size: 12px;
  color: #8c8c8c;
  text-align: center;
  margin-bottom: 4px;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 4px;
}

.toolbar-button {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  cursor: pointer;
  transition: all 0.3s ease;
  color: #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

/* 降级方案 */
@supports not (backdrop-filter: blur(10px)) {
  .toolbar-button {
    background: rgba(255, 255, 255, 0.8);
  }
}

.toolbar-button:hover {
  background: rgba(255, 255, 255, 0.8);
  border-color: rgba(24, 144, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  color: #1890ff;
}

.toolbar-button.active {
  background: rgba(24, 144, 255, 0.2);
  border-color: rgba(24, 144, 255, 0.6);
  color: #1890ff;
  box-shadow: 0 2px 8px rgba(24, 144, 255, 0.3);
}

.toolbar-button:active {
  transform: scale(0.95) translateY(-1px);
}

/* 图标样式优化 */
.tool-icon {
  width: 18px !important;
  height: 18px !important;
  font-size: 18px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  position: absolute !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
}
</style>
