#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像处理核心模块

功能描述：
- 提供图像裁剪、旋转、翻转等基础操作
- 支持文字标注和图形绘制
- 提供多种图像格式的保存功能
- 命令行接口供Electron调用

作者：AI Assistant
版本：1.0.0
"""

import sys
import json
import base64
import argparse
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os


class ImageProcessor:
    """图像处理器类"""
    
    def __init__(self):
        """
        初始化图像处理器
        """
        self.image = None
        self.original_image = None
        self.history = []
        self.history_index = -1
    
    def load_from_base64(self, base64_data):
        """
        从Base64数据加载图像
        
        参数：
            base64_data (str): Base64编码的图像数据
            
        返回：
            bool: 加载是否成功
            
        异常：
            ValueError: 当Base64数据无效时抛出
            IOError: 当图像数据无法解析时抛出
        """
        try:
            # 移除data URL前缀（如果存在）
            if base64_data.startswith('data:image/'):
                base64_data = base64_data.split(',')[1]
            
            # 解码Base64数据
            image_data = base64.b64decode(base64_data)
            
            # 创建PIL图像对象
            self.image = Image.open(BytesIO(image_data))
            self.original_image = self.image.copy()
            
            # 初始化历史记录
            self.history = [self.image.copy()]
            self.history_index = 0
            
            return True
            
        except Exception as e:
            print(f"加载图像失败: {e}", file=sys.stderr)
            return False
    
    def load_from_file(self, file_path):
        """
        从文件加载图像
        
        参数：
            file_path (str): 图像文件路径
            
        返回：
            bool: 加载是否成功
        """
        try:
            self.image = Image.open(file_path)
            self.original_image = self.image.copy()
            
            # 初始化历史记录
            self.history = [self.image.copy()]
            self.history_index = 0
            
            return True
            
        except Exception as e:
            print(f"加载图像文件失败: {e}", file=sys.stderr)
            return False
    
    def crop(self, x, y, width, height):
        """
        裁剪图像
        
        参数：
            x (int): 裁剪区域左上角X坐标
            y (int): 裁剪区域左上角Y坐标
            width (int): 裁剪区域宽度
            height (int): 裁剪区域高度
            
        返回：
            bool: 操作是否成功
        """
        try:
            if not self.image:
                return False
            
            # 确保裁剪区域在图像范围内
            img_width, img_height = self.image.size
            x = max(0, min(x, img_width))
            y = max(0, min(y, img_height))
            width = min(width, img_width - x)
            height = min(height, img_height - y)
            
            # 执行裁剪
            crop_box = (x, y, x + width, y + height)
            self.image = self.image.crop(crop_box)
            
            # 添加到历史记录
            self._add_to_history()
            
            return True
            
        except Exception as e:
            print(f"裁剪图像失败: {e}", file=sys.stderr)
            return False
    
    def rotate(self, angle):
        """
        旋转图像
        
        参数：
            angle (float): 旋转角度（度），正值为顺时针
            
        返回：
            bool: 操作是否成功
        """
        try:
            if not self.image:
                return False
            
            # 执行旋转，使用白色背景填充
            self.image = self.image.rotate(-angle, expand=True, fillcolor='white')
            
            # 添加到历史记录
            self._add_to_history()
            
            return True
            
        except Exception as e:
            print(f"旋转图像失败: {e}", file=sys.stderr)
            return False
    
    def flip_horizontal(self):
        """
        水平翻转图像
        
        返回：
            bool: 操作是否成功
        """
        try:
            if not self.image:
                return False
            
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            
            # 添加到历史记录
            self._add_to_history()
            
            return True
            
        except Exception as e:
            print(f"水平翻转失败: {e}", file=sys.stderr)
            return False
    
    def flip_vertical(self):
        """
        垂直翻转图像
        
        返回：
            bool: 操作是否成功
        """
        try:
            if not self.image:
                return False
            
            self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
            
            # 添加到历史记录
            self._add_to_history()
            
            return True
            
        except Exception as e:
            print(f"垂直翻转失败: {e}", file=sys.stderr)
            return False
    
    def add_text(self, text, x, y, font_size=24, color='black', font_path=None):
        """
        添加文字标注
        
        参数：
            text (str): 要添加的文字
            x (int): 文字位置X坐标
            y (int): 文字位置Y坐标
            font_size (int): 字体大小，默认24
            color (str): 文字颜色，默认黑色
            font_path (str): 字体文件路径，可选
            
        返回：
            bool: 操作是否成功
        """
        try:
            if not self.image:
                return False
            
            # 创建绘图对象
            draw = ImageDraw.Draw(self.image)
            
            # 加载字体
            try:
                if font_path and os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    # 尝试使用系统默认字体
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # 绘制文字
            draw.text((x, y), text, fill=color, font=font)
            
            # 添加到历史记录
            self._add_to_history()
            
            return True
            
        except Exception as e:
            print(f"添加文字失败: {e}", file=sys.stderr)
            return False
    
    def draw_rectangle(self, x1, y1, x2, y2, outline_color='black', fill_color=None, width=2):
        """
        绘制矩形
        
        参数：
            x1, y1 (int): 矩形左上角坐标
            x2, y2 (int): 矩形右下角坐标
            outline_color (str): 边框颜色，默认黑色
            fill_color (str): 填充颜色，None表示不填充
            width (int): 边框宽度，默认2
            
        返回：
            bool: 操作是否成功
        """
        try:
            if not self.image:
                return False
            
            draw = ImageDraw.Draw(self.image)
            draw.rectangle([x1, y1, x2, y2], outline=outline_color, fill=fill_color, width=width)
            
            # 添加到历史记录
            self._add_to_history()
            
            return True
            
        except Exception as e:
            print(f"绘制矩形失败: {e}", file=sys.stderr)
            return False
    
    def draw_circle(self, x, y, radius, outline_color='black', fill_color=None, width=2):
        """
        绘制圆形
        
        参数：
            x, y (int): 圆心坐标
            radius (int): 半径
            outline_color (str): 边框颜色，默认黑色
            fill_color (str): 填充颜色，None表示不填充
            width (int): 边框宽度，默认2
            
        返回：
            bool: 操作是否成功
        """
        try:
            if not self.image:
                return False
            
            draw = ImageDraw.Draw(self.image)
            bbox = [x - radius, y - radius, x + radius, y + radius]
            draw.ellipse(bbox, outline=outline_color, fill=fill_color, width=width)
            
            # 添加到历史记录
            self._add_to_history()
            
            return True
            
        except Exception as e:
            print(f"绘制圆形失败: {e}", file=sys.stderr)
            return False
    
    def draw_line(self, x1, y1, x2, y2, color='black', width=2):
        """
        绘制直线
        
        参数：
            x1, y1 (int): 起点坐标
            x2, y2 (int): 终点坐标
            color (str): 线条颜色，默认黑色
            width (int): 线条宽度，默认2
            
        返回：
            bool: 操作是否成功
        """
        try:
            if not self.image:
                return False
            
            draw = ImageDraw.Draw(self.image)
            draw.line([x1, y1, x2, y2], fill=color, width=width)
            
            # 添加到历史记录
            self._add_to_history()
            
            return True
            
        except Exception as e:
            print(f"绘制直线失败: {e}", file=sys.stderr)
            return False
    
    def save_to_file(self, file_path, format='PNG', quality=95):
        """
        保存图像到文件
        
        参数：
            file_path (str): 保存路径
            format (str): 图像格式，默认PNG
            quality (int): 图像质量（仅对JPEG有效），默认95
            
        返回：
            bool: 保存是否成功
        """
        try:
            if not self.image:
                return False
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 保存图像
            if format.upper() == 'JPEG' or format.upper() == 'JPG':
                # JPEG不支持透明度，需要转换为RGB
                if self.image.mode in ('RGBA', 'LA', 'P'):
                    rgb_image = Image.new('RGB', self.image.size, (255, 255, 255))
                    rgb_image.paste(self.image, mask=self.image.split()[-1] if self.image.mode == 'RGBA' else None)
                    rgb_image.save(file_path, format='JPEG', quality=quality)
                else:
                    self.image.save(file_path, format='JPEG', quality=quality)
            else:
                self.image.save(file_path, format=format)
            
            return True
            
        except Exception as e:
            print(f"保存图像失败: {e}", file=sys.stderr)
            return False
    
    def to_base64(self, format='PNG', quality=95):
        """
        将图像转换为Base64字符串
        
        参数：
            format (str): 图像格式，默认PNG
            quality (int): 图像质量（仅对JPEG有效），默认95
            
        返回：
            str: Base64编码的图像数据，失败时返回None
        """
        try:
            if not self.image:
                return None
            
            buffer = BytesIO()
            
            if format.upper() == 'JPEG' or format.upper() == 'JPG':
                # JPEG不支持透明度，需要转换为RGB
                if self.image.mode in ('RGBA', 'LA', 'P'):
                    rgb_image = Image.new('RGB', self.image.size, (255, 255, 255))
                    rgb_image.paste(self.image, mask=self.image.split()[-1] if self.image.mode == 'RGBA' else None)
                    rgb_image.save(buffer, format='JPEG', quality=quality)
                else:
                    self.image.save(buffer, format='JPEG', quality=quality)
            else:
                self.image.save(buffer, format=format)
            
            buffer.seek(0)
            base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return f"data:image/{format.lower()};base64,{base64_data}"
            
        except Exception as e:
            print(f"转换为Base64失败: {e}", file=sys.stderr)
            return None
    
    def undo(self):
        """
        撤销操作
        
        返回：
            bool: 撤销是否成功
        """
        if self.history_index > 0:
            self.history_index -= 1
            self.image = self.history[self.history_index].copy()
            return True
        return False
    
    def redo(self):
        """
        重做操作
        
        返回：
            bool: 重做是否成功
        """
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.image = self.history[self.history_index].copy()
            return True
        return False
    
    def _add_to_history(self):
        """
        添加当前状态到历史记录
        """
        # 移除当前位置之后的历史记录
        self.history = self.history[:self.history_index + 1]
        
        # 添加新状态
        self.history.append(self.image.copy())
        self.history_index += 1
        
        # 限制历史记录数量（最多保留20个状态）
        if len(self.history) > 20:
            self.history.pop(0)
            self.history_index -= 1
    
    def get_image_info(self):
        """
        获取图像信息

        返回：
            dict: 包含图像信息的字典
        """
        if not self.image:
            return None

        return {
            'width': self.image.width,
            'height': self.image.height,
            'mode': self.image.mode,
            'format': self.image.format,
            'has_transparency': self.image.mode in ('RGBA', 'LA', 'P')
        }


def main():
    """
    命令行接口主函数
    """
    parser = argparse.ArgumentParser(description='图像处理工具')
    parser.add_argument('command', help='操作命令')
    parser.add_argument('--input', help='输入图像（Base64或文件路径）')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--format', default='PNG', help='输出格式')
    parser.add_argument('--quality', type=int, default=95, help='图像质量（JPEG）')
    parser.add_argument('--params', help='操作参数（JSON格式）')

    args = parser.parse_args()

    # 创建图像处理器
    processor = ImageProcessor()

    # 加载图像
    if args.input:
        if os.path.exists(args.input):
            success = processor.load_from_file(args.input)
        else:
            success = processor.load_from_base64(args.input)

        if not success:
            print(json.dumps({'success': False, 'error': '加载图像失败'}))
            return

    # 解析参数
    params = {}
    if args.params:
        try:
            params = json.loads(args.params)
        except:
            print(json.dumps({'success': False, 'error': '参数格式错误'}))
            return

    # 执行命令
    success = False
    result = {}

    try:
        if args.command == 'crop':
            success = processor.crop(
                params.get('x', 0),
                params.get('y', 0),
                params.get('width', 100),
                params.get('height', 100)
            )
        elif args.command == 'rotate':
            success = processor.rotate(params.get('angle', 0))
        elif args.command == 'flip_horizontal':
            success = processor.flip_horizontal()
        elif args.command == 'flip_vertical':
            success = processor.flip_vertical()
        elif args.command == 'add_text':
            success = processor.add_text(
                params.get('text', ''),
                params.get('x', 0),
                params.get('y', 0),
                params.get('font_size', 24),
                params.get('color', 'black'),
                params.get('font_path')
            )
        elif args.command == 'draw_rectangle':
            success = processor.draw_rectangle(
                params.get('x1', 0),
                params.get('y1', 0),
                params.get('x2', 100),
                params.get('y2', 100),
                params.get('outline_color', 'black'),
                params.get('fill_color'),
                params.get('width', 2)
            )
        elif args.command == 'draw_circle':
            success = processor.draw_circle(
                params.get('x', 50),
                params.get('y', 50),
                params.get('radius', 25),
                params.get('outline_color', 'black'),
                params.get('fill_color'),
                params.get('width', 2)
            )
        elif args.command == 'draw_line':
            success = processor.draw_line(
                params.get('x1', 0),
                params.get('y1', 0),
                params.get('x2', 100),
                params.get('y2', 100),
                params.get('color', 'black'),
                params.get('width', 2)
            )
        elif args.command == 'save':
            if args.output:
                success = processor.save_to_file(args.output, args.format, args.quality)
            else:
                base64_data = processor.to_base64(args.format, args.quality)
                if base64_data:
                    result['base64'] = base64_data
                    success = True
        elif args.command == 'info':
            info = processor.get_image_info()
            if info:
                result.update(info)
                success = True
        elif args.command == 'undo':
            success = processor.undo()
        elif args.command == 'redo':
            success = processor.redo()
        else:
            print(json.dumps({'success': False, 'error': f'未知命令: {args.command}'}))
            return

        # 返回结果
        result['success'] = success
        if success and args.command != 'save' and args.command != 'info':
            # 返回处理后的图像信息
            info = processor.get_image_info()
            if info:
                result.update(info)

        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({'success': False, 'error': str(e)}))


if __name__ == '__main__':
    main()
