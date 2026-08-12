---
name: cover-pipeline
description: 封面流水线——文章→AI生图(Seedream角色一致)→四平台尺寸适配→视觉验证。触发：要封面/文章配封面时。
version: 1.0.0
category: creative
---

# 封面流水线（Cover Pipeline）

> 2026-08-08 进化：角色一致性突破（Seedream 5.0）→ 沉淀为"文章→封面"自动化流水线。
> 碰撞来源：设计第一原则 + 生图模型矩阵。

## 触发条件
- 用户要封面（公众号/抖音/知乎/小红书）
- 文章写好要配封面
- 要做品牌形象封面

## 流程（五步）

### 1. 读文章主题（设计第一原则）
- 问"这篇在讲什么" → 人物做对应的事
- 例：别等学会先动手 → 人物在电脑前干活/打字

### 2. 生成场景图（Seedream 5.0，角色一致性）
```python
POST https://ark.cn-beijing.volces.com/api/v3/images/generations
Headers: Authorization: Bearer ark-41781275-...
Body: {
  "model": "doubao-seedream-5-0-260128",
  "prompt": "保持参考图中卡通人物（棕色微翘短发、圆脸、黑色粗框眼镜、蓝色连帽衫）完全一致的样貌，生成他[动作+场景]",
  "image": "data:image/png;base64,{卡通形象b64}",  # cartoon-final.png
  "response_format": "b64_json",
  "size": "2k",  # 最小3686400像素
  "watermark": True
}
```
- 参考图固定：`06-设计源文件/cartoon-final.png`（用户确认的IP形象）

### 3. 四平台适配（HTML合成）
| 平台 | 尺寸 | 布局 |
|:--|:--|:--|
| 公众号 | 900×383 | 横版，标题右侧 |
| 抖音 | 900×1200 | 竖版，标题上方 |
| 知乎 | 690×280 | 横版，标题右侧 |
| 小红书 | 1242×1660 | 竖版，标题上方1/3 |

### 4. 视觉验证（自查清单）
- 标题完整/清晰
- 人物形象一致（棕短发/圆脸/黑框眼镜/蓝连帽衫）
- 人物在"做事"（不站桩）
- 布局平衡/无遮挡/无畸形

### 5. 交付+发布闭环
- 复制到桌面 → 用户发布 → 发完删图 → 归档

## 选型（生图模型矩阵）
- 封面 → Seedream 5.0（0.22元/张，角色一致）
- 日常快速 → CogView-3-flash / Kolors（免费）
- 详见：`10-Hermes/生图模型矩阵.md`

## Pitfalls
- Seedream size 必须≥3686400像素（用2k/3k/4k，不支持1k/小尺寸）
- URL下载可能403（用b64_json直接保存）
- CogView参考图会漂移（形象不稳）→ 用Seedream
- IPAdapter API接口不匹配（图形界面才可做）

## 验证
- 视觉验证通过（vision_analyze查标题/人物/布局/畸形）
- 用户确认"可以" = 流水线成功
