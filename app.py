import streamlit as st
import pandas as pd
import numpy as np

# 表示設定
st.set_page_config(page_title="My Invest AI", layout="wide")
st.title("🇯🇵 日本株 投資自動分析ボード")

# スプレッドシートのURL
sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=0"

# --- 1. 資産サマリーセクション（復活！） ---
st.header("📈 総資産サマリー")
col_a, col_b = st.columns([1, 2])

with col_a:
    # 評価額の表示（将来的にこれもシートから読めます）
    st.metric(label="現在の総評価額", value="1,025,300 JPY", delta="+2.5% (前日比)")
    st.write("📈 **資産推移の概況**")
    st.caption("AI分析に基づき、インフラとエンタメ株の比重を高めています。")

with col_b:
    # 資産推移グラフの生成
    chart_data = pd.DataFrame(
        np.random.randn(20, 1).cumsum() + 100, 
        columns=['資産評価額']
    )
    st.line_chart(chart_data)

st.divider()

# --- 2. AI注目銘柄セクション ---
try:
    df = pd.read_csv(sheet_url)
    st.header("🔥 AI注目銘柄サマリー")
    
    if not df.empty:
        # 銘柄ごとのカード表示
        cols = st.columns(len(df))
        for i, row in df.iterrows():
            with cols[i]:
                st.subheader(f"{row['銘柄名']}")
                st.caption(f"コード: {row['ティッカー']}")
                st.metric("AI分析スコア", f"{row['AI分析スコア']}点")
                st.info(f"**分析コメント:**\n\n{row['コメント']}")
        
        st.divider()
        st.subheader("📊 銘柄詳細データ一覧")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("スプレッドシートにデータがありません。")

except Exception as e:
    st.error("データの読み込み中にエラーが発生しました。")
