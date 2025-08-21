<template>
  <div class="property-section">
    <div class="section-title">选择工具</div>
    <p class="section-desc">点击和拖拽来选择区域</p>
  </div>
</template>

<script setup>
/**
 * 选择工具属性面板
 * 说明：
 * - 专注展示“选择工具”的说明与占位，后续可在此扩展选择框样式、吸附、羽化等选项。
 * - 清空按钮已统一移动到 PropertyPanel 底部操作区进行展示与触发。
 */
</script>

<style scoped>
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
</style>