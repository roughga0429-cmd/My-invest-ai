import streamlit as st
import pandas as pd

st.set_page_config(page_title="My Invest AI", layout="wide")
st.title("🇯🇵 日本株 投資自動分析ボード")

# スプレッドシートのURL
sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=0"

# --- 1. 資産サマリー（手入力連携モード） ---
st.header("📈 総資産サマリー")
# ここは一旦、あなたが「今いくら持っているか」を入力できるスライダーにしました
balance = st.sidebar.number_input("現在の投資元本を入力 (JPY)", value=1000000)
st.metric(label="現在の評価額", value=f"{balance:,} JPY", delta="運用開始待ち")

st.info("※現在、運用開始前のためグラフは非表示にしています。実際に株を購入されたら、推移を記録できるようにしましょう。")

st.divider()

# --- 2. AI注目銘柄（スプレッドシート完全連動） ---
try:
    df = pd.read_csv(sheet_url)
    st.header("🔥 AI注目銘柄サマリー")
    
    if not df.empty and len(df.columns) >= 4:
        cols = st.columns(len(df))
        for i, row in df.iterrows():
            with cols[i]:
                st.subheader(f"{row['銘柄名']}")
                st.caption(f"コード: {row['ティッカー']}")
                st.metric("AI分析スコア", f"{row['AI分析スコア']}点")
                st.info(f"**分析コメント:**\n\n{row['コメント']}")
    else:
        st.write("スプレッドシートに有効なデータがありません。")

except Exception as e:
    st.error("データの読み込みに失敗しました。スプレッドシートが『リンクを知っている全員：閲覧者』になっているか確認してください。")
