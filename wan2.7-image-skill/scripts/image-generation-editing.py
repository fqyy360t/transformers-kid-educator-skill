#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-2026 The Alibaba Wan Team Authors. All rights reserved.

"""
image-generation-editing —— 调用百炼接口完成文生图、图像编辑与组图生成。
"""

import os
import sys
import argparse
import requests
import time


def _poll_wan_task_status(task_id: str, headers: dict[str, str]) -> str:
    """轮询任务状态，直到任务结束"""

    dashscope_base_url = os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/api/v1/")
    check_url = f"{dashscope_base_url}tasks/{task_id}"
    
    status = "PENDING"
    check_count = 0
    while status not in ("SUCCEEDED", "FAILED", "CANCELLED"):
        if check_count >= 15:
            return {"status": status, "content": []}
        print(
            f"正在查询百炼任务 {task_id}，当前状态：{status} ……")
        time.sleep(3)  # 每次查询间隔 3 秒
        poll_response = requests.get(check_url, headers=headers)
        if poll_response.status_code != 200:
            try:
                error_data = poll_response.json()
                error_message = error_data.get(
                    "error", f"HTTP {poll_response.status_code}")
            except Exception:
                error_message = f"HTTP {poll_response.status_code}"
            raise Exception(
                f"查询百炼任务失败：{error_message}")
        
        poll_res = poll_response.json()
        status = poll_res.get("output", {}).get("task_status")
        if status == "SUCCEEDED":
            output = poll_res.get("output", {}).get("choices", [])[0].get("message", None).get("content", None)
            if output and isinstance(output, list):
                return {"status": status, "content": output}
            else:
                raise Exception(
                    "成功响应中未找到图片地址")
        elif status == "FAILED":
            failed_code = poll_res.get("output", {}).get("code", "")
            failed_message = poll_res.get("output", {}).get("message", "")
            detail_error = f"任务失败，错误码：{failed_code}，说明：{failed_message}"
            raise Exception(
                f"百炼图片生成失败：{detail_error}")
        check_count += 1
    raise Exception(f"任务查询结束，最终状态：{status}")
    

def generate(user_requirement: str, input_images: list[str] = [], n: int = 1, size: str = '1K', enable_sequential: bool = False):
    """
    调用百炼接口完成文生图、图像编辑与组图生成

    参数：
        user_requirement：用户对文生图、图像编辑或组图生成的需求描述
        input_images：输入的参考图
        n：生成图片数量
        size：生成图片的分辨率
        enable_sequential：是否启用组图生成
        
    返回值：
        dict：包含 success、content 等字段的结果字典
    """

    try:
        api_key = os.environ.get("DASHSCOPE_API_KEY")
        if not api_key:
            return {
                "success": False,
                "error": "未提供 API 密钥，请设置 DASHSCOPE_API_KEY 环境变量"
            }

        dashscope_base_url = os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/api/v1/")
        api_url = f"{dashscope_base_url}services/aigc/image-generation/generation"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "X-DashScope-Async": "enable",
            "X-DashScope-OssResourceResolve": "enable"
        }
        payload = {
            "model": "wan2.7-image",
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"text": f"{user_requirement}"}
                        ]
                    }
                ]
            },
            "parameters": {
                "size": f"{size}",
                "n": n,
                "watermark": False,
                "enable_sequential": enable_sequential
            }
        }
        if input_images:
            for img_url in input_images:
                payload['input']['messages'][0]['content'].append({"image": f"{img_url}"})
        response = requests.post(api_url, headers=headers, json=payload)

        # 发起生成请求
        if response.status_code != 200:
            try:
                error_data = response.json()
                error_message = error_data.get(
                    "error", f"HTTP {response.status_code}")
            except Exception:
                error_message = f"HTTP {response.status_code}"
            raise Exception(
                f"创建百炼任务失败：{error_message}")
        result = response.json()
        task_id = result.get("output", {}).get("task_id", None)
        print('任务编号（task_id）：', task_id)

        # 查询生成结果
        check_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        poll_rst = _poll_wan_task_status(task_id, check_headers)
        status = poll_rst['status']
        content = poll_rst['content']
        if status == 'SUCCEEDED':
            for rst_idx, rst_item in enumerate(content):
                rst_type = rst_item.get('type', '')
                if rst_type == 'image':
                    print(f'第 {rst_idx+1} 张：', rst_item['image'])

            return {
                "success": True,
                "content": content,
                "error": ""
            }
        elif status == 'RUNNING':
            return {
                "success": False,
                "content": content,
                "task_id": task_id,
                "error": "still running"
            }

    except Exception as e:
        print(f"❌ 生成失败：{e}")
        return {
            "success": False,
            "error": f"Generation failed: {e}"
        }


def main():
    parser = argparse.ArgumentParser(description="调用百炼接口完成文生图、图像编辑与组图生成")

    parser.add_argument("--user_requirement", type=str, required=True, help="用户对文生图、图像编辑或组图生成的需求描述")

    parser.add_argument("--input_images", nargs='*', default=[], help="输入的参考图")
    parser.add_argument("--n", type=int, default=1, help="生成图片数量")
    parser.add_argument("--size", type=str, default='1K', help="生成图片的分辨率")
    parser.add_argument("--enable_sequential", action="store_true", help="是否启用组图生成")
    
    args = parser.parse_args()
    

    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ 错误：未设置 DASHSCOPE_API_KEY")
        print("请先设置环境变量：")
        print("使用 bash 时：")
        print("echo 'export DASHSCOPE_API_KEY=\"your-api-key-here\"' >> ~/.bashrc && source ~/.bashrc")
        print("使用 zsh 时：")
        print("echo 'export DASHSCOPE_API_KEY=\"your-api-key-here\"' >> ~/.zshrc && source ~/.zshrc")
        sys.exit(1)
    
    dashscope_base_url = os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/api/v1/")
    api_url = f"{dashscope_base_url}services/aigc/image-generation/generation"

    try:
        result = generate(
            user_requirement=args.user_requirement,
            input_images=args.input_images,
            n=args.n,
            size=args.size,
            enable_sequential=args.enable_sequential
        )
        
        if result["success"]:
            print("\n🎉 生成成功！")
        else:
            if result['error'] == 'still running':
                print(f"\n仍在进行中：这是异步生成任务，稍后可用任务编号 {result['task_id']} 再查一次。")
            else:
                print(f"\n❌ 生成失败：{result['error']}")
                sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断了操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序执行失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
