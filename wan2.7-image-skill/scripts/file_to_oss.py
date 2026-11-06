#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-2026 The Alibaba Wan Team Authors. All rights reserved.

"""
上传文件到对象存储 —— 文件上传工具

把本地文件或 base64 图片数据上传到临时对象存储，换取一个 oss:// 地址。

适用场景：
- 为图生图、图像编辑或组图生成上传参考图
- 任何需要把本地文件、base64 数据作为模型输入的场景

用法：
    # 方式一：按文件路径上传
    python file_to_oss.py --file /path/to/image.jpg --model wan2.7-image
    
    # 方式二：上传 base64 数据
    python file_to_oss.py --base64 "<base64_data>" --model wan2.7-image

输出示例：
    oss://dashscope-instant/xxx/2024-07-18/xxx/cat.png

环境变量：
    DASHSCOPE_API_KEY：必填，阿里云百炼的 API 密钥
"""

import os
import sys
import base64
import requests
from pathlib import Path
import argparse


def upload_file_to_oss(api_key: str, model_name: str, file_path: str = None, 
                       base64_data: str = None, filename: str = None) -> str:
    """
    把文件上传到临时对象存储
    
    参数：
        api_key：阿里云百炼的 API 密钥
        model_name：模型名称，例如 wan2.7-image
        file_path：本地文件路径，与 base64_data 二选一
        base64_data：base64 编码的图片数据，与 file_path 二选一
        filename：用 base64_data 上传时指定的文件名，默认 image.png
        
    返回值：
        oss:// 格式的临时地址
        
    可能抛出的异常：
        ValueError：file_path 与 base64_data 都没给
        FileNotFoundError：指定文件不存在
        Exception：上传失败
    """
    
    if not file_path and not base64_data:
        raise ValueError("必须提供 file_path 或 base64_data")
    if file_path and base64_data:
        raise ValueError("file_path 与 base64_data 只能提供一个")
    

    if file_path:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")
        with open(file_path, 'rb') as f:
            file_content = f.read()
        file_name = Path(file_path).name
    else:
        try:
            if ',' in base64_data:
                base64_data = base64_data.split(',', 1)[1]
            file_content = base64.b64decode(base64_data)
        except Exception as e:
            raise Exception(f"base64 解码失败：{e}")
        file_name = filename or "image.png"


    upload_url = "https://dashscope.aliyuncs.com/api/v1/uploads"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    params = {
        "action": "getPolicy",
        "model": model_name
    }
    
    try:
        response = requests.get(upload_url, headers=headers, params=params)
        if response.status_code != 200:
            raise ValueError(f"获取上传凭证失败：{response.text}")
        
        policy_data = response.json()['data']
    except Exception as e:
        raise Exception(f"获取上传凭证失败：{e}")
    
    
    key = f"{policy_data['upload_dir']}/{file_name}"
    
    files = {
        'OSSAccessKeyId': (None, policy_data['oss_access_key_id']),
        'Signature': (None, policy_data['signature']),
        'policy': (None, policy_data['policy']),
        'x-oss-object-acl': (None, policy_data['x_oss_object_acl']),
        'x-oss-forbid-overwrite': (None, policy_data['x_oss_forbid_overwrite']),
        'key': (None, key),
        'success_action_status': (None, '200'),
        'file': (file_name, file_content)
    }
    
    try:
        response = requests.post(policy_data['upload_host'], files=files)
        if response.status_code != 200:
            raise Exception(f"上传失败：{response.text}")
    except Exception as e:
        raise Exception(f"文件上传失败：{e}")
    
    return f"oss://{key}"


def main():
    parser = argparse.ArgumentParser(
        description='上传文件到对象存储的工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 方式一：按文件路径上传
  python file_to_oss.py --file /path/to/image.jpg --model wan2.7-image
  
  # 方式二：上传 base64 数据
  python file_to_oss.py --base64 "<base64_data>" --model wan2.7-image
        """
    )
    
    parser.add_argument('--file', '-f', help='本地文件路径，与 base64_data 二选一')
    parser.add_argument('--base64', '-b', help='base64 编码的图片数据，与 file_path 二选一')
    parser.add_argument('--model', '-m', required=True, help='模型名称，例如 wan2.7-image')
    parser.add_argument('--filename', help='用 base64_data 上传时指定的文件名，默认 image.png')
    
    args = parser.parse_args()


    if not args.file and not args.base64:
        print("❌ 错误：请提供 --file 或 --base64 之一")
        print("   用 --help 查看帮助信息。")
        sys.exit(1)
    
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 DASHSCOPE_API_KEY")
        print("请先设置环境变量：")
        print("使用 bash 时：")
        print("echo 'export DASHSCOPE_API_KEY=\"your-api-key-here\"' >> ~/.bashrc && source ~/.bashrc")
        print("使用 zsh 时：")
        print("echo 'export DASHSCOPE_API_KEY=\"your-api-key-here\"' >> ~/.zshrc && source ~/.zshrc")
        sys.exit(1)
    
    try:
        if args.base64:
            oss_url = upload_file_to_oss(api_key, args.model, base64_data=args.base64, 
                                        filename=args.filename)
        else:
            oss_url = upload_file_to_oss(api_key, args.model, file_path=args.file)
        
        print(oss_url)
    except Exception as e:
        print(f"❌ 失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
