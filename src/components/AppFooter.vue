<template>
  <div class="app-footer">
    <div class="footer-content">
      <div class="left">
        <slot name="left">
          <span class="status-text">就绪</span>
        </slot>
      </div>
      <div class="right">
        <slot name="right">
          <a-space>
            <span v-if="estimatedSize" class="info-item">
              <Image24Regular class="info-icon" />
              {{ estimatedSize }}
            </span>
            <span v-if="lastSaveTime" class="info-item">
              <Clock24Regular class="info-icon" />
              上次保存: {{ formatTime(lastSaveTime) }}
            </span>
          </a-space>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Image24Regular, Clock24Regular } from '@vicons/fluent'

const props = defineProps({
  imageData: { type: Object, default: null },
  estimatedSize: { type: String, default: '' },
  lastSaveTime: { type: [String, Date, Number], default: null },
  statusText: { type: String, default: '就绪' },
})

/**
 * 格式化时间输出
 * @param {Date|number|string} date 时间对象或时间戳
 * @returns {string} HH:mm:ss
 */
const formatTime = (date) => {
  const d = date instanceof Date ? date : new Date(date)
  return d.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>

<style scoped>
.app-footer {
  height: 24px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  position: relative;
  z-index: 10;
}

:global([data-theme="dark"]) .app-footer {
  background: rgba(28, 28, 30, 0.9);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.footer-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px;
}

.left .status-text {
  font-size: 12px;
  color: #595959;
  line-height: 1;
  vertical-align: middle;
  display: inline-block;
  transform: translateY(-3px);
}

.right .info-item {
  font-size: 12px;
  color: #8c8c8c;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.info-icon {
  width: 12px !important;
  height: 12px !important;
  font-size: 12px !important;
}
</style>