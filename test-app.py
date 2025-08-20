#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用程序测试脚本

功能描述：
- 生成测试图像并复制到剪贴板
- 测试应用程序的剪贴板监控功能
- 验证图像处理功能

作者：AI Assistant
版本：1.0.0
"""

import sys
import time
from PIL import Image, ImageDraw, ImageFont
import io

def create_test_image():
    """
    创建测试图像
    
    返回：
        PIL.Image: 测试图像对象
    """
    # 创建一个彩色测试图像
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # 绘制彩色背景
    for i in range(600):
        color = (255 - i//3, i//3, 128 + i//5)
        draw.line([(0, i), (800, i)], fill=color)
    
    # 绘制测试图形
    draw.rectangle([100, 100, 700, 500], outline='blue', width=8)
    draw.ellipse([200, 200, 600, 400], outline='red', width=5)
    draw.line([100, 100, 700, 500], fill='green', width=4)
    draw.line([700, 100, 100, 500], fill='green', width=4)
    
    # 添加文字
    try:
        font = ImageFont.load_default()
        draw.text((300, 280), "剪贴板图像处理工具", fill='black', font=font)
        draw.text((320, 300), "Clipboard Image Tool", fill='black', font=font)
        draw.text((350, 320), "测试图像", fill='blue', font=font)
    except:
        draw.text((300, 280), "剪贴板图像处理工具", fill='black')
        draw.text((320, 300), "Clipboard Image Tool", fill='black')
        draw.text((350, 320), "测试图像", fill='blue')
    
    return img

def copy_to_clipboard():
    """
    将测试图像复制到剪贴板
    """
    try:
        import win32clipboard
        from PIL import ImageWin
        
        img = create_test_image()
        
        # 将图像复制到剪贴板
        output = io.BytesIO()
        img.convert('RGB').save(output, 'BMP')
        data = output.getvalue()[14:]  # 移除BMP文件头
        output.close()
        
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        
        print("✅ 测试图像已复制到剪贴板")
        print("📱 请检查应用程序是否检测到图像")
        
    except ImportError:
        print("❌ 需要安装 pywin32 库来操作剪贴板")
        print("   运行: pip install pywin32")
        
        # 降级方案：保存图像文件
        img = create_test_image()
        img.save('test-clipboard-image.png', 'PNG')
        print("💾 测试图像已保存为 test-clipboard-image.png")
        print("📋 请手动复制此图像到剪贴板进行测试")
        
    except Exception as e:
        print(f"❌ 复制到剪贴板失败: {e}")
        
        # 降级方案：保存图像文件
        img = create_test_image()
        img.save('test-clipboard-image.png', 'PNG')
        print("💾 测试图像已保存为 test-clipboard-image.png")
        print("📋 请手动复制此图像到剪贴板进行测试")

def main():
    """
    主测试函数
    """
    print("🚀 开始测试剪贴板图像处理工具...")
    print()
    
    print("1. 生成测试图像...")
    img = create_test_image()
    print(f"   ✅ 测试图像创建成功: {img.size[0]} x {img.size[1]} 像素")
    
    print()
    print("2. 复制图像到剪贴板...")
    copy_to_clipboard()
    
    print()
    print("3. 测试说明:")
    print("   - 应用程序应该自动检测到剪贴板中的图像")
    print("   - 图像应该显示在应用程序的预览区域")
    print("   - 可以使用工具栏中的各种工具编辑图像")
    print("   - 可以在底部面板保存处理后的图像")
    
    print()
    print("4. 功能测试建议:")
    print("   ✓ 测试图像预览和缩放")
    print("   ✓ 测试裁剪工具")
    print("   ✓ 测试旋转和翻转")
    print("   ✓ 测试文字标注")
    print("   ✓ 测试图形绘制")
    print("   ✓ 测试保存功能")
    
    print()
    print("🎉 测试准备完成！请在应用程序中验证功能。")

if __name__ == '__main__':
    main()
