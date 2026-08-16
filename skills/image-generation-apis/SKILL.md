---
name: image-generation-apis
description: AI生图API接入矩阵与调用方法。触发：要生图/接入生图模型/选生图方案。
version: 1.0.0
category: creative
---

# AI生图API接入矩阵

> 2026-08-08 建立。会话突破：Seedream 5.0 参考图=角色一致性（形象锁定+动作跟随）。
> 完整矩阵也在 OB：`10-Hermes/生图模型矩阵.md`

## 选型原则（先看这个）

1. **封面角色一致性** → Seedream 5.0（0.22元/张，值）——参考图锁形象+动作
2. **日常快速图** → CogView-3-flash / Kolors（免费）
3. **本地大图/批量** → ComfyUI SDXL（免费，8GB显存可跑）
4. **质量要求高** → 通义万相
5. **角色更强**（Pro）→ Seedream Pro（需充值）

## 主力：Seedream 5.0（火山方舟）

```python
POST https://ark.cn-beijing.volces.com/api/v3/images/generations
Headers: Authorization: Bearer ark-41781275-...
Body: {
  "model": "doubao-seedream-5-0-260128",
  "prompt": "保持参考图中卡通人物（棕色微翘短发、圆脸、黑色粗框眼镜、蓝色连帽衫）完全一致的样貌，生成他[动作+场景]",
  "image": "data:image/png;base64,{参考图b64}",  # 关键：参考图锁定形象
  "response_format": "b64_json",
  "size": "2k",  # 见下方坑
  "watermark": True
}
# 返回 data[0].b64_json → base64解码保存
# 0.22元/张 | 参考图=角色一致（10图参考）
```

### Seedream 参数坑（实测）
- **size 最小像素限制**：必须 ≥ 3686400 像素（约2048×1800）——**不支持 1k / 720×1280**，用 `2k`/`3k`/`4k` 或 `WIDTHxHEIGHT`（如 2048x2048）
- **Pro 版**（doubao-seedream-5-0-pro-260628）：RPM 限流 + 需充值（AccountOverdueError）
- **参考图参数**：`image: "data:image/jpeg;base64,{b64}"`（角色一致性关键）——**必须带 data URI 前缀**！直接传裸 base64 → 400 "invalid url specified"（实测 2026-08-12）。格式用 jpeg/png 都行，但要 `data:image/<格式>;base64,` 前缀
- **chat/completions 方式**：Seedream 5.0 标准版不支持 chat 接口（只走 images/generations）

### 封面人物形象分工（2026-08-12 用户确立）
- **九思形象（雾蓝波波头Y2K女主播）** → 九思对外输出的文章（AI技能分享/AI内容）——参考图用 `播客创作/02-音频/九思头像/换发型/hair4_bob.png`
- **苏不倦形象（棕色短发卡通/黑框眼镜/蓝连帽衫）** → 需要苏不倦出场时（节目组合/苏不倦IP）——参考图用 `九思对外输出/06-设计源文件/cartoon-final.png`
- 做封面前先判断：这篇是谁的内容？用对应形象（别默认用一个）

## 替补模型速查

| 模型 | 平台 | 调用要点/坑 |
|:--|:--|:--|
| **通义万相** | 阿里 | **必须加 `X-DashScope-Async: enable` 头**（否则403"不支持同步"）；异步提交→轮询 GET /api/v1/tasks/{id}；URL下载403防盗链 |
| **CogView-3-flash** | 智谱 | cogview-4 限流时用它（同一key）；参考图=reference_image 参数；国内直连 |
| **Kolors** | 硅基 | model=Kwai-Kolors/Kolors（FLUX被禁用Model disabled）；返回S3临时URL，**要完整URL才能下载**（打印截断会坏）；1小时有效 |
| **ComfyUI SDXL** | 本地 | 启动：`cd ComfyUI_Windows_portable/ComfyUI && unset PYTHONPATH && ../python_standalone/python.exe -s main.py --windows-standalone-build`；端口8188；10秒出图 |

## 通用工作流

1. **形象固定**：确认的IP形象 → 存透明PNG（rembg抠图）作参考图
2. **角色一致性**：参考图 + 提示词"保持参考图中[形象特征]完全一致的样貌，生成他[动作+场景]"
3. **生成后审图**（铁律）：形象一致？动作对吗？畸形（手/五官）？→ 用 vision_analyze 逐项查
4. **封面合成**：HTML（场景图作背景+标题+品牌）→ Chrome headless 截图 → vision 验证

## Pitfalls

- **Seedream 生图慢**（30-100秒）：等待超时设 ≥180秒；或分批
- **URL下载403**：万相/S3 都有防盗链——优先用 `response_format: b64_json` 直接拿数据
- **别贴肖像**：封面人物要"在场景里做事"（电脑前/打字），不是站着贴图
- **先确认工具能力再动手**：做不到（如CogView参考图漂移）→ 换方案，不硬试（用户"图做混乱了"教训）
