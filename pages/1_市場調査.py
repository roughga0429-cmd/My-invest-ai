import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

st.set_page_config(page_title="市場調査 - My Invest AI Pro", page_icon="📈", layout="wide")

st.title("📈 市場調査・トレンド分析")
st.write(f"最終更新: {datetime.today().strftime('%Y-%m-%d')}")

# --- 1. 市場調査のAIコメント ---
st.subheader("🤖 AI 本日の相場ビュー")
# 変換済みの市場調査シートURL
market_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX40s/export?format=csv&gid=1071329934"

try:
    df_market = pd.read_csv(market_sheet_url)
    if not df_market.empty:
        latest_date = df_market.iloc[0, 0]
        latest_comment = df_market.iloc[0, 1]
        st.info(f"**【{latest_date} のAI分析】**\n\n{latest_comment}")
    else:
        st.warning("まだAIの市場分析データがないみたいやわ。GASを実行してみてな！")
except Exception as e:
    st.error("AIコメントの読み込みでエラーが出たわ。")

st.divider()

# --- 2. 🎯 AI PickUp (短期・中期・長期の推奨銘柄) ---
st.subheader("🎯 AI PickUp (推奨銘柄)")

# 大ボスがくれた推奨銘柄のURLをCSV用に変換して埋め込んどいたで！
pickup_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX40s/export?format=csv&gid=0"

try:
    df_pickup = pd.read_csv(pickup_sheet_url)
    
    if not df_pickup.empty:
        # Streamlitのタブ機能で短期・中期・長期を分ける！
        tabs = st.tabs(["短期目線", "中期目線", "長期目線"])
        periods = ["短期", "中期", "長期"]
        
        for i, period in enumerate(periods):
            with tabs[i]:
                # 該当する期間のデータだけ抜き出す
                period_data = df_pickup[df_pickup['推奨期間'] == period]
                
                if not period_data.empty:
                    # 銘柄の数だけ横に並べるカッコええカードレイアウト
                    cols = st.columns(len(period_data))
                    for idx, (_, row_data) in enumerate(period_data.iterrows()):
                        with cols[idx]:
                            st.write(f"### {row_data['銘柄名']} ({row_data['ティッカー']})")
                            st.metric("AI分析スコア", f"{row_data['AI分析スコア']} pt")
                            st.write(f"**💡 根拠:** {row_data['根拠・コメント']}")
                else:
                    st.write("この期間の推奨銘柄はまだないみたいやわ。")
    else:
        st.warning("推奨銘柄のデータが空っぽみたいやわ。")
except Exception as e:
    st.error("推奨銘柄の読み込みエラーや！GASでデータが作られてるか確認してな。")

st.divider()

# --- 3. 主要インデックス＆為替のリアルタイム表示 ---
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
    if c: st.metric("日経平均株価", f
