#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图像生成器

功能描述：
- 生成测试图像并复制到剪贴板
- 用于测试应用程序的剪贴板监控功能

作者：AI Assistant
版本：1.0.0
"""

from PIL import Image, ImageDraw, ImageFont
import io
import base64

def create_test_image():
    """
    创建测试图像
    
    返回：
        PIL.Image: 测试图像对象
    """
    # 创建一个彩色测试图像
    img = Image.new('RGB', (600, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # 绘制彩色背景渐变
    for i in range(400):
        color = (255 - i//2, i//2, 128)
        draw.line([(0, i), (600, i)], fill=color)
    
    # 绘制测试图形
    draw.rectangle([50, 50, 550, 350], outline='blue', width=5)
    draw.ellipse([100, 100, 500, 300], outline='red', width=3)
    draw.line([50, 50, 550, 350], fill='green', width=3)
    draw.line([550, 50, 50, 350], fill='green', width=3)
    
    # 添加文字
    try:
        # 尝试使用系统字体
        font = ImageFont.load_default()
        draw.text((200, 180), "测试图像", fill='black', font=font)
        draw.text((200, 200), "Test Image", fill='black', font=font)
    except:
        draw.text((200, 180), "测试图像", fill='black')
        draw.text((200, 200), "Test Image", fill='black')
    
    return img

def save_test_image():
    """
    保存测试图像到文件
    """
    img = create_test_image()
    img.save('test-image.png', 'PNG')
    print("测试图像已保存为 test-image.png")
    
    # 同时输出Base64数据
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    print(f"Base64数据长度: {len(base64_data)} 字符")
    print("Base64数据（前100字符）:", base64_data[:100] + "...")

if __name__ == '__main__':
    save_test_image()
