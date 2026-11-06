#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2025-2026 The Alibaba Wan Team Authors. All rights reserved.

"""
check_wan_task_status —— 按任务编号查询异步生成任务的状态与最终结果。
"""

import os
import sys
import argparse
import requests


def _check_wan_task_status(task_id: str, headers: dict[str, str]) -> str:
    """查询任务状态，直到任务结束"""

    dashscope_base_url = os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/api/v1/")
    check_url = f"{dashscope_base_url}tasks/{task_id}"
    
    check_response = requests.get(check_url, headers=headers)
    if check_response.status_code != 200:
        try:
            error_data = check_response.json()
            error_message = error_data.get(
                "error", f"HTTP {check_response.status_code}")
        except Exception:
            error_message = f"HTTP {check_response.status_code}"
        raise Exception(
            f"查询百炼任务失败：{error_message}")
    
    check_res = check_response.json()
    status = check_res.get("output", {}).get("task_status")
    if status == "SUCCEEDED":
        output = check_res.get("output", {}).get("choices", [])[0].get("message", None).get("content", None)
        if output and isinstance(output, list):
            return {"status": status, "content": output}
        else:
            raise Exception(
                "成功响应中未找到图片地址")
    elif status == "RUNNING":
        return {"status": status, "content": []}
    elif status == "FAILED":
        failed_code = check_res.get("output", {}).get("code", "")
        failed_message = check_res.get("output", {}).get("message", "")
        detail_error = f"任务失败，错误码：{failed_code}，说明：{failed_message}"
        raise Exception(
            f"百炼图片生成失败：{detail_error}")
    raise Exception(f"任务查询结束，最终状态：{status}")


def main():
    parser = argparse.ArgumentParser(description="按任务编号查询异步生成任务的状态与最终结果")
    parser.add_argument("--task_id", type=str, required=True, help="要查询的任务编号")
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
    
    check_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
    }

    try:
        check_rst = _check_wan_task_status(task_id = args.task_id, headers = check_headers)
        status = check_rst["status"]
        content = check_rst["content"]
        
        if status == "SUCCEEDED":
            for rst_idx, rst_item in enumerate(content):
                rst_type = rst_item.get('type', '')
                if rst_type == 'image':
                    print(f'第 {rst_idx+1} 张：', rst_item['image'])
            print("\n🎉 生成成功！")
        elif status == "RUNNING":
            print(f"\n仍在进行中：这是异步生成任务，稍后可用任务编号 {args.task_id} 再查一次。")
        
            
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断了操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序执行失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
