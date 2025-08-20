#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像处理器测试脚本

功能描述：
- 测试图像处理器的各项功能
- 验证命令行接口是否正常工作
- 生成测试图像用于验证

作者：AI Assistant
版本：1.0.0
"""

import os
import sys
import json
from PIL import Image, ImageDraw
from image_processor import ImageProcessor


def create_test_image():
    """
    创建测试图像
    
    返回：
        str: 测试图像的Base64数据
    """
    # 创建一个简单的测试图像
    img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # 绘制一些测试内容
    draw.rectangle([50, 50, 350, 250], outline='blue', width=3)
    draw.ellipse([100, 100, 300, 200], outline='red', width=2)
    draw.line([50, 50, 350, 250], fill='green', width=2)
    draw.line([350, 50, 50, 250], fill='green', width=2)
    
    # 转换为Base64
    from io import BytesIO
    import base64
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return f"data:image/png;base64,{base64_data}"


def test_basic_operations():
    """
    测试基础操作
    """
    print("=== 测试基础操作 ===")
    
    # 创建处理器
    processor = ImageProcessor()
    
    # 创建测试图像
    test_image_base64 = create_test_image()
    
    # 测试加载图像
    print("1. 测试加载图像...")
    success = processor.load_from_base64(test_image_base64)
    print(f"   加载结果: {'成功' if success else '失败'}")
    
    if not success:
        return False
    
    # 测试获取图像信息
    print("2. 测试获取图像信息...")
    info = processor.get_image_info()
    if info:
        print(f"   图像尺寸: {info['width']} x {info['height']}")
        print(f"   图像模式: {info['mode']}")
        print(f"   是否透明: {info['has_transparency']}")
    
    # 测试裁剪
    print("3. 测试裁剪...")
    success = processor.crop(50, 50, 200, 150)
    print(f"   裁剪结果: {'成功' if success else '失败'}")
    
    # 测试旋转
    print("4. 测试旋转...")
    success = processor.rotate(45)
    print(f"   旋转结果: {'成功' if success else '失败'}")
    
    # 测试翻转
    print("5. 测试水平翻转...")
    success = processor.flip_horizontal()
    print(f"   翻转结果: {'成功' if success else '失败'}")
    
    # 测试添加文字
    print("6. 测试添加文字...")
    success = processor.add_text("测试文字", 10, 10, 20, 'red')
    print(f"   文字添加结果: {'成功' if success else '失败'}")
    
    # 测试绘制矩形
    print("7. 测试绘制矩形...")
    success = processor.draw_rectangle(20, 20, 100, 80, 'blue', None, 2)
    print(f"   矩形绘制结果: {'成功' if success else '失败'}")
    
    # 测试撤销
    print("8. 测试撤销...")
    success = processor.undo()
    print(f"   撤销结果: {'成功' if success else '失败'}")
    
    # 测试重做
    print("9. 测试重做...")
    success = processor.redo()
    print(f"   重做结果: {'成功' if success else '失败'}")
    
    # 测试保存
    print("10. 测试保存...")
    output_path = os.path.join(os.path.dirname(__file__), 'test_output.png')
    success = processor.save_to_file(output_path, 'PNG')
    print(f"    保存结果: {'成功' if success else '失败'}")
    if success:
        print(f"    保存路径: {output_path}")
    
    return True


def test_command_line_interface():
    """
    测试命令行接口
    """
    print("\n=== 测试命令行接口 ===")
    
    # 创建测试图像
    test_image_base64 = create_test_image()
    
    # 测试获取图像信息
    print("1. 测试获取图像信息命令...")
    import subprocess
    
    try:
        result = subprocess.run([
            sys.executable, 'image_processor.py', 'info',
            '--input', test_image_base64
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            print(f"   命令执行成功: {response}")
        else:
            print(f"   命令执行失败: {result.stderr}")
    except Exception as e:
        print(f"   命令执行异常: {e}")
    
    # 测试裁剪命令
    print("2. 测试裁剪命令...")
    try:
        params = json.dumps({'x': 50, 'y': 50, 'width': 200, 'height': 150})
        result = subprocess.run([
            sys.executable, 'image_processor.py', 'crop',
            '--input', test_image_base64,
            '--params', params
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            print(f"   裁剪命令成功: {response.get('success', False)}")
        else:
            print(f"   裁剪命令失败: {result.stderr}")
    except Exception as e:
        print(f"   裁剪命令异常: {e}")


def main():
    """
    主测试函数
    """
    print("开始测试图像处理器...")
    
    try:
        # 测试基础操作
        success = test_basic_operations()
        
        if success:
            # 测试命令行接口
            test_command_line_interface()
        
        print("\n测试完成！")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
