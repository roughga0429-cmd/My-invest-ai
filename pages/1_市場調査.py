import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="市場調査 - My Invest AI Pro", page_icon="📈", layout="wide")

st.title("📈 市場調査・トレンド分析")
st.write(f"最終更新: {datetime.today().strftime('%Y-%m-%d')}")

# --- 🌟 追加：GASで作った「市場調査」シートからAIコメントを読み込む！ ---
st.subheader("🤖 AI 本日の相場ビュー")

# ⚠️ 【重要】ここに大ボスのスプレッドシートの「市場調査」シートのCSV用URLを貼ってな！
# （前にapp.pyに貼ってたみたいな、export?format=csv&gid=〇〇 ってやつやで！）
market_sheet_url = "ここに市場調査シートのURLを貼り付ける"

try:
    # データを読み込んで、一番新しい行（1行目）のコメントを表示するで
    df_market = pd.read_csv(market_sheet_url)
    if not df_market.empty:
        latest_date = df_market.iloc[0, 0]
        latest_comment = df_market.iloc[0, 1]
        st.info(f"**【{latest_date} のAI分析】**\n\n{latest_comment}")
    else:
        st.warning("まだAIの市場分析データがないみたいやわ。GASを実行してみてな！")
except Exception as e:
    st.error("AIコメントの読み込みでエラーが出たわ。URLが合ってるか確認してな！")

st.divider()

# --- 主要インデックス＆為替のリアルタイム表示（yfinance） ---
st.subheader("🌍 主要インデックス＆為替レーダー")

@st.cache_data(ttl=3600)
def fetch_macro_data(ticker_symbol):
    try:
        tkr = yf.Ticker(ticker_symbol)
        hist = tkr.history(period="5d")
        if len(hist) >= 2:
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            diff = current - prev
            diff_pct = (diff / prev) * 100
            return current, diff, diff_pct
        return None, None, None
    except:
        return None, None, None

col1, col2, col3 = st.columns(3)
with col1:
    c, d, dp = fetch_macro_data("^N225")
    if c: st.metric("日経平均株価", f"¥{c:,.0f}", f"{d:+,.0f} ({dp:+.2f}%)")
with col2:
    c, d, dp = fetch_macro_data("^GSPC")
    if c: st.metric("S&P 500", f"${c:,.2f}", f"{d:+,.2f} ({dp:+.2f}%)")
with col3:
    c, d, dp = fetch_macro_data("JPY=X")
    if c: st.metric("ドル円 (USD/JPY)", f"¥{c:,.2f}", f"{d:+,.2f} ({dp:+.2f}%)", delta_color="inverse")

st.divider()

# --- 個別銘柄の深掘り調査エリア ---
st.subheader("🔍 個別銘柄 深掘り調査")
search_ticker = st.text_input("証券コードを入力（例: 7011）", max_chars=4)

if st.button("📈 トレンドを調査する"):
    if search_ticker:
        with st.spinner('データ集めてるで...'):
            try:
                tkr = yf.Ticker(f"{search_ticker}.T")
                hist_1mo = tkr.history(period="1mo")
                if not hist_1mo.empty:
                    info = tkr.info
                    company_name = info.get('longName', '名称不明')
                    current_price = hist_1mo['Close'].iloc[-1]
                    st.success(f"**{company_name} ({search_ticker})** の直近1ヶ月のデータや！")
                    st.metric("現在値", f"¥{current_price:,.0f}")
                    st.line_chart(hist_1mo['Close'])
                else:
                    st.warning("データが見つからんかったわ。")
            except:
                st.error("エラーが起きたわ。もう1回試してみてな！")
    else:
        st.warning("コードを入力してや！")
