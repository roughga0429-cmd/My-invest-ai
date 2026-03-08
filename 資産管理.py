import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="資産管理 - My Invest AI Pro", layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.title("⚙️ System Settings")
    st.write(f"📅 最終更新: {datetime.date.today()}")
    st.divider()
    st.info("💡 **運用方針**: 地政学リスクを考慮したインフラ・ディフェンシブ銘柄の選定\n🎯 **目標**: 5年で1億円")

st.title("💰 資産管理・ポートフォリオ")

# --- URL設定 ---
portfolio_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=1796285252"
diag_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=1357398603"

# --- 1. 資産状況・ポートフォリオ ---
st.subheader("📊 現在の資産状況")
try:
    pf_df = pd.read_csv(portfolio_sheet_url)
    pf_df['評価額'] = pd.to_numeric(pf_df['評価額'], errors='coerce').fillna(0)
    pf_df['損益'] = pd.to_numeric(pf_df['損益'], errors='coerce').fillna(0)
    total_asset = pf_df['評価額'].sum()
    total_pl = pf_df['損益'].sum()
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.metric(label="現在の総評価額", value=f"¥ {total_asset:,.0f}", delta=f"¥ {total_pl:,.0f} (トータル損益)")
    with col_b:
        st.write("📋 **保有銘柄一覧**")
        valid_cols = [col for col in pf_df.columns if "Unnamed" not in str(col) and col != "AIポートフォリオ診断"]
        display_df = pf_df[valid_cols]
        st.dataframe(
            display_df,
            column_config={
                "購入単価": st.column_config.NumberColumn(format="¥%d"),
                "現在値": st.column_config.NumberColumn(format="¥%d"),
                "評価額": st.column_config.NumberColumn(format="¥%d"),
                "損益": st.column_config.NumberColumn(format="¥%d"),
                "最新ニュースお天気判定": st.column_config.TextColumn("AIお天気判定 🌤️", width="large"),
            },
            hide_index=True,
            use_container_width=True
        )
except Exception as e:
    st.warning(f"保有株データの読み込みに失敗しました: {e}")

st.divider()

# --- 2. 🤖 専属AIポートフォリオ診断 ---
st.subheader("🤖 専属AIポートフォリオ診断")
try:
    df_diag = pd.read_csv(diag_sheet_url, header=None)
    if not df_diag.empty:
        ai_advice = df_diag.iloc[0, 0]
        st.info(f"💡 **AI専属コンサルタントより**\n\n{ai_advice}")
    else:
        st.write("まだAIの診断結果がないみたいやわ。")
except Exception as e:
    st.error("AI診断データの読み込みエラーや！URLのgidが合ってるか確認してな。")

st.divider()

# --- 3. 年間配当金予測カレンダー ---
st.subheader("🗓️ 年間配当金予測カレンダー")
try:
    annual_yield = 0.03
    estimated_annual_dividend = total_asset * annual_yield
    months = [f"{i}月" for i in range(1, 13)]
    dividends = [0] * 12
    dividends[2] = estimated_annual_dividend * 0.4 
    dividends[5] = estimated_annual_dividend * 0.1 
    dividends[8] = estimated_annual_dividend * 0.4 
    dividends[11] = estimated_annual_dividend * 0.1
    chart_data = pd.DataFrame({"月": months, "予想配当金 (円)": dividends}).set_index("月")

    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        st.bar_chart(chart_data, color="#FFD700") 
    with col_c2:
        st.success("💰 **不労所得シミュレーション**")
        st.metric("年間予想配当金", f"¥ {int(estimated_annual_dividend):,.0f}")
        st.write(f"💡 ひと月あたり換算:\n**約 ¥ {int(estimated_annual_dividend/12):,.0f}**")
except Exception as e:
    st.write("配当金計算に失敗しました。")
