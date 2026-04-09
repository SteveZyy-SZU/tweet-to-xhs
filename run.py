"""
tweet-to-xhs: 把推文截图成小红书封面图，并打开发布页面。

用法：
    python3 run.py <推文URL>

示例：
    python3 run.py https://x.com/username/status/1234567890
"""

import asyncio
import sys
import os
import subprocess
from datetime import datetime
from PIL import Image
import rookiepy
from playwright.async_api import async_playwright

# ── 输出设置 ──────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
XHS_PUBLISH_URL = "https://creator.xiaohongshu.com/publish/publish"

# ── 图片尺寸（小红书封面 3:4）────────────────────────────
WIDTH = 1080
HEIGHT = 1440


async def screenshot_tweet(url: str, output_path: str):
    """用Chrome已有的Twitter登录状态截取推文。"""

    # 从Chrome提取Twitter cookies（无需重新登录）
    chrome_cookies = rookiepy.chrome(["x.com", "twitter.com"])

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,  # 后台静默运行，不弹出窗口
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            viewport={"width": WIDTH, "height": HEIGHT},
            device_scale_factor=2,
        )

        # 注入cookies
        playwright_cookies = []
        for c in chrome_cookies:
            playwright_cookies.append({
                "name": c["name"],
                "value": c["value"],
                "domain": c["domain"],
                "path": c.get("path", "/"),
                "secure": c.get("secure", False),
                "httpOnly": c.get("httpOnly", False),
            })
        await context.add_cookies(playwright_cookies)

        page = await context.new_page()
        await page.goto(url, wait_until="load", timeout=30000)
        await page.wait_for_timeout(3000)

        # 找推文元素，精准截图
        article = await page.query_selector('article[data-testid="tweet"]')
        if not article:
            print("❌ 找不到推文，请确认链接是具体的推文（包含 /status/）")
            await browser.close()
            return False

        box = await article.bounding_box()
        side_pad = 16
        clip = {
            "x": max(0, box["x"] - side_pad),
            "y": box["y"],
            "width": box["width"] + side_pad * 2,
            "height": box["height"] + side_pad,
        }
        await page.screenshot(path="__tweet_raw.png", clip=clip)
        await browser.close()

    # 合成3:4封面图
    tweet_img = Image.open("__tweet_raw.png").convert("RGB")
    tw, th = tweet_img.size

    canvas = Image.new("RGB", (WIDTH, HEIGHT), color=(255, 255, 255))

    scale = WIDTH / tw
    new_w = WIDTH
    new_h = int(th * scale)
    tweet_resized = tweet_img.resize((new_w, new_h), Image.LANCZOS)

    y_offset = max(0, (HEIGHT - new_h) // 2)
    canvas.paste(tweet_resized, (0, y_offset))
    canvas.save(output_path)

    os.remove("__tweet_raw.png")
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    url = sys.argv[1]

    # 检查是否是推文链接
    if "/status/" not in url:
        print("❌ 请提供具体的推文链接，格式：https://x.com/用户名/status/数字")
        sys.exit(1)

    # 创建输出目录
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 用时间戳命名，避免覆盖
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(OUTPUT_DIR, f"tweet_{timestamp}.png")

    print(f"📸 正在截图：{url}")
    success = asyncio.run(screenshot_tweet(url, output_path))

    if not success:
        sys.exit(1)

    print(f"✅ 截图已保存：{output_path}")

    # 在Finder中高亮显示文件（方便拖拽）
    subprocess.run(["open", "-R", output_path])

    # 在Chrome中打开小红书发布页
    print("🔗 正在打开小红书创作页面...")
    subprocess.run(["open", "-a", "Google Chrome", XHS_PUBLISH_URL])

    print("\n✨ 完成！")
    print("   1. Finder 里已选中截图文件")
    print("   2. Chrome 里已打开小红书发布页")
    print("   3. 把图片拖入页面，填写标题和正文，发布！")


if __name__ == "__main__":
    main()
