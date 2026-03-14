import os
import yfinance as yf
import google.generativeai as genai
from datetime import datetime

# 1. 配置 AI 授权
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ 未找到 GEMINI_API_KEY，请在 GitHub Secrets 中配置。")

genai.configure(api_key=api_key)
# 设定生成配置，确保输出更稳定
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 1000,
}
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

def generate_report():
    # 获取你要分析的股票列表
    raw_list = os.getenv("STOCK_LIST", "600519.SS")
    stock_list = [s.strip() for s in raw_list.split(",") if s.strip()]
    
    print(f"开始分析股票列表: {stock_list}")
    final_results = []
    
    for symbol in stock_list:
        try:
            print(f"正在获取 {symbol} 的实时行情...")
            ticker = yf.Ticker(symbol)
            # 获取最近5天数据确保能拿到最新收盘价
            hist = ticker.history(period="5d")
            if hist.empty:
                print(f"⚠️ 无法获取 {symbol} 的数据，请检查代码后缀是否正确。")
                continue
                
            price = hist['Close'].iloc[-1]
            
            # 让 Gemini 分析并强制要求格式
            prompt = (
                f"你是一位资深美股/A股分析师。请分析股票 {symbol}，当前价格为 {price:.2f}。\n"
                f"请严格按照此格式回答，不要有任何多余文字：\n"
                f"评分|建议操作|一句话核心理由\n"
                f"例如：85|持有(HOLD)|技术面回踩关键支撑位，且基本面稳健。"
            )
            
            response = model.generate_content(prompt)
            # 增加清洗逻辑，防止AI返回多余的空格或换行
            res_text = response.text.replace("\n", "").strip()
            res_parts = res_text.split("|")
            
            # 填补缺失字段的保护机制
            score = res_parts[0] if len(res_parts) > 0 else "70"
            advice = res_parts[1] if len(res_parts) > 1 else "观察"
            reason = res_parts[2] if len(res_parts) > 2 else "数据获取成功，建议关注近期波动。"
            
            final_results.append({
                "symbol": symbol,
                "score": score,
                "advice": advice,
                "reason": reason
            })
            print(f"✅ {symbol} 分析成功：{score}分 | {advice}")
            
        except Exception as e:
            print(f"❌ 分析 {symbol} 时发生技术错误: {e}")

    # 4. 生成“黑金仪表盘”网页
    os.makedirs("reports", exist_ok=True)
    
    # 动态生成股票卡片 HTML
    cards_html = ""
    for s in final_results:
        cards_html += f"""
        <div class="card">
            <h2><span class="symbol">{s['symbol']}</span> {s['advice']}</h2>
            <div class="score">{s['score']}</div>
            <div class="reason">
                <strong>Gemini 核心分析逻辑：</strong><br>
                {s['reason']}
            </div>
        </div>
        """

    # 如果没有任何结果，生成一个提示卡片
    if not cards_html:
        cards_html = "<div class='card'><h2>暂无数据</h2><p>请检查 STOCK_LIST 格式是否正确。</p></div>"

    full_html = f"""
    <!DOCTYPE html>
    <html><head><meta charset="utf-8">
    <title>AI 决策仪表盘</title>
    <style>
        body {{ background: #0d1117; color: #ffd700; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; padding: 50px 20px; }}
        h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .time {{ color: #8b949e; margin-bottom: 40px; }}
        .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 30px; margin: 20px auto; max-width: 600px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: transform 0.3s; }}
        .card:hover {{ transform: translateY(-5px); border-color: #ffd700; }}
        .score {{ font-size: 80px; color: #39d353; font-weight: bold; margin: 20px 0; }}
        .symbol {{ color: #58a6ff; font-weight: normal; margin-right: 10px; }}
        .reason {{ border-top: 1px solid #30363d; margin-top: 20px; padding-top: 20px; color: #c9d1d9; line-height: 1.6; text-align: left; }}
        footer {{ margin-top: 60px; color: #484f58; font-size: 0.9em; }}
    </style></head>
    <body>
        <h1>📈 AI 股票决策仪表盘</h1>
        <div class="time">数据更新时刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        {cards_html}
        <footer>系统运行正常 | 核心算法: Gemini | 部署环境: GitHub Actions</footer>
    </body></html>
    """
    
    with open("reports/index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("✨ 最终报告已写入 reports/index.html")

if __name__ == "__main__":
    generate_report()
