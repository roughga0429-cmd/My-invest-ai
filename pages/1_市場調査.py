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
market_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=1071329934"

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

# 推奨銘柄のURL
pickup_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=0"

try:
    df_pickup = pd.read_csv(pickup_sheet_url)
    
    if not df_pickup.empty:
        tabs = st.tabs(["短期目線", "中期目線", "長期目線"])
        periods = ["短期", "中期", "長期"]
        
        for i, period in enumerate(periods):
            with tabs[i]:
                period_data = df_pickup[df_pickup['推奨期間'] == period]
                if not period_data.empty:
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
            # 確実に計算できるようにする安全設計！
            current = float(hist['Close'].iloc[-1])
            prev = float(hist['Close'].iloc[-2])
            diff = current - prev
            diff_pct = (diff / prev) * 100
            return current, diff, diff_pct
        return None, None, None
    except Exception:
        # エラーが起きてもアプリを止めずにNoneを返す！
        return None, None, None

col1, col2, col3 = st.columns(3)

# 取得に失敗しても画面がクラッシュしないようにガード！
with col1:
    c, d, dp = fetch_macro_data("^N225")
    if c is not None: 
        st.metric("日経平均株価", f"¥{c:,.0f}", f"{d:+,.0f} ({dp:+.2f}%)")
    else: 
        st.metric("日経平均株価", "データ取得エラー")
        
with col2:
    c, d, dp = fetch_macro_data("^GSPC")
    if c is not None: 
        st.metric("S&P 500", f"${c:,.2f}", f"{d:+,.2f} ({dp:+.2f}%)")
    else: 
        st.metric("S&P 500", "データ取得エラー")
        
with col3:
    c, d, dp = fetch_macro_data("JPY=X")
    if c is not None: 
        st.metric("ドル円 (USD/JPY)", f"¥{c:,.2f}", f"{d:+,.2f} ({dp:+.2f}%)", delta_color="inverse")
    else: 
        st.metric("ドル円 (USD/JPY)", "データ取得エラー")

st.divider()

# --- 4. 個別銘柄の深掘り調査エリア ---
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
                    current_price = float(hist_1mo['Close'].iloc[-1])
                    st.success(f"**{company_name} ({search_ticker})** の直近1ヶ月のデータや！")
                    st.metric("現在値", f"¥{current_price:,.0f}")
                    st.line_chart(hist_1mo['Close'])
                else:
                    st.warning("データが見つからんかったわ。")
            except Exception:
                st.error("エラーが起きたわ。もう1回試してみてな！")
    else:
        st.warning("コードを入力してや！")
