<div align="right">

[English](README.md) | [中文](README_CN.md)

</div>

<div align="center">

# 🤖 Transformers Kid Educator Skill

**Turn boring lessons into epic animated adventures!**

An AI skill that uses beloved characters like **Transformers**, **Ultraman**, **PAW Patrol**, **Super Wings**, and **Peppa Pig** to teach children aged 4–12 through engaging, story-driven lessons — with AI-generated storybook illustrations powered by Wan2.7.

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)]()
[![Age](https://img.shields.io/badge/ages-4--12-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)]()

</div>

---

## ✨ Features

- 🎭 **Smart Character Matching** — Automatically selects the best character for the child's age and topic (Optimus Prime for logic, Bumblebee for science, Ratchet for health & safety…)
- 📖 **Story-Driven Learning** — Embeds knowledge into 3-act adventure narratives with real character dialogue
- 🎨 **AI Image Generation** — Integrates with [Wan2.7](https://github.com/anthropics/wan2.7-image-skill) to generate sequential storybook illustrations (3/5/8 images)
- 🧩 **Interactive Q&A** — Optional comprehension questions woven into the story
- 🎯 **Personalized** — Adjustable difficulty, story length, character preference, and educational focus

## 🚀 Quick Start

### Prerequisites

| Requirement | Details |
|---|---|
| **Wan2.7 Image Skill** | Included in `wan2.7-image-skill/` (bundled) |
| **DASHSCOPE_API_KEY** | Set in your environment ([get one here](https://dashscope.console.aliyun.com/)) |
| **Python 3.8+** | Required for image generation script |

### Installation

```bash
# Clone the repo (wan2.7-image-skill is bundled — no separate install needed)
git clone https://github.com/fqyy360t/transformers-kid-educator-skill.git
cd transformers-kid-educator-skill
```

### Basic Usage

Just say any of these to your AI assistant:

```
"Give a children's lesson about gravity with Transformers"
"Ultraman teaches kids about the solar system"
"Create a story for my 5-year-old about brushing teeth"
"汪汪队教孩子过马路安全"
```

### Generate Story Images

```bash
cd scripts
python generate_story_images.py
```

## 📚 How It Works

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  1. Gather Info  │───▶│  2. Pick Character│───▶│  3. Create Story │
│  age, topic,     │    │  Optimus? Bumble- │    │  3-act narrative │
│  preferences     │    │  bee? Ultraman?   │    │  with dialogue   │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                                        │
                                                        ▼
                                               ┌──────────────────┐
                                               │  4. Generate Art  │
                                               │  Wan2.7 sequential│
                                               │  image generation │
                                               └──────────────────┘
```

1. **Requirements Gathering** — Collects child's age (4–6 / 7–9 / 10–12), topic type, character preference
2. **Character Selection** — Matches topic to the ideal character (see table below)
3. **Story Creation** — Generates a structured story with Problem → Exploration → Resolution
4. **Image Generation** — Calls Wan2.7 API to produce storybook illustrations

### Character-Topic Guide

| Character | Best For | Why |
|---|---|---|
| 🔴 **Optimus Prime** | Math, Logic, Leadership | Wise, methodical, teaches through problem-solving |
| 🟡 **Bumblebee** | Science, Nature, Exploration | Curious, energetic, makes discovery fun |
| 🟢 **Ratchet** | Health, Safety, First Aid | Careful, knowledgeable, explains "why" clearly |
| ⚡ **Ultraman** | Courage, Environmental Care | Gentle hero, inspires responsibility |
| 🐾 **PAW Patrol** | Safety, Teamwork, Community | Relatable, action-oriented, emphasizes cooperation |
| ✈️ **Super Wings** | Geography, Culture, Travel | Explores the world, introduces diversity |

## 📁 Project Structure

```
transformers-kid-educator-skill/
├── SKILL.md                          # Main skill definition & workflow
├── QUICKSTART.md                     # Quick-start reference card
├── FULL-EXAMPLE.md                   # Worked example: teaching "gravity"
├── README.md                         # English documentation
├── README_CN.md                      # Chinese documentation
├── wan2.7-image-skill/               # Wan2.7 image generation (bundled)
│   ├── SKILL.md
│   ├── scripts/
│   └── references/
├── references/
│   ├── character-voices.md           # Dialogue style per character
│   ├── image-prompts.md              # Image prompt library
│   ├── requirements-gathering.md     # User requirements flow
│   └── story-templates.md            # 4 reusable story templates
└── scripts/
    └── generate_story_images.py      # Wan2.7 image generation bridge
```

## 🎨 Story Templates

| Template | Best For | Lead Character |
|---|---|---|
| 🧩 Puzzle / Mission | Math, Logic | Optimus Prime |
| 🌍 Adventure / Discovery | Science, Nature | Bumblebee |
| 🚑 Rescue Action | Safety, Health | Ratchet / PAW Patrol |
| ⏰ Time Travel | History, Culture | Super Wings / Optimus |

## 🔧 API Reference

The image generation script accepts these arguments:

```bash
python scripts/generate_story_images.py
```

| Parameter | Description | Default |
|---|---|---|
| `--user_requirement` | Story prompt text | (interactive) |
| `--n` | Number of images: 3, 5, or 8 | 5 |
| `--size` | Resolution: `1K` or `2K` | 2K |
| `--enable_sequential` | Coherent multi-image mode | `true` |

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Add a character** — Create a new entry in `references/character-voices.md` and `references/image-prompts.md`
2. **Add a story template** — Add to `references/story-templates.md`
3. **Improve prompts** — Enhance image generation quality in `references/image-prompts.md`
4. **Report issues** — Open an issue with the `bug` label

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [Wan2.7 Image Skill](https://github.com/anthropics/wan2.7-image-skill) — AI image generation backbone
- [DashScope API](https://dashscope.aliyun.com/) — Image generation service
- Inspired by every parent who turned bedtime into story time ❤️

---

<div align="center">
<sub>Made with ❤️ for curious little minds</sub>
</div>
