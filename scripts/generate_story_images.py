#!/usr/bin/env python3
"""
变形金刚儿童知识讲解员 - 图片生成脚本
集成 Wan2.7 Image 生成组图
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Wan2.7 Skill 路径（项目根目录下的 wan2.7-image-skill 子目录）
SKILL_ROOT = Path(__file__).resolve().parent.parent
WAN_SKILL_PATH = SKILL_ROOT / "wan2.7-image-skill"


def check_environment():
    """检查环境配置"""
    print("=" * 60)
    print("🤖 变形金刚儿童知识讲解员 - 图片生成")
    print("=" * 60)

    # 检查 Wan2.7 Skill
    if not WAN_SKILL_PATH.exists():
        print(f"❌ 错误：未找到 wan2.7-image-skill")
        print(f"   请确认项目根目录下存在 wan2.7-image-skill/ 文件夹")
        return False

    # 检查 API Key
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("⚠️  警告：未设置 DASHSCOPE_API_KEY 环境变量")
        print("   请设置：export DASHSCOPE_API_KEY='your-key-here'")
        # 继续执行，让用户自己决定
    else:
        print("✅ API Key 已配置")

    print(f"✅ Wan2.7 Skill 路径：{WAN_SKILL_PATH}")
    return True


def build_prompt(story_data):
    """构建组图生成提示词"""

    num_images = story_data.get("num_images", 5)
    character = story_data.get("character", "擎天柱和大黄蜂")
    knowledge = story_data.get("knowledge", "浮力")
    style = story_data.get("style", "变形金刚动画片风格")

    # 画面描述模板
    image_descriptions = {
        3: [
            f"{style}，{character}在明亮的汽车人基地里，准备开始学习关于{knowledge}的知识，儿童友好，明亮鲜艳的色彩",
            f"{style}，{character}在做关于{knowledge}的小实验，大家都在认真观察，儿童友好，明亮温暖的色彩",
            f"{style}，{character}开心地庆祝学到了新知识，右下角有知识卡片，儿童友好，温暖的色彩"
        ],
        5: [
            f"{style}，{character}在明亮的汽车人基地里，收到任务，准备去探索关于{knowledge}的知识，儿童友好，明亮鲜艳的色彩",
            f"{style}，{character}在户外发现了有趣的现象，表情好奇惊讶，儿童友好，明亮的自然色调",
            f"{style}，{character}在做关于{knowledge}的小实验，桌上有实验道具，大家都在认真观察，儿童友好，明亮温暖的色彩",
            f"{style}，{character}用学到的{knowledge}知识解决问题，行动起来，动态感，儿童友好，明亮欢快的色彩",
            f"{style}，{character}开心地庆祝任务完成，右下角有一个可爱的知识卡片写着'{knowledge}小知识'，儿童友好，温暖的橙色调"
        ],
        8: [
            f"{style}，{character}在明亮的汽车人基地里，警报响起，收到紧急任务，儿童友好，明亮鲜艳的色彩",
            f"{style}，{character}出发前往现场，充满期待和好奇，儿童友好，明亮的色彩",
            f"{style}，{character}到达现场，发现了问题，表情疑惑，儿童友好",
            f"{style}，{character}开始讨论和思考关于{knowledge}的问题，儿童友好",
            f"{style}，{character}在做关于{knowledge}的小实验，桌上有实验道具，儿童友好，明亮温暖的色彩",
            f"{style}，{character}明白了！表情恍然大悟，儿童友好",
            f"{style}，{character}用学到的{knowledge}知识解决问题，行动起来，儿童友好，明亮欢快的色彩",
            f"{style}，{character}开心地庆祝任务完成，右下角有知识卡片，儿童友好，温暖的色彩"
        ]
    }

    descriptions = image_descriptions.get(num_images, image_descriptions[5])

    # 构建完整提示词
    prompt = f"生成一个{num_images}张图的儿童教育绘本：\n"
    for i, desc in enumerate(descriptions, 1):
        prompt += f"{i}. {desc}\n"
    prompt += "要求：儿童友好，无恐怖元素，无战斗场景，明亮鲜艳的色彩，高品质，2K分辨率"

    return prompt


def call_wan27(prompt, num_images=5, size="1K"):
    """调用 Wan2.7 生成组图"""

    script_path = WAN_SKILL_PATH / "scripts" / "image-generation-editing.py"

    if not script_path.exists():
        print(f"❌ 错误：未找到生成脚本 {script_path}")
        return None

    cmd = [
        "python3",
        str(script_path),
        "--user_requirement", prompt,
        "--n", str(num_images),
        "--size", size,
        "--enable_sequential"
    ]

    print("\n" + "=" * 60)
    print("🎨 调用 Wan2.7 生成组图...")
    print("=" * 60)
    print(f"📝 提示词（前200字符）：{prompt[:200]}...")
    print(f"🖼️  图片数量：{num_images}")
    print(f"📐 分辨率：{size}")
    print("=" * 60)

    try:
        os.chdir(WAN_SKILL_PATH)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            print("✅ 生成成功！")
            print("\n" + "-" * 60)
            print(result.stdout)
            print("-" * 60)
            return result.stdout
        else:
            print("❌ 生成失败")
            print("stderr:", result.stderr)
            return None

    except subprocess.TimeoutExpired:
        print("⏰ 生成超时（超过5分钟）")
        print("   请稍后使用 task_id 查询结果")
        return None
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def main():
    """主函数"""

    # 示例故事数据
    example_story = {
        "num_images": 5,
        "character": "擎天柱和大黄蜂",
        "knowledge": "浮力",
        "style": "变形金刚动画片风格",
        "age_group": "7-9岁"
    }

    if not check_environment():
        return 1

    print("\n📖 示例配置：")
    print(json.dumps(example_story, ensure_ascii=False, indent=2))

    # 构建提示词
    prompt = build_prompt(example_story)

    print("\n" + "=" * 60)
    print("📝 生成的完整提示词：")
    print("=" * 60)
    print(prompt)
    print("=" * 60)

    # 询问是否继续
    print("\n⚠️  注意：调用 Wan2.7 会消耗 API 额度")
    response = input("是否继续？(y/N): ").strip().lower()

    if response == "y" or response == "yes":
        # 调用 Wan2.7
        result = call_wan27(prompt, num_images=example_story["num_images"])
        if result:
            print("\n🎉 完成！请查看上方输出获取图片 URL")
        else:
            print("\n❌ 生成失败，请检查配置")
    else:
        print("\n👋 已取消")
        print("\n💡 提示：您可以根据需要修改示例配置")
        print("   或者直接使用 Wan2.7 命令手动调用")

    return 0


if __name__ == "__main__":
    sys.exit(main())
