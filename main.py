import os
import yfinance as yf
import google.generativeai as genai
from datetime import datetime

# 1. 配置 AI 授权
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ 未找到 GEMINI_API_KEY，请在 GitHub Secrets 中配置。")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash') # 使用更快的模型

def generate_report():
    # 获取你要分析的股票列表
    stock_list = os.getenv("STOCK_LIST", "sh600519.SS").split(",")
    final_results = []
    
    for symbol in stock_list:
        try:
            # 2. 自动抓取 yfinance 免费行情数据
            # 提示：yfinance 对 A 股需要加后缀，如 sh600519.SS
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="5d")
            price = hist['Close'].iloc[-1]
            
            # 3. 让 Gemini 分析
            prompt = f"分析股票代码 {symbol}，当前价格 {price:.2f}。请给出评分(0-100)、建议和极简核心理由。格式：评分|建议|理由"
            response = model.generate_content(prompt)
            res_parts = response.text.strip().split("|")
            
            final_results.append({
                "symbol": symbol,
                "score": res_parts[0] if len(res_parts)>0 else "N/A",
                "advice": res_parts[1] if len(res_parts)>1 else "分析中",
                "reason": res_parts[2] if len(res_parts)>2 else "暂无理由"
            })
            print(f"✅ 完成 {symbol} 的 AI 分析。")
        except Exception as e:
            print(f"❌ 分析 {symbol} 时出错: {e}")

    # 4. 生成你已经成功的“黑金仪表盘”网页
    os.makedirs("reports", exist_ok=True)
    html_content = f"""
    <html><head><meta charset="utf-8">
    <title>AI 决策仪表盘</title>
    <style>
        body {{ background: #0d1117; color: #ffd700; font-family: sans-serif; text-align: center; padding-top: 50px; }}
        .card {{ background: #161b22; border: 2px solid #ffd700; border-radius: 20px; padding: 30px; margin: 30px auto; width: 70%; box-shadow: 0 0 20px rgba(255,215,0,0.1); }}
        .score {{ font-size: 72px; color: #00ff00; font-weight: bold; }}
        .symbol {{ color: #58a6ff; font-size: 18px; }}
        .reason {{ border-top: 1px solid #30363d; margin-top: 20px; padding-top: 15px; color: #8b949e; line-height: 1.6; text-align: left; }}
    </style></head>
    <body>
        <h1>📈 AI 股票决策仪表盘</h1>
        <p>Gemini 智能分析时刻：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """
    for s in final_results:
        html_content += f"""
        <div class="card">
            <h2><span class="symbol">{s['symbol']}</span> {s['advice']}</h2>
            <div class="score">{s['score']}</div>
            <div class="reason">
                <strong>Gemini 核心分析逻辑：</strong><br>
                {s['reason']}
            </div>
        </div>
        """
    html_content += f"""
        <footer style="margin-top: 50px; color: #666;">系统运行正常 | 核心算法: Gemini | 部署环境: GitHub Actions</footer>
    </body></html>
    """
    
    with open("reports/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ 成功生成真实 AI 分析网页: reports/index.html")

if __name__ == "__main__":
    generate_report()
