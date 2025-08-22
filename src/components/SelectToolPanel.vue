<template>
  <div class="select-tool-panel">
    <!-- 工具说明区域 -->
    <div class="property-section">
      <div class="section-title">选择工具</div>
      <p class="section-desc">点击和拖拽来选择区域</p>
    </div>
  </div>
</template>

<script setup>
/**
 * 选择工具属性面板
 * 功能：
 * - 展示选择工具的使用说明
 */
</script>

<style scoped>
.select-tool-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.property-section {
  flex: 1;
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

.clear-section {
  padding: 12px 0 0;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.06);
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