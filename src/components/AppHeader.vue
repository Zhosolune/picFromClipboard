<template>
  <div class="app-header">
    <div class="header-content">
      <!-- 左侧标题 -->
      <div class="header-title">
        <span>剪贴板图像处理工具</span>
      </div>

      <!-- 右侧操作按钮 -->
      <div class="header-actions">
        <!-- 移除：清空按钮 -->
        <a-tooltip title="切换主题">
          <a-button
            type="text"
            size="small"
            @click="toggleTheme"
            class="header-btn"
          >
            <template #icon>
              <WeatherSunny24Regular v-if="currentTheme === 'dark'" class="header-icon" />
              <WeatherMoon24Regular v-else class="header-icon" />
            </template>
          </a-button>
        </a-tooltip>

        <a-tooltip title="设置">
          <a-button
            type="text"
            size="small"
            @click="openSettings"
            class="header-btn"
          >
            <template #icon>
              <Settings24Regular class="header-icon" />
            </template>
          </a-button>
        </a-tooltip>

        <a-tooltip title="关于">
          <a-button
            type="text"
            size="small"
            @click="showAbout"
            class="header-btn"
          >
            <template #icon>
              <Info24Regular class="header-icon" />
            </template>
          </a-button>
        </a-tooltip>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import {
  WeatherSunny24Regular,
  WeatherMoon24Regular,
  Settings24Regular,
  Info24Regular
} from '@vicons/fluent'

// Emits
const emit = defineEmits(['theme-change'])

// 响应式数据
const currentTheme = ref('light')

/**
 * 切换主题
 * 在亮色和暗色主题之间切换
 */
const toggleTheme = () => {
  currentTheme.value = currentTheme.value === 'light' ? 'dark' : 'light'
  emit('theme-change', currentTheme.value)
  
  // 应用主题到document
  document.documentElement.setAttribute('data-theme', currentTheme.value)
  
  message.success(`已切换到${currentTheme.value === 'light' ? '亮色' : '暗色'}主题`)
}

/**
 * 打开设置对话框
 * 显示应用设置界面
 */
const openSettings = () => {
  // TODO: 实现设置对话框
  message.info('设置功能开发中...')
}

/**
 * 显示关于信息
 * 显示应用版本和作者信息
 */
const showAbout = () => {
  // TODO: 实现关于对话框
  message.info('剪贴板图像处理工具 v1.0.0')
}

// 组件挂载时初始化主题
onMounted(() => {
  // 从本地存储读取主题设置
  const savedTheme = localStorage.getItem('app-theme') || 'light'
  currentTheme.value = savedTheme
  document.documentElement.setAttribute('data-theme', savedTheme)
  emit('theme-change', savedTheme)
})

// 监听主题变化并保存到本地存储
const saveTheme = (theme) => {
  localStorage.setItem('app-theme', theme)
}
</script>

<style scoped>
.app-header {
  height: 48px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  z-index: 20;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

/* 暗色主题样式 */
:global([data-theme="dark"]) .app-header {
  background: rgba(28, 28, 30, 0.9);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

/* 降级方案 */
@supports not (backdrop-filter: blur(20px)) {
  .app-header {
    background: rgba(255, 255, 255, 0.95);
  }
  
  :global([data-theme="dark"]) .app-header {
    background: rgba(28, 28, 30, 0.95);
  }
}

.header-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: #262626;
  user-select: none;
}

:global([data-theme="dark"]) .header-title {
  color: #ffffff;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 图标按钮：等宽高 + 透明背景 */
.header-btn,
:deep(.header-btn.ant-btn),
:deep(.header-btn.ant-btn-text),
:deep(.header-btn.ant-btn-icon-only) {
  width: 32px;
  height: 32px;
  min-width: 32px;
  min-height: 32px;
  padding: 0 !important;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  background: transparent !important;
  background-color: transparent !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
  /* 禁用磨砂玻璃效果 */
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

/* hover效果：响应式背景色变化 */
.header-btn:hover,
:deep(.header-btn.ant-btn:hover),
:deep(.header-btn.ant-btn-text:hover),
:deep(.header-btn.ant-btn-icon-only:hover) {
  background: rgba(0, 0, 0, 0.08) !important;
  background-color: rgba(0, 0, 0, 0.08) !important;
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}

:global([data-theme="dark"]) .header-btn:hover,
:global([data-theme="dark"]) :deep(.header-btn.ant-btn:hover),
:global([data-theme="dark"]) :deep(.header-btn.ant-btn-text:hover),
:global([data-theme="dark"]) :deep(.header-btn.ant-btn-icon-only:hover) {
  background: rgba(255, 255, 255, 0.08) !important;
  background-color: rgba(255, 255, 255, 0.08) !important;
}

/* active效果 */
.header-btn:active,
.header-btn:focus,
:deep(.header-btn.ant-btn:active),
:deep(.header-btn.ant-btn:focus),
:deep(.header-btn.ant-btn-icon-only:active),
:deep(.header-btn.ant-btn-icon-only:focus) {
  background: rgba(0, 0, 0, 0.12);
  background-color: rgba(0, 0, 0, 0.12);
  border: none !important;
  box-shadow: none !important;
  outline: none !important;
}

:global([data-theme="dark"]) .header-btn:active,
:global([data-theme="dark"]) .header-btn:focus,
:global([data-theme="dark"]) :deep(.header-btn.ant-btn:active),
:global([data-theme="dark"]) :deep(.header-btn.ant-btn:focus),
:global([data-theme="dark"]) :deep(.header-btn.ant-btn-icon-only:active),
:global([data-theme="dark"]) :deep(.header-btn.ant-btn-icon-only:focus) {
  background: rgba(255, 255, 255, 0.12) !important;
  background-color: rgba(255, 255, 255, 0.12) !important;
}

/* 彻底移除 antd 在不同状态下注入的背景 */
:deep(.header-btn.ant-btn-text:not(:disabled):hover),
:deep(.header-btn.ant-btn-text:not(:disabled):active),
:deep(.header-btn.ant-btn.ant-tooltip-open),
:deep(.header-btn.ant-btn-icon-only:not(:disabled):hover),
:deep(.header-btn.ant-btn-icon-only:not(:disabled):active) {
  background: rgba(0, 0, 0, 0.08) !important;
  background-color: rgba(0, 0, 0, 0.08) !important;
  background-image: none !important;
  box-shadow: none !important;
  border: none !important;
}

:global([data-theme="dark"]) :deep(.header-btn.ant-btn-text:not(:disabled):hover),
:global([data-theme="dark"]) :deep(.header-btn.ant-btn-text:not(:disabled):active),
:global([data-theme="dark"]) :deep(.header-btn.ant-btn.ant-tooltip-open),
:global([data-theme="dark"]) :deep(.header-btn.ant-btn-icon-only:not(:disabled):hover),
:global([data-theme="dark"]) :deep(.header-btn.ant-btn-icon-only:not(:disabled):active) {
  background: rgba(255, 255, 255, 0.08) !important;
  background-color: rgba(255, 255, 255, 0.08) !important;
}

/* 图标样式 */
.header-icon {
  width: 20px;
  height: 20px;
  color: #595959;
  transition: color 0.2s ease;
}

:global([data-theme="dark"]) .header-icon {
  color: #d9d9d9;
}
</style>