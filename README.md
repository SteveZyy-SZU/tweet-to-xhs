# tweet-to-xhs

把一条推文截图成小红书封面图（3:4），并自动打开小红书发布页面。

**一条命令完成截图 → 你只需要拖图、写文字、发布。**

---

## 效果演示

输入一条推文链接，脚本会：

1. 自动截取推文内容（去掉导航栏、推荐栏等干扰元素）
2. 生成 1080×1440 的小红书封面图
3. 在 Finder 中弹出截图文件
4. 在 Chrome 中打开小红书发布页

剩下的事（写标题、写正文、点发布）完全由你完成。

---

## 前提条件

- **操作系统**：macOS（目前仅支持 macOS）
- **Python**：3.8 或以上
- **Google Chrome**：已安装，且已在 Chrome 中登录 Twitter/X 账号

---

## 安装

```bash
# 克隆项目
git clone https://github.com/你的用户名/tweet-to-xhs.git
cd tweet-to-xhs

# 一键安装依赖
bash setup.sh
```

---

## 使用方法

确保 Chrome 已关闭，然后运行：

```bash
python3 run.py https://x.com/用户名/status/推文ID
```

**示例：**

```bash
python3 run.py https://x.com/stevezhang42780/status/2034372902163022248
```

运行后：
- Finder 会自动弹出并选中截图文件
- Chrome 会自动打开小红书发布页
- 把图片拖入发布页，填写标题和正文，发布即可

截图保存在项目目录下的 `output/` 文件夹中。

---

## 常见问题

**Q：提示找不到推文怎么办？**

确认链接格式正确，必须包含 `/status/`，例如：
```
https://x.com/username/status/1234567890
```

**Q：提示 Twitter cookies 为空或登录失败？**

1. 打开 Google Chrome
2. 前往 [x.com](https://x.com) 确认已登录
3. 用 **Cmd+Q** 完整退出 Chrome（不是点×号关窗口）
4. 重新运行脚本

**Q：支持 Windows 吗？**

暂不支持。Windows 的 Chrome 路径和 cookies 加密方式不同，欢迎 PR 贡献。

---

## 工作原理

```
推文 URL
    ↓
rookiepy 从 Chrome 提取 Twitter cookies（无需重新登录）
    ↓
Playwright 后台打开推文页面，注入 cookies
    ↓
找到推文的 article 元素，精准截图
    ↓
Pillow 将截图合成到 1080×1440 白色画布（居中）
    ↓
保存到 output/ 文件夹
    ↓
Finder 弹出文件 + Chrome 打开小红书发布页
```

---

## 安全说明

- 本工具**不会自动发布**到小红书，所有发布操作均由你手动完成
- 不存储任何账号密码，仅读取 Chrome 本地 cookies
- cookies 文件不会被提交到 Git（已加入 `.gitignore`）
- 建议合理使用，勿批量操作，保护账号安全

---

## 依赖

- [Playwright](https://playwright.dev/python/) — 浏览器自动化
- [rookiepy](https://github.com/borisbabic/browser_cookie3) — Chrome cookies 提取
- [Pillow](https://pillow.readthedocs.io/) — 图片合成

---

## License

MIT
