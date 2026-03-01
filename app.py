import streamlit as st
import pandas as pd
import numpy as np

# iPad向けの表示設定
st.set_page_config(page_title="My Invest AI", layout="wide")

# タイトル
st.title("🇯🇵 日本株 投資パートナー")

# --- 資産状況セクション ---
st.header("📈 総資産サマリー")
col_a, col_b = st.columns([1, 1])
with col_a:
    st.metric(label="現在の評価額", value="1,000,000 JPY", delta="準備完了")
with col_b:
    # 資産推移のサンプルグラフ
    chart_data = pd.DataFrame(np.random.randn(7, 1).cumsum() + 100, columns=['資産推移'])
    st.line_chart(chart_data)

st.divider()

# --- 本日の注目株トップ3 ---
st.header("🔥 AI厳選：本日の注目株TOP3")
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("1. バンダイナムコ (7832)")
    st.info("**根拠:** ガンプラの世界需要と強力なIP。")

with c2:
    st.subheader("2. 三菱電機 (6503)")
    st.info("**根拠:** AIデータセンター向けの電力設備需要。")

with c3:
    st.subheader("3. ハピネット (7552)")
    st.info("**根拠:** ガチャガチャのインバウンド需要。")
