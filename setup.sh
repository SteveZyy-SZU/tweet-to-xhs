#!/bin/bash
# tweet-to-xhs 一键安装脚本
# 运行方式：bash setup.sh

set -e

echo "🔧 正在安装依赖..."
pip3 install -r requirements.txt

echo "🌐 正在安装 Chromium 浏览器..."
python3 -m playwright install chromium

echo ""
echo "✅ 安装完成！"
echo ""
echo "下一步："
echo "  1. 用 Google Chrome 登录你的 Twitter/X 账号"
echo "  2. 登录后用 Cmd+Q 正常退出 Chrome"
echo "  3. 运行：python3 run.py <推文链接>"
