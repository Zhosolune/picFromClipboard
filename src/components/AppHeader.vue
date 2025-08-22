<template>
  <div class="app-header">
    <div class="header-content">
      <!-- 左侧工具按钮 -->
      <div class="header-tools">
        <!-- 撤销重做组 -->
        <div class="undo-redo-group">
          <a-tooltip title="撤销 (Ctrl+Z)">
            <a-button
              type="text"
              size="small"
              @click="handleUndo"
              class="header-btn small"
            >
              <template #icon>
                <ArrowUndo24Regular class="header-icon small" />
              </template>
            </a-button>
          </a-tooltip>

          <a-tooltip title="重做 (Ctrl+Y)">
            <a-button
              type="text"
              size="small"
              @click="handleRedo"
              class="header-btn small"
            >
              <template #icon>
                <ArrowRedo24Regular class="header-icon small" />
              </template>
            </a-button>
          </a-tooltip>
        </div>

        <!-- 分隔线 -->
        <div class="header-divider"></div>

        <!-- 选择工具 -->
        <a-tooltip title="选择工具">
          <a-button
            type="text"
            size="small"
            @click="handleSelectTool"
            :class="['header-btn', { 'active': currentTool === 'select' }]"
          >
            <template #icon>
              <Cursor24Regular class="header-icon" />
            </template>
          </a-button>
        </a-tooltip>

        <!-- 保存按钮 -->
        <a-tooltip title="保存">
          <a-button
            type="primary"
            size="small"
            @click="handleSave"
            class="save-btn"
          >
            <template #icon>
              <Save24Regular class="save-icon" />
            </template>
            保存
          </a-button>
        </a-tooltip>

        <!-- 清空按钮 -->
        <a-tooltip title="清空">
          <a-button
            danger
            size="small"
            @click="handleClear"
            class="clear-btn"
          >
            <template #icon>
              <Delete24Regular class="clear-icon" />
            </template>
            清空
          </a-button>
        </a-tooltip>
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
  Info24Regular,
  ArrowUndo24Regular,
  ArrowRedo24Regular,
  Cursor24Regular,
  Delete24Regular,
  Save24Regular
} from '@vicons/fluent'

// Props
const props = defineProps({
  currentTool: {
    type: String,
    default: 'select'
  }
})

// Emits
const emit = defineEmits(['theme-change', 'tool-change', 'undo', 'redo', 'clear', 'save'])

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

/**
 * 处理撤销操作
 */
const handleUndo = () => {
  emit('undo')
}

/**
 * 处理重做操作
 */
const handleRedo = () => {
  emit('redo')
}

/**
 * 处理选择工具切换
 */
const handleSelectTool = () => {
  emit('tool-change', 'select')
}

/**
 * 处理保存操作
 */
const handleSave = () => {
  emit('save')
}

/**
 * 处理清空操作
 */
const handleClear = () => {
  emit('clear')
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

.header-tools {
  display: flex;
  align-items: center;
  gap: 16px;
}

.undo-redo-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.header-divider {
  width: 1px;
  height: 20px;
  background: rgba(0, 0, 0, 0.15);
  margin: 0 4px;
}

:global([data-theme="dark"]) .header-divider {
  background: rgba(255, 255, 255, 0.2);
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

/* 小尺寸按钮样式 */
.header-btn.small,
:deep(.header-btn.small.ant-btn),
:deep(.header-btn.small.ant-btn-text),
:deep(.header-btn.small.ant-btn-icon-only) {
  width: 28px;
  height: 28px;
  min-width: 28px;
  min-height: 28px;
}

/* 保存按钮样式 */
.save-btn,
:deep(.save-btn.ant-btn),
:deep(.save-btn.ant-btn-primary) {
  height: 32px !important;
  padding: 0 12px !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  border-radius: 6px !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  margin-left: 8px !important;
  transition: all 0.2s ease !important;
  background: transparent !important;
  background-color: transparent !important;
  border: 1px solid #1890ff !important;
  color: #1890ff !important;
}

.save-btn:hover,
:deep(.save-btn.ant-btn:hover),
:deep(.save-btn.ant-btn-primary:hover) {
  background: rgba(24, 144, 255, 0.1) !important;
  background-color: rgba(24, 144, 255, 0.1) !important;
  border-color: #1890ff !important;
}

.save-icon {
  width: 16px;
  height: 16px;
  color: #1890ff;
}

/* 清空按钮样式 */
.clear-btn,
:deep(.clear-btn.ant-btn),
:deep(.clear-btn.ant-btn-dangerous) {
  height: 32px !important;
  padding: 0 12px !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  border-radius: 6px !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  margin-left: 8px !important;
  transition: all 0.2s ease !important;
  background: transparent !important;
  background-color: transparent !important;
  border: 1px solid #ff4d4f !important;
  color: #ff4d4f !important;
}

.clear-btn:hover,
:deep(.clear-btn.ant-btn:hover),
:deep(.clear-btn.ant-btn-dangerous:hover) {
  background: rgba(255, 77, 79, 0.1) !important;
  background-color: rgba(255, 77, 79, 0.1) !important;
  border-color: #ff4d4f !important;
}

.clear-icon {
  width: 16px;
  height: 16px;
  color: #ff4d4f;
}

/* 小图标样式 */
.header-icon.small {
  width: 16px;
  height: 16px;
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

/* 激活状态样式 */
.header-btn.active,
:deep(.header-btn.active.ant-btn),
:deep(.header-btn.active.ant-btn-text) {
  background: rgba(24, 144, 255, 0.1) !important;
  background-color: rgba(24, 144, 255, 0.1) !important;
}

.header-btn.active .header-icon {
  color: #1890ff;
}

:global([data-theme="dark"]) .header-btn.active,
:global([data-theme="dark"]) :deep(.header-btn.active.ant-btn),
:global([data-theme="dark"]) :deep(.header-btn.active.ant-btn-text) {
  background: rgba(24, 144, 255, 0.15) !important;
  background-color: rgba(24, 144, 255, 0.15) !important;
}

:global([data-theme="dark"]) .header-btn.active .header-icon {
  color: #40a9ff;
}

/* 暗色主题下的保存按钮样式 */
:global([data-theme="dark"]) .save-btn,
:global([data-theme="dark"]) :deep(.save-btn.ant-btn),
:global([data-theme="dark"]) :deep(.save-btn.ant-btn-primary) {
  border-color: #40a9ff !important;
  color: #40a9ff !important;
}

:global([data-theme="dark"]) .save-btn:hover,
:global([data-theme="dark"]) :deep(.save-btn.ant-btn:hover),
:global([data-theme="dark"]) :deep(.save-btn.ant-btn-primary:hover) {
  background: rgba(64, 169, 255, 0.15) !important;
  background-color: rgba(64, 169, 255, 0.15) !important;
  border-color: #40a9ff !important;
}

:global([data-theme="dark"]) .save-icon {
  color: #40a9ff;
}

/* 暗色主题下的清空按钮样式 */
:global([data-theme="dark"]) .clear-btn,
:global([data-theme="dark"]) :deep(.clear-btn.ant-btn),
:global([data-theme="dark"]) :deep(.clear-btn.ant-btn-dangerous) {
  border-color: #ff7875 !important;
  color: #ff7875 !important;
}

:global([data-theme="dark"]) .clear-btn:hover,
:global([data-theme="dark"]) :deep(.clear-btn.ant-btn:hover),
:global([data-theme="dark"]) :deep(.clear-btn.ant-btn-dangerous:hover) {
  background: rgba(255, 120, 117, 0.15) !important;
  background-color: rgba(255, 120, 117, 0.15) !important;
  border-color: #ff7875 !important;
}

:global([data-theme="dark"]) .clear-icon {
  color: #ff7875;
}
</style>