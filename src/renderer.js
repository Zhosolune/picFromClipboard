/**
 * 渲染进程入口文件
 *
 * 功能描述：
 * - 初始化Vue应用
 * - 配置Ant Design Vue
 * - 挂载应用到DOM
 *
 * @author AI Assistant
 * @version 1.0.0
 */

import { createApp } from 'vue'
import Antd from 'ant-design-vue'
import App from './App.vue'
import 'ant-design-vue/dist/reset.css'

// 创建Vue应用实例
const app = createApp(App)

// 使用Ant Design Vue
app.use(Antd)

// 挂载应用
app.mount('#app')

console.log('🎨 剪贴板图像处理工具已启动');
