#!/usr/bin/env python3
"""
将background.png扩展为正方形，然后分成16份作为卡牌背面
"""

from PIL import Image
import os

def split_background():
    # 读取原始图片
    background_path = '/Users/apple/Documents/cursor/game2/background.png'
    
    if not os.path.exists(background_path):
        print(f"错误：找不到文件 {background_path}")
        return
    
    # 打开图片
    img = Image.open(background_path)
    original_width, original_height = img.size
    print(f"原始图片尺寸: {original_width}x{original_height}")
    
    # 计算正方形尺寸（取较大的边）
    square_size = max(original_width, original_height)
    print(f"正方形尺寸: {square_size}x{square_size}")
    
    # 创建正方形画布
    square_img = Image.new('RGBA', (square_size, square_size), (0, 0, 0, 0))
    
    # 将原图居中放置
    x_offset = (square_size - original_width) // 2
    y_offset = (square_size - original_height) // 2
    square_img.paste(img, (x_offset, y_offset))
    
    # 保存正方形图片
    square_img.save('/Users/apple/Documents/cursor/game2/background_square.png')
    print("已保存正方形图片: background_square.png")
    
    # 创建card_backgrounds文件夹
    card_bg_dir = '/Users/apple/Documents/cursor/game2/card_backgrounds'
    os.makedirs(card_bg_dir, exist_ok=True)
    
    # 计算每个小块的尺寸
    piece_size = square_size // 4
    print(f"每个小块尺寸: {piece_size}x{piece_size}")
    
    # 分割成16个小块
    for row in range(4):
        for col in range(4):
            # 计算裁剪区域
            left = col * piece_size
            top = row * piece_size
            right = left + piece_size
            bottom = top + piece_size
            
            # 裁剪小块
            piece = square_img.crop((left, top, right, bottom))
            
            # 保存小块
            filename = f'card_bg_{row}_{col}.png'
            piece.save(os.path.join(card_bg_dir, filename))
            print(f"已保存: {filename} (位置: 行{row}, 列{col}, 裁剪区域: {left},{top},{right},{bottom})")
    
    print(f"完成！已将背景图片分割成16个小块，保存在 {card_bg_dir} 文件夹中")

if __name__ == "__main__":
    split_background()
