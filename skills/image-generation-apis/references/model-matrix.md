# 生图模型矩阵（2026-08-08 实测）

## 8个模型状态

| # | 模型 | 平台 | 收费 | 角色一致性 | 状态 | 用途 |
|:--|:--|:--|:--|:--|:--|:--|
| 1 | **Seedream 5.0** | 火山方舟 | 0.22元/张 | 🟢🟢 最强(10图参考) | ✅ 主力 | 封面人物 |
| 2 | **通义万相** | 阿里 | ~0.1元/张 | 🟡 中 | ✅ 接入 | 高质量生图 |
| 3 | **CogView-3-flash** | 智谱 | 免费/便宜 | 🟡 中 | ✅ 可用 | 参考图生成 |
| 4 | **Kolors** | 硅基流动 | 免费 | 🟡 中 | ✅ 接入 | 免费生图 |
| 5 | **ComfyUI SDXL** | 本地 | 免费 | 🟢 强(IPAdapter) | ✅ 可用 | 本地大图 |
| 6 | Seedream Pro | 火山 | 贵(需充值) | 🟢🟢 | 🟡 欠费 | 高质量备用 |
| 7 | CogView-4 | 智谱 | 贵些 | 🟡 | 🟡 限流 | 高质量备用 |
| 8 | FLUX | 硅基 | 付费 | 🟢 | ⏳ 待开通 | 备用 |

## key 位置（.env）

- ARK_API_KEY（火山方舟）：`ark-41781275-...`（Seedream + DeepSeek 替补通道）
- DASHSCOPE_API_KEY（阿里）：`sk-ws-H...`
- ZAI_API_KEY / GLM_API_KEY（智谱）
- SILICONFLOW_API_KEY（硅基）：`sk-grvdzjgs...`
- 混元/文心一格：未接入（需注册腾讯云/百度云）

## 各接口完整调用

### Seedream 5.0（主力）
```
POST https://ark.cn-beijing.volces.com/api/v3/images/generations
Authorization: Bearer ARK_API_KEY
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "...",
  "image": "data:image/png;base64,...",   # 参考图
  "response_format": "b64_json",
  "size": "2k",                            # ≥3686400像素
  "watermark": true
}
```

### 通义万相（异步必须）
```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis
Authorization: Bearer DASHSCOPE_API_KEY
X-DashScope-Async: enable                  # 关键！否则403
{
  "model": "wanx2.1-t2i-turbo",
  "input": {"prompt": "..."},
  "parameters": {"size": "1024*1024", "n": 1}
}
# → output.task_id → 轮询 GET /api/v1/tasks/{task_id} 直到 SUCCEEDED
```

### CogView（智谱）
```
POST https://open.bigmodel.cn/api/paas/v4/images/generations
Authorization: Bearer ZAI_API_KEY
{
  "model": "cogview-3-flash",              # cogview-4限流时用3-flash
  "prompt": "...",
  "size": "1024x1024",
  "reference_image": "base64"              # 参考图
}
```

### Kolors（硅基，免费）
```
POST https://api.siliconflow.cn/v1/images/generations
Authorization: Bearer SILICONFLOW_API_KEY
{
  "model": "Kwai-Kolors/Kolors",           # FLUX被禁用
  "prompt": "...",
  "image_size": "1024x1024",
  "batch_size": 1
}
# → images[0].url（S3临时URL 1小时，需完整URL下载）
```

### ComfyUI（本地）
```
cd D:\软件\ComfyUI\ComfyUI_Windows_portable\ComfyUI
unset PYTHONPATH && ../python_standalone/python.exe -s main.py --windows-standalone-build
# 端口8188，API POST /prompt
```

## 关键经验

1. **角色一致性=参考图锁定**：Seedream 的 `image` 参数 + 提示词"保持完全一致" → 形象锁定+动作跟随（CogView做不到）
2. **URL下载普遍403**：优先 `response_format: b64_json` 直接拿数据
3. **火山方舟也是 DeepSeek 替补**：`deepseek-v4-flash-ga-260731` 走 chat/completions（DeepSeek涨价应对）
4. **ComfyUI IPAdapter**：API盲调接口不匹配（IPAdapterApply vs IPAdapter），图形界面可做但需手动
5. **月成本极低**：封面每月~10张×0.22元 = 2-3元/月；日常用免费模型
