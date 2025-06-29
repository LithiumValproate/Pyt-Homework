#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import requests
import time
import math
from PIL import Image
from io import BytesIO
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# 定义常量
CSV_FILE = "2025.csv"
OUTPUT_DIR = "album_covers"
COLLAGE_FILENAME = "album_collage.jpg"
MAX_WORKERS = 10  # 并发下载的最大线程数
GRID_SIZE = None  # 自动计算网格大小


def create_output_dir():
    """创建输出目录"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    print(f"输出目录: {OUTPUT_DIR}")


def get_album_cover(apple_id, artist, album, retries=3):
    """获取专辑封面"""
    filename = f"{OUTPUT_DIR}/{apple_id}.jpg"

    # 如果已经下载过，直接返回文件路径
    if os.path.exists(filename):
        return filename

    # 构建iTunes API URL
    url = f"https://itunes.apple.com/lookup?id={apple_id}&entity=album"

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data["resultCount"] > 0:
                    # 获取高质量的专辑封面URL (替换尺寸为600x600)
                    artwork_url = data["results"][0].get("artworkUrl100", "")
                    if artwork_url:
                        artwork_url = artwork_url.replace("100x100", "600x600")
                        # 下载封面图片
                        img_response = requests.get(artwork_url, timeout=10)
                        if img_response.status_code == 200:
                            # 保存图片
                            with open(filename, "wb") as f:
                                f.write(img_response.content)
                            print(f"已下载: {artist} - {album}")
                            return filename

            # 如果没有找到或下载失败
            print(f"尝试 {attempt+1}/{retries}: 无法获取 {artist} - {album} 的封面")
            time.sleep(1)  # 等待一秒后重试

        except Exception as e:
            print(f"错误: {e} - {artist} - {album}")
            time.sleep(1)

    # 所有重试都失败了，返回None
    return None


def download_all_covers(csv_file):
    """从CSV文件下载所有专辑封面"""
    df = pd.read_csv(csv_file)

    # 去重，只保留唯一的专辑
    unique_albums = df[["Artist name", "Album", "Apple - id"]].drop_duplicates()
    total = len(unique_albums)
    print(f"发现 {total} 张唯一专辑")

    cover_paths = []

    # 使用线程池并行下载
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for _, row in unique_albums.iterrows():
            apple_id = row["Apple - id"]
            artist = row["Artist name"]
            album = row["Album"]
            futures.append(
                executor.submit(get_album_cover, apple_id, artist, album)
            )

        # 收集结果
        for future in futures:
            result = future.result()
            if result:
                cover_paths.append(result)

    print(f"成功下载 {len(cover_paths)}/{total} 张专辑封面")
    return cover_paths


def create_collage(image_paths):
    """创建拼贴图"""
    if not image_paths:
        print("没有可用的封面图片")
        return

    # 计算最佳网格大小
    n = len(image_paths)
    if GRID_SIZE:
        cols, rows = GRID_SIZE
    else:
        cols = math.ceil(math.sqrt(n))
        rows = math.ceil(n / cols)

    print(f"创建 {cols}x{rows} 的拼贴图")

    # 封面图片的标准大小
    thumb_size = 300

    # 创建空白画布
    collage = Image.new('RGB', (thumb_size * cols, thumb_size * rows))

    # 填充拼贴图
    for i, img_path in enumerate(image_paths):
        if i >= cols * rows:
            break

        try:
            img = Image.open(img_path)
            # 调整大小并保持纵横比
            img.thumbnail((thumb_size, thumb_size))

            # 计算位置
            x = (i % cols) * thumb_size
            y = (i // cols) * thumb_size

            # 如果图片小于缩略图大小，居中放置
            x_offset = (thumb_size - img.width) // 2
            y_offset = (thumb_size - img.height) // 2

            # 粘贴到拼贴图上
            collage.paste(img, (x + x_offset, y + y_offset))

        except Exception as e:
            print(f"无法处理图片 {img_path}: {e}")

    # 保存拼贴图
    collage.save(COLLAGE_FILENAME)
    print(f"拼贴图已保存为: {COLLAGE_FILENAME}")

    return COLLAGE_FILENAME


def main():
    """主函数"""
    print("开始处理专辑封面")

    # 确保输出目录存在
    create_output_dir()

    # 下载所有封面
    cover_paths = download_all_covers(CSV_FILE)

    # 创建拼贴图
    if cover_paths:
        collage_path = create_collage(cover_paths)
        print(f"完成! 拼贴图已保存为: {collage_path}")
    else:
        print("无法创建拼贴图，因为没有下载到封面图片")


if __name__ == "__main__":
    main()
