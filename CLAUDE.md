# Agent Instructions — tweet-to-xhs

## 这个项目是什么

把一条 Twitter/X 推文截图成小红书封面图（1080×1440，3:4比例），并自动打开小红书发布页。

## 环境要求

- macOS
- Python 3.8+
- Google Chrome 已安装
- Chrome 中已登录 Twitter/X 账号（Cmd+Q 正常退出过一次）

## 安装步骤（按顺序执行）

```bash
pip3 install -r requirements.txt
python3 -m playwright install chromium
```

## 运行

```bash
python3 run.py <推文URL>
```

推文 URL 必须包含 `/status/`，例如：
```
python3 run.py https://x.com/username/status/1234567890
```

## 输出

- 截图保存在 `output/tweet_YYYYMMDD_HHMMSS.png`
- 运行结束后 Finder 会弹出文件，Chrome 会打开小红书发布页

## 常见错误处理

| 错误 | 原因 | 解决方法 |
|------|------|---------|
| `❌ 找不到推文` | URL 格式错误或链接失效 | 确认 URL 包含 `/status/` |
| cookies 相关报错 | Chrome 未完整退出或未登录 | 打开 Chrome → 登录 x.com → Cmd+Q 退出 → 重试 |
| `playwright install` 报错 | 网络问题 | 重试或使用代理 |

## 文件结构

```
tweet-to-xhs/
├── run.py           # 主脚本，入口文件
├── requirements.txt # Python 依赖
├── setup.sh         # 一键安装脚本
├── CLAUDE.md        # 本文件，给 Agent 看的说明
├── README.md        # 给人看的说明
├── .gitignore
└── output/          # 截图输出目录（自动创建）
```

## 不需要做的事

- 不需要配置任何 API key
- 不需要登录小红书（发布由用户手动完成）
- 不需要修改任何代码即可使用
