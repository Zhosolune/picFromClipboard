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
import os
from io import BytesIO
from typing import Optional, Dict, Any, List, Union, Tuple
from PIL import Image, ImageDraw, ImageFont


class ImageProcessor:
    """图像处理器类
    
    提供完整的图像处理功能，包括基础操作、绘图功能和历史记录管理。
    """
    
    def __init__(self) -> None:
        """
        初始化图像处理器
        
        创建一个新的图像处理器实例，初始化图像对象和历史记录。
        
        异常：
            无
        """
        self.image: Optional[Image.Image] = None
        self.original_image: Optional[Image.Image] = None
        self.history: List[Image.Image] = []
        self.history_index: int = -1
    
    def load_from_base64(self, base64_data: str) -> bool:
        """
        从Base64数据加载图像
        
        解析Base64编码的图像数据并创建PIL图像对象，同时初始化历史记录。
        支持带有data URL前缀的Base64数据。
        
        参数：
            base64_data: Base64编码的图像数据，可包含data URL前缀
            
        返回：
            加载是否成功
            
        异常：
            ValueError: 当Base64数据格式无效时抛出
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
    
    def load_from_file(self, file_path: str) -> bool:
        """
        从文件加载图像
        
        从指定的文件路径加载图像，支持PIL支持的所有图像格式。
        
        参数：
            file_path: 图像文件的完整路径
            
        返回：
            加载是否成功
            
        异常：
            FileNotFoundError: 当文件不存在时抛出
            IOError: 当文件无法读取或格式不支持时抛出
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
    
    def crop(self, x: int, y: int, width: int, height: int) -> bool:
        """
        裁剪图像
        
        根据指定的坐标和尺寸裁剪图像。会自动调整裁剪区域以确保在图像边界内。
        
        参数：
            x: 裁剪区域左上角X坐标
            y: 裁剪区域左上角Y坐标
            width: 裁剪区域宽度
            height: 裁剪区域高度
            
        返回：
            操作是否成功
            
        异常：
            ValueError: 当坐标或尺寸参数无效时抛出
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
    
    def rotate(self, angle: float) -> bool:
        """
        旋转图像
        
        按指定角度旋转图像，使用白色背景填充空白区域。
        
        参数：
            angle: 旋转角度（度），正值为顺时针旋转
            
        返回：
            操作是否成功
            
        异常：
            ValueError: 当角度参数无效时抛出
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
    
    def flip_horizontal(self) -> bool:
        """
        水平翻转图像
        
        沿垂直轴翻转图像（左右镜像）。
        
        返回：
            操作是否成功
            
        异常：
            RuntimeError: 当图像处理失败时抛出
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
    
    def flip_vertical(self) -> bool:
        """
        垂直翻转图像
        
        沿水平轴翻转图像（上下镜像）。
        
        返回：
            操作是否成功
            
        异常：
            RuntimeError: 当图像处理失败时抛出
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
    
    def add_text(self, text: str, x: int, y: int, font_size: int = 24, 
                 color: str = 'black', font_path: Optional[str] = None) -> bool:
        """
        添加文字标注
        
        在图像的指定位置添加文字。支持自定义字体、大小和颜色。
        
        参数：
            text: 要添加的文字内容
            x: 文字位置X坐标
            y: 文字位置Y坐标
            font_size: 字体大小，默认24像素
            color: 文字颜色，支持颜色名称或十六进制值，默认黑色
            font_path: 字体文件路径，为None时使用系统默认字体
            
        返回：
            操作是否成功
            
        异常：
            ValueError: 当坐标或字体大小无效时抛出
            IOError: 当字体文件无法加载时抛出
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
    
    def draw_rectangle(self, x1: int, y1: int, x2: int, y2: int, 
                      outline_color: str = 'black', fill_color: Optional[str] = None, 
                      width: int = 2) -> bool:
        """
        绘制矩形
        
        在图像上绘制矩形，支持自定义边框和填充颜色。
        
        参数：
            x1: 矩形左上角X坐标
            y1: 矩形左上角Y坐标
            x2: 矩形右下角X坐标
            y2: 矩形右下角Y坐标
            outline_color: 边框颜色，支持颜色名称或十六进制值，默认黑色
            fill_color: 填充颜色，None表示不填充，默认None
            width: 边框宽度，默认2像素
            
        返回：
            操作是否成功
            
        异常：
            ValueError: 当坐标或宽度参数无效时抛出
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
    
    def draw_circle(self, x: int, y: int, radius: int, 
                   outline_color: str = 'black', fill_color: Optional[str] = None, 
                   width: int = 2) -> bool:
        """
        绘制圆形
        
        在图像上绘制圆形，支持自定义边框和填充颜色。
        
        参数：
            x: 圆心X坐标
            y: 圆心Y坐标
            radius: 圆的半径
            outline_color: 边框颜色，支持颜色名称或十六进制值，默认黑色
            fill_color: 填充颜色，None表示不填充，默认None
            width: 边框宽度，默认2像素
            
        返回：
            操作是否成功
            
        异常：
            ValueError: 当坐标、半径或宽度参数无效时抛出
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
    
    def draw_line(self, x1: int, y1: int, x2: int, y2: int, 
                 color: str = 'black', width: int = 2) -> bool:
        """
        绘制直线
        
        在图像上绘制从起点到终点的直线。
        
        参数：
            x1: 起点X坐标
            y1: 起点Y坐标
            x2: 终点X坐标
            y2: 终点Y坐标
            color: 线条颜色，支持颜色名称或十六进制值，默认黑色
            width: 线条宽度，默认2像素
            
        返回：
            操作是否成功
            
        异常：
            ValueError: 当坐标或宽度参数无效时抛出
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
    
    def save_to_file(self, file_path: str, format: str = 'PNG', quality: int = 95) -> bool:
        """
        保存图像到文件
        
        将当前图像保存到指定路径，支持多种图像格式。对于JPEG格式会自动处理透明度。
        
        参数：
            file_path: 保存文件的完整路径
            format: 图像格式（PNG、JPEG、BMP、GIF等），默认PNG
            quality: 图像质量，仅对JPEG格式有效，范围1-100，默认95
            
        返回：
            保存是否成功
            
        异常：
            IOError: 当文件无法写入时抛出
            ValueError: 当格式不支持或质量参数无效时抛出
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
    
    def to_base64(self, format: str = 'PNG', quality: int = 95) -> Optional[str]:
        """
        将图像转换为Base64字符串
        
        将当前图像编码为Base64格式的data URL，便于在Web环境中使用。
        
        参数：
            format: 图像格式（PNG、JPEG、BMP、GIF等），默认PNG
            quality: 图像质量，仅对JPEG格式有效，范围1-100，默认95
            
        返回：
            Base64编码的data URL字符串，失败时返回None
            
        异常：
            ValueError: 当格式不支持或质量参数无效时抛出
            MemoryError: 当图像过大无法编码时抛出
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
    
    def undo(self) -> bool:
        """
        撤销操作
        
        回退到历史记录中的上一个状态。
        
        返回：
            撤销是否成功，如果已经是最早状态则返回False
            
        异常：
            无
        """
        if self.history_index > 0:
            self.history_index -= 1
            self.image = self.history[self.history_index].copy()
            return True
        return False
    
    def redo(self) -> bool:
        """
        重做操作
        
        前进到历史记录中的下一个状态。
        
        返回：
            重做是否成功，如果已经是最新状态则返回False
            
        异常：
            无
        """
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.image = self.history[self.history_index].copy()
            return True
        return False
    
    def _add_to_history(self) -> None:
        """
        添加当前状态到历史记录
        
        将当前图像状态保存到历史记录中，用于撤销/重做功能。
        自动管理历史记录数量，最多保留20个状态。
        
        异常：
            无
        """
        if self.image is None:
            return
            
        # 移除当前位置之后的历史记录
        self.history = self.history[:self.history_index + 1]
        
        # 添加新状态
        self.history.append(self.image.copy())
        self.history_index += 1
        
        # 限制历史记录数量（最多保留20个状态）
        if len(self.history) > 20:
            self.history.pop(0)
            self.history_index -= 1
    
    def get_image_info(self) -> Optional[Dict[str, Any]]:
        """
        获取图像信息
        
        返回当前图像的基本信息，包括尺寸、颜色模式等。

        返回：
            包含图像信息的字典，如果没有加载图像则返回None
            字典包含以下键：
            - width: 图像宽度
            - height: 图像高度
            - mode: 颜色模式（RGB、RGBA等）
            - format: 原始文件格式
            - has_transparency: 是否包含透明度
            
        异常：
            无
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


def main() -> None:
    """
    命令行接口主函数
    
    提供命令行方式调用图像处理功能，支持多种操作命令。
    通过JSON格式的参数传递和结果返回，便于与Electron等前端框架集成。
    
    命令格式：
        python image_processor.py <command> --input <input> [options]
    
    支持的命令：
        crop: 裁剪图像
        rotate: 旋转图像  
        flip_horizontal: 水平翻转
        flip_vertical: 垂直翻转
        add_text: 添加文字标注
        draw_rectangle: 绘制矩形
        draw_circle: 绘制圆形
        draw_line: 绘制直线
        save: 保存图像
        info: 获取图像信息
        undo: 撤销操作
        redo: 重做操作
        
    异常：
        SystemExit: 当参数解析失败时退出
        Exception: 当命令执行失败时输出错误信息
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
    result: Dict[str, Any] = {}

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
