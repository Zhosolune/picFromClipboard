/**
 * 剪贴板监控工具
 *
 * 功能描述：
 * - 实时监控剪贴板内容变化
 * - 检测图像数据并触发回调
 * - 支持常见图像格式（PNG、JPG、BMP、GIF等）
 *
 * @author AI Assistant
 * @version 1.0.0
 */

import { ref } from "vue";

// 监控状态
const isMonitoring = ref(false);
let monitoringInterval = null;
let lastClipboardTimestamp = null;

/**
 * 开始监控剪贴板
 *
 * @param {Function} onImageDetected - 检测到图像时的回调函数
 * @param {number} interval - 监控间隔（毫秒），默认500ms
 */
export function useClipboard() {
  const startMonitoring = (onImageDetected, interval = 500) => {
    if (isMonitoring.value) {
      console.warn("剪贴板监控已在运行中");
      return;
    }

    isMonitoring.value = true;
    console.log("开始监控剪贴板...");

    monitoringInterval = setInterval(async () => {
      try {
        await checkClipboard(onImageDetected);
      } catch (error) {
        console.error("剪贴板检查失败:", error);
      }
    }, interval);
  };

  /**
   * 停止监控剪贴板
   */
  const stopMonitoring = () => {
    if (!isMonitoring.value) {
      return;
    }

    isMonitoring.value = false;
    if (monitoringInterval) {
      clearInterval(monitoringInterval);
      monitoringInterval = null;
    }
    console.log("停止监控剪贴板");
  };

  /**
   * 检查剪贴板内容
   *
   * @param {Function} onImageDetected - 检测到图像时的回调函数
   */
  const checkClipboard = async (onImageDetected) => {
    try {
      // 优先使用Electron的clipboard API
      if (window.electronAPI && window.electronAPI.clipboard) {
        const clipboardData = await window.electronAPI.clipboard.readImage();

        if (
          clipboardData &&
          clipboardData.timestamp !== lastClipboardTimestamp
        ) {
          lastClipboardTimestamp = clipboardData.timestamp;

          console.log("检测到剪贴板图像:", clipboardData);
          onImageDetected(clipboardData);
        }
      } else {
        // 在Electron环境中，如果electronAPI不可用，则跳过浏览器clipboard检查
        // 因为浏览器clipboard API在Electron中可能不稳定
        console.warn("Electron clipboard API不可用，跳过剪贴板检查");
      }
    } catch (error) {
      console.error("读取剪贴板失败:", error);
    }
  };

  return { startMonitoring, stopMonitoring };
}

/**
 * 读取剪贴板图像
 *
 * @returns {Promise<Object|null>} 剪贴板图像数据或null
 */
export async function readClipboardImage() {
  try {
    if (window.electronAPI && window.electronAPI.clipboard) {
      const clipboardData = await window.electronAPI.clipboard.readImage();
      return clipboardData;
    } else {
      console.warn("Electron clipboard API不可用");
      return null;
    }
  } catch (error) {
    console.error("读取剪贴板失败:", error);
    throw error;
  }
}

/**
 * 清空剪贴板
 * @returns {Promise<boolean>} 清空是否成功
 */
export const clearClipboard = async () => {
  try {
    if (window.electronAPI && window.electronAPI.clipboard) {
      return await window.electronAPI.clipboard.clear();
    } else {
      console.warn("Electron API 不可用，无法清空剪贴板");
      return false;
    }
  } catch (error) {
    console.error("清空剪贴板失败:", error);
    return false;
  }
};
