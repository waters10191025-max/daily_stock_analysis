import os
import pandas as pd
from datetime import datetime

def generate_report():
    # 1. 模拟获取 AI 分析数据 (你可以根据需要修改这里的文字)
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 假设这是 Gemini AI 给出的真实分析结果
    stock_data = [
        {
            "symbol": "sh600519",
            "name": "贵州茅台",
            "score": 92,
            "advice": "建议持有",
            "reason": "技术面回踩支撑位，Gemini AI 监测到主力资金流入，短期情绪偏乐观。"
        },
        {
            "symbol": "002202",
            "name": "金风科技",
            "score": 78,
            "advice": "观望",
            "reason": "可再生能源板块近期波动较大，建议等待日线级别放量突破后再行介入。"
        }
    ]

    # 2. 准备 HTML 内容
    os.makedirs("reports", exist_ok=True)
    html_path = "reports/index.html"
    
    # 构建网页头部
    html_start = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>AI 决策仪表盘</title>
        <style>
            body {{ background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 20px; }}
            .container {{ max-width: 800px; margin: auto; }}
            .header {{ text-align: center; border-bottom: 2px solid #ffd700; padding-bottom: 20px; }}
            .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-top: 20px; position: relative; }}
            .stock-name {{ color: #ffd700; font-size: 24px; margin: 0; }}
            .score {{ position: absolute; top: 20px; right: 20px; font-size: 48px; color: #39d353; font-weight: bold; }}
            .advice {{ display: inline-block; background: #238636; color: white; padding: 5px 15px; border-radius: 20px; margin: 10px 0; font-weight: bold; }}
            .reason {{ color: #8b949e; line-height: 1.6; border-top: 1px solid #30363d; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📈 AI 决策仪表盘</h1>
                <p>系统更新时间：{report_date}</p>
            </div>
    """
    
    # 动态生成股票卡片 (直接用循环生成，不再用花括号)
    cards_html = ""
    for stock in stock_data:
        cards_html += f"""
            <div class="card">
                <div class="score">{stock['score']}</div>
                <h2 class="stock-name">{stock['name']} <small style="color:#58a6ff">{stock['symbol']}</small></h2>
                <div class="advice">{stock['advice']}</div>
                <div class="reason">
                    <strong>Gemini 核心逻辑：</strong><br>
                    {stock['reason']}
                </div>
            </div>
        """
    
    html_end = """
            <div style="text-align:center; margin-top:40px; color:#484f58; font-size:12px;">
                提示：AI 生成内容仅供参考，不构成投资建议
            </div>
        </div>
    </body>
    </html>
    """
    
    # 合并并写入文件
    full_html = html_start + cards_html + html_end
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"✅ 成功生成清晰版仪表盘: {html_path}")

if __name__ == "__main__":
    generate_report()
