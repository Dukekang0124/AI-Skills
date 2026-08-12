#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""封面提示词生成器——输入文章信息，输出AI生图提示词

用法:
    python3 generate-cover-prompt.py "文章标题" "一句话核心观点" [动作描述]

示例:
    python3 generate-cover-prompt.py "别等学会了再动手" "先做起来AI会教你" "在电脑前打字干活"

输出: 可直接用于AI生图模型的完整提示词
"""

import sys
import json
import os

# 平台尺寸配置
PLATFORM_SIZES = {
    "公众号": "900x383",
    "抖音": "900x1200",
    "知乎": "690x280",
    "小红书": "1242x1660",
}


def load_character(character_file=None):
    """加载固定形象描述（可选）"""
    if character_file and os.path.exists(character_file):
        with open(character_file, encoding="utf-8") as f:
            return f.read().strip()
    return "卡通人物"


def build_prompt(title, core_message, action, character_desc):
    """构建生图提示词"""
    if action:
        action_desc = f"人物在{action}"
    else:
        action_desc = "人物在电脑前工作"
    prompt = (
        f"{character_desc}，保持完全一致的样貌特征。"
        f"{action_desc}，"
        f"屏幕上有与「{core_message}」相关的界面，"
        f"科技感氛围，深蓝青色背景带光点，"
        f"PBR写实渲染，高质量3D动画风格，没有文字"
    )
    return prompt


def main():
    if len(sys.argv) < 3:
        print("用法: python3 generate-cover-prompt.py <文章标题> <一句话核心观点> [动作描述]")
        print("示例: python3 generate-cover-prompt.py \"别等学会了再动手\" \"先做起来AI会教你\" \"在电脑前打字干活\"")
        sys.exit(1)

    title = sys.argv[1]
    core = sys.argv[2]
    action = sys.argv[3] if len(sys.argv) > 3 else ""

    # 读取形象描述（如存在 character.txt）
    character_desc = load_character(os.path.join(os.path.dirname(__file__), "character.txt"))

    prompt = build_prompt(title, core, action, character_desc)

    result = {
        "title": title,
        "core_message": core,
        "action": action or "电脑前工作",
        "prompt": prompt,
        "platform_sizes": PLATFORM_SIZES,
        "checklist": [
            "标题完整/清晰/可读",
            "人物形象一致（不漂移）",
            "人物在做事（不站桩）",
            "布局平衡/无遮挡/无畸形",
            "整体专业感",
        ],
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
