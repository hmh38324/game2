#!/usr/bin/env python3
"""
验证分割后的图片是否正确对应到4x4网格
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_test_grid():
    # 创建card_backgrounds文件夹
    card_bg_dir = '/Users/apple/Documents/cursor/game2/card_backgrounds'
    
    # 创建一个测试图片来验证分割
    test_img = Image.new('RGB', (924, 924), (255, 255, 255))
    draw = ImageDraw.Draw(test_img)
    
    # 绘制网格线
    for i in range(5):
        x = i * 231
        y = i * 231
        draw.line([(x, 0), (x, 924)], fill=(0, 0, 0), width=2)
        draw.line([(0, y), (924, y)], fill=(0, 0, 0), width=2)
    
    # 在每个格子中写入坐标
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    for row in range(4):
        for col in range(4):
            x = col * 231 + 115  # 居中
            y = row * 231 + 115
            text = f"({row},{col})"
            draw.text((x-30, y-10), text, fill=(255, 0, 0), font=font)
    
    # 保存测试图片
    test_img.save('/Users/apple/Documents/cursor/game2/test_grid.png')
    print("已创建测试网格图片: test_grid.png")
    
    # 验证每个分割图片
    print("\n验证分割图片:")
    for row in range(4):
        for col in range(4):
            filename = f'card_bg_{row}_{col}.png'
            filepath = os.path.join(card_bg_dir, filename)
            if os.path.exists(filepath):
                img = Image.open(filepath)
                print(f"{filename}: {img.size}")
            else:
                print(f"{filename}: 文件不存在")

if __name__ == "__main__":
    create_test_grid()
