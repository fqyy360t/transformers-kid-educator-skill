#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-2026 The Alibaba Wan Team Authors. All rights reserved.

"""
Wan 2.7 图片生成的分辨率解析工具

把用户写的分辨率描述转换成接口所需的 size 参数。

用法示例：
    python parse_resolution.py "2K 3:4"
    python parse_resolution.py "1K 16:9"
    python parse_resolution.py "2048*2048"
    python parse_resolution.py "1K"

输出：
    1536*2048
    1696*960
    2048*2048
    1024*1024

K 值加宽高比的写法：
`{K 值} {宽}:{高}`
| 输入 | 输出 | 说明 |
|------|------|------|
| `1K 1:1` | 1024*1024 | 1K 正方形 |
| `1K 3:4` | 896*1194 | 竖版 |
| `1K 4:3` | 1194*896 | 横版 |
| `1K 16:9` | 1364*768 | 宽屏 |
| `1K 9:16` | 768*1364 | 手机竖屏 |
| `2K 3:4` | 1774*2364 | 2K 竖版 |
| `2K 16:9` | 2730*1536 | 2K 宽屏 |
| `2K 1:1` | 2048*2048 | 2K 正方形 |
"""

import re
import sys
import argparse


def parse_resolution(input_str):
    """
    解析用户输入的分辨率描述
    
    参数：
        input_str：支持以下输入格式：
            - "2K 3:4"、"1K 16:9"（K 值加宽高比）
            - "2K"、"1K"（只给 K 值，默认 1:1）
            - "1280*1280"、"2048*2048"（直接指定分辨率，用 * 分隔）
            - "1280x1280"（直接指定分辨率，用 x 分隔）
    
    返回值：
        str：格式化后的分辨率字符串，例如 "1536*2048"
    
    可能抛出的异常：
        ValueError：输入格式不合法或超出范围
    """
    
    input_str = input_str.strip().lower()
    
    # 方式一：直接指定分辨率，例如 "1280*1280" 或 "1280x1280"
    direct_pattern = r'^(\d+)[*x](\d+)$'
    match = re.match(direct_pattern, input_str)
    if match:
        width = int(match.group(1))
        height = int(match.group(2))
        
        if not (768*768 <= width * height <= 2048*2048):
            raise ValueError(f"总像素数需在 [768*768, 2048*2048] 即 [{768*768}, {2048*2048}] 之间，当前为 {width}*{height}: {width*height}")
        
        aspect_ratio = width / height
        if not (1/8 <= aspect_ratio <= 8):
            raise ValueError(f"宽高比需在 [1:8, 8:1] 之间，当前为 {aspect_ratio:.2f}")
        
        return f"{width}*{height}"
    
    # 方式二：K 值加宽高比，例如 "2K 3:4"、"1K 16:9"
    k_ratio_pattern = r'^([124])k\s*(\d+):(\d+)$'
    match = re.match(k_ratio_pattern, input_str)
    if match:
        k_value = int(match.group(1))
        ratio_w = int(match.group(2))
        ratio_h = int(match.group(3))
        
        
        total_pixels = min(max((k_value * 1024) ** 2, 1024*1024), 2048*2048)
        base_unit = (total_pixels / (ratio_w * ratio_h)) ** 0.5
        width = int(round(base_unit * ratio_w))
        height = int(round(base_unit * ratio_h))

        # 保证是偶数，部分模型有此要求
        width = width if width % 2 == 0 else width - 1
        height = height if height % 2 == 0 else height - 1

        if not (768*768 <= width * height <= 2048*2048):
            raise ValueError(f"总像素数需在 [768*768, 2048*2048] 即 [{768*768}, {2048*2048}] 之间，算出的分辨率越界：{width}*{height}: {width*height}")
        
        aspect_ratio = width / height
        if not (1/8 <= aspect_ratio <= 8):
            raise ValueError(f"宽高比需在 [1:8, 8:1] 之间，当前为 {aspect_ratio:.2f}")
        
        return f"{width}*{height}"
    
    # 方式三：只给 K 值，例如 "1K"、"2K"，默认 1:1
    k_only_pattern = r'^([12])k$'
    match = re.match(k_only_pattern, input_str)
    if match:
        k_value = int(match.group(1))
        size = k_value * 1024
        return f"{size}*{size}"


    raise ValueError(
        f"不支持的输入格式：'{input_str}'\n"
        f"支持的输入格式：\n"
        f"  - K 值加宽高比：'2K 3:4'、'1K 16:9'、'2K 1:1'\n"
        f"  - 只给 K 值：'1K'、'2K'（默认 1:1）\n"
        f"  - 直接指定分辨率：'1280*1280'、'2048*2048'"
    )


def main():
    parser = argparse.ArgumentParser(
        description='解析分辨率描述，支持 K 值写法或具体像素写法',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例：
  python parse_resolution.py '2K 3:4'       # 输出：1536*2048
  python parse_resolution.py '1K 16:9'      # 输出：1696*960
  python parse_resolution.py '2048*2048'    # 输出：2048*2048
  python parse_resolution.py '1K'           # 输出：1024*1024
        '''.strip()
    )
    
    parser.add_argument(
        'input',
        help='分辨率描述，例如 "2K 3:4"、"2048*2048"、"1K"'
    )
    
    args = parser.parse_args()
    input_str = args.input
    
    try:
        result = parse_resolution(input_str)
        print(result)
    except ValueError as e:
        print(f"失败：{e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
