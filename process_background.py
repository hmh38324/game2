#!/usr/bin/env python3
"""
将background.png处理成16个正方形背景，用作4x4卡牌的背景
"""

from PIL import Image
import os

def process_background():
    # 读取原始图片
    img = Image.open('background.png')
    print(f"原始图片尺寸: {img.size}")
    
    # 获取原始尺寸
    width, height = img.size
    
    # 计算正方形尺寸（使用较小的边作为正方形边长）
    square_size = min(width, height)
    
    # 创建正方形图片（上下扩展）
    square_img = Image.new('RGBA', (square_size, square_size), (0, 0, 0, 0))
    
    # 计算粘贴位置（居中）
    paste_x = (square_size - width) // 2
    paste_y = (square_size - height) // 2
    
    # 将原始图片粘贴到正方形中心
    square_img.paste(img, (paste_x, paste_y))
    
    print(f"正方形图片尺寸: {square_img.size}")
    
    # 计算每个小正方形的尺寸
    small_size = square_size // 4
    
    # 创建card_backgrounds目录
    os.makedirs('card_backgrounds', exist_ok=True)
    
    # 分割成16个小正方形
    for row in range(4):
        for col in range(4):
            # 计算裁剪区域
            left = col * small_size
            top = row * small_size
            right = left + small_size
            bottom = top + small_size
            
            # 裁剪小正方形
            small_square = square_img.crop((left, top, right, bottom))
            
            # 保存文件
            filename = f'card_backgrounds/card_bg_{row}_{col}.png'
            small_square.save(filename)
            print(f"保存: {filename}")
    
    print("处理完成！生成了16个卡片背景文件。")

if __name__ == "__main__":
    process_background()
