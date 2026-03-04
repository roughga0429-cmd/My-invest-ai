import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# ページの設定（タブのタイトルとか）
st.set_page_config(page_title="市場調査 - My Invest AI Pro", page_icon="📈", layout="wide")

st.title("📈 市場調査・トレンド分析")
st.write(f"最終更新: {datetime.today().strftime('%Y-%m-%d')}")
st.write("大ボス、ここでは市場全体の波と、気になる銘柄のトレンドをチェックするで！")

st.divider()

# --- 1. 主要インデックス＆為替のリアルタイム表示 ---
st.subheader("🌍 主要インデックス＆為替レーダー")

# 株価や為替を爆速で取得する関数（yfinance大活躍！）
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
    c, d, dp = fetch_macro_data("^N225") # 日経平均
    if c:
        st.metric("日経平均株価", f"¥{c:,.0f}", f"{d:+,.0f} ({dp:+.2f}%)")
    else:
        st.metric("日経平均株価", "取得エラー")

with col2:
    c, d, dp = fetch_macro_data("^GSPC") # S&P500
    if c:
        st.metric("S&P 500", f"${c:,.2f}", f"{d:+,.2f} ({dp:+.2f}%)")
    else:
        st.metric("S&P 500", "取得エラー")

with col3:
    c, d, dp = fetch_macro_data("JPY=X") # ドル円
    if c:
        # ドル円は「円安（数値がプラス）」が赤字になるように inverse を設定！
        st.metric("ドル円 (USD/JPY)", f"¥{c:,.2f}", f"{d:+,.2f} ({dp:+.2f}%)", delta_color="inverse")
    else:
        st.metric("ドル円 (USD/JPY)", "取得エラー")

st.divider()

# --- 2. 個別銘柄の深掘り調査エリア ---
st.subheader("🔍 個別銘柄 深掘り調査")
st.write("気になる銘柄のコードを入れたら、直近の株価トレンドとチャートを引っ張ってくるで！")

search_ticker = st.text_input("証券コードを入力（例: 7011）", max_chars=4)

if st.button("📈 トレンドを調査する"):
    if search_ticker:
        with st.spinner('データ集めてるで...'):
            try:
                # 日本株は「.T」をつける
                tkr = yf.Ticker(f"{search_ticker}.T")
                info = tkr.info
                hist_1mo = tkr.history(period="1mo")
                
                if not hist_1mo.empty:
                    company_name = info.get('longName', '名称不明')
                    current_price = hist_1mo['Close'].iloc[-1]
                    
                    st.success(f"**{company_name} ({search_ticker})** の直近1ヶ月のデータや！")
                    st.metric("現在値", f"¥{current_price:,.0f}")
                    
                    # 終値のチャートを描画
                    st.line_chart(hist_1mo['Close'])
                else:
                    st.warning("データが見つからんかったわ。コード間違ってないか確認してな！")
            except Exception as e:
                st.error("エラーが起きたわ。もう1回試してみてな！")
    else:
        st.warning("コードを入力してや！")
