<div align="right">

[English](README.md) | [中文](README_CN.md)

</div>

<div align="center">

# 🤖 变形金刚儿童知识讲解员 Skill

**把枯燥的知识变成精彩的动画冒险故事！**

一个 AI Skill，利用孩子们喜爱的**变形金刚**、**奥特曼**、**汪汪队**、**超级飞侠**、**小猪佩奇**等动画角色，通过引人入胜的故事化教学为 4–12 岁儿童讲解知识，并由 Wan2.7 生成绘本插图。

[![版本](https://img.shields.io/badge/版本-2.0.0-blue.svg)]()
[![年龄](https://img.shields.io/badge/适用年龄-4--12-green.svg)]()
[![许可证](https://img.shields.io/badge/许可证-MIT-yellow.svg)]()

</div>

---

## ✨ 核心特点

- 🎭 **智能角色匹配** — 根据孩子年龄和知识类型自动匹配最合适的动画角色（擎天柱讲逻辑，大黄蜂讲科学，救护车讲健康安全……）
- 📖 **故事化讲解** — 把知识点融入三幕式冒险故事，配合角色原汁原味的对话
- 🎨 **AI 生成绘本** — 集成 [Wan2.7](https://github.com/anthropics/wan2.7-image-skill) 生成连贯的绘本插图（3/5/8 张）
- 🧩 **趣味互动问答** — 可选的 comprehension 问题穿插在故事中
- 🎯 **个性化定制** — 可调节故事难度、时长、角色偏好和教学重点

## 🚀 快速开始

### 前置要求

| 要求 | 说明 |
|---|---|
| **Wan2.7 Image Skill** | 已集成于 `wan2.7-image-skill/` 目录 |
| **DASHSCOPE_API_KEY** | 设置环境变量（[点此获取](https://dashscope.console.aliyun.com/)） |
| **Python 3.8+** | 图片生成脚本所需 |

### 安装

```bash
# 克隆仓库（wan2.7-image-skill 已内置，无需单独安装）
git clone https://github.com/fqyy360t/transformers-kid-educator-skill.git
cd transformers-kid-educator-skill
```

### 基本使用

只需对你的 AI 助手说：

```
"用变形金刚给孩子讲重力知识"
"奥特曼教小朋友认识太阳系"
"给我 5 岁的孩子讲一个关于刷牙的故事"
"汪汪队教孩子过马路安全"
```

### 生成故事绘本

```bash
cd scripts
python generate_story_images.py
```

## 📚 工作流程

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  1. 收集信息      │───▶│  2. 匹配角色      │───▶│  3. 创作故事      │
│  年龄、主题、偏好  │    │  擎天柱？大黄蜂？  │    │  三幕式叙事       │
│                  │    │  奥特曼？         │    │  配角色对话       │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                                        │
                                                        ▼
                                               ┌──────────────────┐
                                               │  4. 生成绘本      │
                                               │  Wan2.7 连贯      │
                                               │  多图生成         │
                                               └──────────────────┘
```

1. **需求收集** — 了解孩子年龄（4–6 / 7–9 / 10–12）、知识类型、角色偏好
2. **角色匹配** — 将知识主题与最佳角色配对（见下表）
3. **故事创作** — 生成结构化故事：发现问题 → 探索知识 → 应用解决
4. **图片生成** — 调用 Wan2.7 API 生成绘本插图

### 角色-主题指南

| 角色 | 适合讲解 | 原因 |
|---|---|---|
| 🔴 **擎天柱** | 数学、逻辑、领导力 | 睿智、有条理，通过解决问题来教学 |
| 🟡 **大黄蜂** | 科学、自然、探索 | 好奇、充满活力，让发现变得有趣 |
| 🟢 **救护车** | 健康、安全、急救 | 细心、知识渊博，善于解释"为什么" |
| ⚡ **奥特曼** | 勇气、环保、责任感 | 温柔的英雄，激发责任心 |
| 🐾 **汪汪队** | 安全、团队合作、社区 | 亲切、注重行动，强调合作精神 |
| ✈️ **超级飞侠** | 地理、文化、旅行 | 环游世界，介绍多元文化 |

## 📁 项目结构

```
transformers-kid-educator-skill/
├── SKILL.md                          # 主 Skill 定义与工作流程
├── QUICKSTART.md                     # 快速入门参考卡片
├── FULL-EXAMPLE.md                   # 完整示例：教"重力"知识
├── README.md                         # 英文文档
├── README_CN.md                      # 中文文档
├── wan2.7-image-skill/               # Wan2.7 图片生成（已内置）
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
├── references/
│   ├── character-voices.md           # 各角色对话风格指南
│   ├── image-prompts.md              # 图片提示词库
│   ├── requirements-gathering.md     # 用户需求收集流程
│   └── story-templates.md            # 4 套可复用故事模板
└── scripts/
    └── generate_story_images.py      # Wan2.7 图片生成桥接脚本
```

## 🎨 故事模板

| 模板 | 适合主题 | 主角 |
|---|---|---|
| 🧩 谜题/任务型 | 数学、逻辑 | 擎天柱 |
| 🌍 冒险/发现型 | 科学、自然 | 大黄蜂 |
| 🚑 救援行动型 | 安全、健康 | 救护车 / 汪汪队 |
| ⏰ 穿越时空型 | 历史、文化 | 超级飞侠 / 擎天柱 |

## 🔧 API 说明

图片生成脚本支持以下参数：

```bash
python scripts/generate_story_images.py
```

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--user_requirement` | 故事提示文本 | （交互式输入） |
| `--n` | 图片数量：3、5 或 8 | 5 |
| `--size` | 分辨率：`1K` 或 `2K` | 2K |
| `--enable_sequential` | 连贯多图模式 | `true` |

## 🤝 参与贡献

欢迎参与贡献！

1. **添加角色** — 在 `references/character-voices.md` 和 `references/image-prompts.md` 中添加新角色
2. **添加故事模板** — 在 `references/story-templates.md` 中添加新模板
3. **优化提示词** — 在 `references/image-prompts.md` 中提升图片生成质量
4. **反馈问题** — 提交 Issue 并添加 `bug` 标签

## 📄 许可证

本项目基于 MIT 许可证 — 详见 [LICENSE](LICENSE)。

## 🙏 致谢

- [Wan2.7 Image Skill](https://github.com/anthropics/wan2.7-image-skill) — AI 图片生成核心
- [DashScope API](https://dashscope.aliyun.com/) — 图片生成服务
- 灵感来自每一位把睡前时光变成故事时间的家长 ❤️

---

<div align="center">
<sub>为好奇的小脑袋而做 ❤️</sub>
</div>
