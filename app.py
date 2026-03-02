import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="My Invest AI Pro", layout="wide", initial_sidebar_state="expanded")

# カスタムCSSでデザインを整える
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# サイドバー設定
with st.sidebar:
    st.title("⚙️ System Settings")
    st.write(f"📅 最終更新: {datetime.date.today()}")
    st.divider()
    st.info("💡 **運用方針**: 地政学リスクを考慮したインフラ・ディフェンシブ銘柄の選定")

st.title("🇯🇵 日本株 投資自動分析ボード")

# スプレッドシートのURL
sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=0"

# --- 1. AI注目銘柄セクション ---
try:
    df = pd.read_csv(sheet_url)
    if not df.empty:
        # 最新3件を取得
        recent_df = df.tail(3).iloc[::-1]
        
        st.subheader("🔥 AI PickUp - 今日の注目銘柄")
        cols = st.columns(3)
        
        for i, (idx, row) in enumerate(recent_df.iterrows()):
            with cols[i]:
                # スコアによって色を分ける
                score = int(row.iloc[2])
                color = "inverse" if score >= 80 else "normal"
                
                with st.container(border=True):
                    st.markdown(f"### {row.iloc[0]}")
                    st.caption(f"Ticker: {row.iloc[1]}")
                    st.metric("AI Score", f"{score}pt", delta=f"{score-70}%", delta_color=color)
                    st.write(f"**分析コメント:**\n{row.iloc[3]}")
                    st.button(f"{row.iloc[1]} の詳細を表示", key=f"btn_{i}")
    else:
        st.warning("スプレッドシートにデータがありません。")
except Exception as e:
    st.error(f"データの読み込みに失敗しました。")

st.divider()

# --- 2. 資産管理（簡易表示） ---
st.subheader("💰 資産推移・ポートフォリオ")
tab1, tab2 = st.tabs(["資産チャート", "保有状況"])

with tab1:
    chart_data = pd.DataFrame({"評価額": [1000, 1010, 1005, 1020, 1025]}, index=["2/24", "2/25", "2/26", "2/27", "3/2"])
    st.line_chart(chart_data)

with tab2:
    st.write("保有銘柄リストをスプレッドシートに追加すると、ここに自動反映されます。")
