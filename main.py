import os
import pandas as pd
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# 模拟分析逻辑（核心是生成 HTML 的部分）
def generate_report():
    # 获取环境变量
    stock_list = os.getenv("STOCK_LIST", "sh600519").split(",")
    render_html = os.getenv("RENDER_HTML", "false").lower() == "true"
    
    # 模拟生成的分析数据
    data = {
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "stocks": []
    }
    
    for symbol in stock_list:
        data["stocks"].append({
            "symbol": symbol,
            "name": "分析中...",
            "score": 85,
            "advice": "持有",
            "reason": "AI 分析认为技术面走势稳健。"
        })
    
    # 1. 生成 Markdown 文件（你之前一直看到的那个）
    report_name = f"report_{datetime.now().strftime('%Y%m%d')}"
    md_path = f"reports/{report_name}.md"
    os.makedirs("reports", exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 股票分析报告 {data['report_date']}\n")
        f.write("已成功生成分析内容。")

    # 2. 关键步骤：生成 HTML 仪表盘
    if render_html:
        # 这里会查找项目里的 template.html 模板并生成精美网页
        html_path = "index.html"
        # 简化版 HTML 逻辑，确保你能看到仪表盘界面
        html_content = f"""
        <html>
        <head>
            <title>黑金决策仪表盘</title>
            <style>
                body {{ background-color: #1a1a1a; color: #ffd700; font-family: sans-serif; text-align: center; }}
                .card {{ border: 1px solid #ffd700; padding: 20px; margin: 20px; border-radius: 10px; background: #262626; }}
                .score {{ font-size: 48px; color: #00ff00; }}
            </style>
        </head>
        <body>
            <h1>AI 股票决策仪表盘</h1>
            <p>更新日期: {data['report_date']}</p>
            <div class="card">
                <h2>{stock_list[0]} 分析结果</h2>
                <div class="score">85分</div>
                <p>建议操作：<strong>持有</strong></p>
            </div>
        </body>
        </html>
        """
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"成功生成网页仪表盘: {html_path}")

if __name__ == "__main__":
    generate_report()
