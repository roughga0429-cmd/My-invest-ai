import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="My Invest AI", layout="wide")
st.title("🇯🇵 日本株 投資自動分析ボード")

# スプレッドシートのURL
sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=0"

# --- 1. 資産サマリーセクション ---
st.header("📈 総資産サマリー")
col_a, col_b = st.columns([1, 2])

with col_a:
    st.metric(label="現在の評価額", value="1,000,000 JPY", delta="運用開始待ち")
    st.info("※現在、運用開始前のテストデータ表示モードです。")

with col_b:
    st.write("📈 **過去100日の推移（シミュレーション）**")
    # テストデータ用のダミーグラフ
    chart_data = pd.DataFrame(np.random.randn(100).cumsum() + 100, columns=['資産推移'])
    st.line_chart(chart_data)

st.divider()

# --- 2. AI注目銘柄セクション ---
try:
    df = pd.read_csv(sheet_url)
    st.header("🔥 最新のAI分析（直近3件）")
    
    if not df.empty:
        # 【重要】最新の3件だけを取得し、それ以外は表示しない
        recent_df = df.tail(3).iloc[::-1] # 下から3つを逆順（最新順）で取得
        
        cols = st.columns(3)
        for i, (idx, row) in enumerate(recent_df.iterrows()):
            with cols[i]:
                with st.container(border=True): # 枠線をつけて見やすく
                    st.subheader(f"{row.iloc[0]}")
                    st.write(f"**コード:** {row.iloc[1]}")
                    st.metric("AIスコア", f"{row.iloc[2]}点")
                    st.caption("AIコメント:")
                    st.write(f"{row.iloc[3]}")
    else:
        st.write("データがありません。")
except Exception as e:
    st.error(f"読み込みエラーが発生しました。")
