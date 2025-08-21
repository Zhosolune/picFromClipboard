<template>
  <div class="property-panel">
    <div class="panel-header">
      <h3>工具属性</h3>
    </div>
    
    <div class="panel-content">
      <!-- 选择工具（提取为独立组件） -->
      <SelectToolPanel v-if="currentTool === 'select'" />

      <!-- 裁剪工具 -->
      <div v-else-if="currentTool === 'crop'" class="property-section">
        <div class="section-title">自由裁剪</div>
        <a-space direction="vertical" style="width: 100%">
          <a-button type="primary" block @click="applyCrop">
            <template #icon><Checkmark24Regular class="button-icon" /></template>
            应用裁剪
          </a-button>
          <a-button block @click="cancelCrop">
            <template #icon><Dismiss24Regular class="button-icon" /></template>
            取消裁剪
          </a-button>
        </a-space>
      </div>

      <!-- 固定比例裁剪 -->
      <div v-else-if="currentTool === 'crop-ratio'" class="property-section">
        <div class="section-title">固定比例裁剪</div>
        <a-space direction="vertical" style="width: 100%">
          <div class="form-item">
            <label>裁剪比例</label>
            <a-select 
              v-model:value="cropRatio" 
              style="width: 100%"
              @change="handleCropRatioChange"
            >
              <a-select-option value="free">自由比例</a-select-option>
              <a-select-option value="1:1">1:1 (正方形)</a-select-option>
              <a-select-option value="4:3">4:3</a-select-option>
              <a-select-option value="16:9">16:9</a-select-option>
              <a-select-option value="3:2">3:2</a-select-option>
              <a-select-option value="custom">自定义</a-select-option>
            </a-select>
          </div>
          
          <div v-if="cropRatio === 'custom'" class="form-item">
            <label>自定义比例</label>
            <a-input-group compact>
              <a-input-number 
                v-model:value="customRatio.width" 
                :min="1" 
                style="width: 45%"
                placeholder="宽"
              />
              <a-input 
                style="width: 10%; text-align: center; pointer-events: none" 
                value=":" 
                disabled 
              />
              <a-input-number 
                v-model:value="customRatio.height" 
                :min="1" 
                style="width: 45%"
                placeholder="高"
              />
            </a-input-group>
          </div>
        </a-space>
      </div>

      <!-- 旋转工具 -->
      <div v-else-if="currentTool === 'rotate'" class="property-section">
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

      <!-- 翻转工具 -->
      <div v-else-if="currentTool === 'flip'" class="property-section">
        <div class="section-title">翻转</div>
        <a-space direction="vertical" style="width: 100%">
          <a-button block @click="flipHorizontal">
            <template #icon><ArrowSwap24Regular class="button-icon" /></template>
            水平翻转
          </a-button>
          <a-button block @click="flipVertical">
            <template #icon><ArrowSwap24Regular class="button-icon" style="transform: rotate(90deg)" /></template>
            垂直翻转
          </a-button>
        </a-space>
      </div>

      <!-- 文字工具 -->
      <div v-else-if="currentTool === 'text'" class="property-section">
        <div class="section-title">文字标注</div>
        <a-space direction="vertical" style="width: 100%">
          <div class="form-item">
            <label>文字内容</label>
            <a-textarea 
              v-model:value="textContent"
              placeholder="输入文字内容"
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

      <!-- 图形工具 -->
      <div v-else-if="['rectangle', 'circle', 'line', 'arrow'].includes(currentTool)" class="property-section">
        <div class="section-title">{{ getShapeTitle(currentTool) }}</div>
        <a-space direction="vertical" style="width: 100%">
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
          
          <div v-if="['rectangle', 'circle'].includes(currentTool)" class="form-item">
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
    </div>

    <!-- 底部操作区：将“清空”按钮移动到底部，避免被保存面板遮挡 -->
    <div class="panel-footer" v-if="currentTool === 'select'">
      <a-space direction="vertical" style="width: 100%">
        <a-button danger block @click="handleClear">
          <template #icon><Delete24Regular class="button-icon" /></template>
          清空
        </a-button>
      </a-space>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { message } from 'ant-design-vue'
import {
  Checkmark24Regular,
  Dismiss24Regular,
  ArrowSwap24Regular,
  Delete24Regular
} from '@vicons/fluent'
import SelectToolPanel from './SelectToolPanel.vue'

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
  }
})

// Emits
const emit = defineEmits(['options-change', 'image-change', 'clear'])

// 裁剪相关
const cropRatio = ref('free')
const customRatio = ref({ width: 1, height: 1 })

// 旋转相关
const rotateAngle = ref(0)

// 文字相关
const textContent = ref('')
const fontSize = ref(24)
const textColor = ref('#000000')
const textBold = ref(false)
const textItalic = ref(false)

// 图形相关
const strokeWidth = ref(2)
const strokeColor = ref('#000000')
const fillColor = ref('#ffffff')
const hasFill = ref(false)

// 监听属性变化并发送给父组件
watch([
  cropRatio, customRatio, rotateAngle, textContent, fontSize, textColor, 
  textBold, textItalic, strokeWidth, strokeColor, fillColor, hasFill
], () => {
  emit('options-change', {
    cropRatio: cropRatio.value,
    customRatio: customRatio.value,
    rotateAngle: rotateAngle.value,
    textContent: textContent.value,
    fontSize: fontSize.value,
    textColor: textColor.value,
    textBold: textBold.value,
    textItalic: textItalic.value,
    strokeWidth: strokeWidth.value,
    strokeColor: strokeColor.value,
    fillColor: fillColor.value,
    hasFill: hasFill.value
  })
}, { deep: true })

/**
 * 应用裁剪
 * 成功后通过 image-change 向父级回传新图像
 */
const applyCrop = async () => {
  if (!props.imageData) {
    message.warning('没有图像数据')
    return
  }

  try {
    // TODO: 获取裁剪区域坐标
    const cropParams = {
      x: 0, y: 0, width: 100, height: 100 // 临时值，需要从画布获取
    }

    const result = await window.electronAPI.python.execute('crop', {
      input: props.imageData.data,
      params: cropParams
    })

    if (result.success) {
      // 更新图像数据
      const newImageData = { ...props.imageData, ...result }
      emit('image-change', newImageData)
      message.success('裁剪成功')
    } else {
      message.error('裁剪失败: ' + (result.error || '未知错误'))
    }
  } catch (error) {
    message.error('裁剪失败: ' + error.message)
  }
}

/**
 * 取消裁剪，重置为选择工具
 */
const cancelCrop = () => {
  emit('options-change', { tool: 'select' })
}

/**
 * 处理裁剪比例变更
 */
const handleCropRatioChange = (value) => {
  cropRatio.value = value
}

/**
 * 按指定角度旋转
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
 */
const handleRotateChange = async (value) => {
  rotateAngle.value = value
  await rotate(value)
}

/**
 * 水平翻转
 */
const flipHorizontal = async () => {
  if (!props.imageData) {
    message.warning('没有图像数据')
    return
  }

  try {
    const result = await window.electronAPI.python.execute('flip_horizontal', {
      input: props.imageData.data
    })

    if (result.success) {
      const newImageData = { ...props.imageData, ...result }
      emit('image-change', newImageData)
      message.success('水平翻转成功')
    } else {
      message.error('翻转失败: ' + (result.error || '未知错误'))
    }
  } catch (error) {
    message.error('翻转失败: ' + error.message)
  }
}

/**
 * 垂直翻转
 */
const flipVertical = async () => {
  if (!props.imageData) {
    message.warning('没有图像数据')
    return
  }

  try {
    const result = await window.electronAPI.python.execute('flip_vertical', {
      input: props.imageData.data
    })

    if (result.success) {
      const newImageData = { ...props.imageData, ...result }
      emit('image-change', newImageData)
      message.success('垂直翻转成功')
    } else {
      message.error('翻转失败: ' + (result.error || '未知错误'))
    }
  } catch (error) {
    message.error('翻转失败: ' + error.message)
  }
}

/**
 * 根据工具返回标题
 */
const getShapeTitle = (tool) => {
  const titles = {
    rectangle: '矩形',
    circle: '圆形',
    line: '直线',
    arrow: '箭头'
  }
  return titles[tool] || '图形'
}

/**
 * 处理“清空”按钮点击：
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

/* 底部操作区域，避免被保存面板遮挡，保持舒适的内边距与分隔线 */
.panel-footer {
  padding: 12px 16px 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.06);
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
