import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="My Invest AI Pro", layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.title("⚙️ System Settings")
    st.write(f"📅 最終更新: {datetime.date.today()}")
    st.divider()
    st.info("💡 **運用方針**: 地政学リスクを考慮したインフラ・ディフェンシブ銘柄の選定")

st.title("🇯🇵 日本株 投資自動分析ボード")

# --- URL設定 ---
# AI分析シート (gid=0)
ai_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=0"
# 保有株シート (あなたのGIDを設定済み)
portfolio_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=1796285252"

# --- 1. AI注目銘柄セクション（タブ機能！） ---
try:
    df = pd.read_csv(ai_sheet_url)
    if not df.empty and "推奨期間" in df.columns:
        st.subheader("🔥 AI PickUp - 期間別・推奨銘柄リスト")
        tab_short, tab_mid, tab_long = st.tabs(["⚡ 短期 (1ヶ月)", "📈 中期 (半年)", "🌍 長期 (年単位)"])
        
        def display_term_cards(term_label, target_tab):
            with target_tab:
                term_df = df[df["推奨期間"].str.contains(term_label, na=False)]
                if not term_df.empty:
                    cols = st.columns(3)
                    for i, (idx, row) in enumerate(term_df.iterrows()):
                        with cols[i % 3]:
                            try:
                                score = int(row["AI分析スコア"])
                            except:
                                score = 0
                            color = "inverse" if score >= 80 else "normal"
                            with st.container(border=True):
                                st.markdown(f"### {row['銘柄名']}")
                                st.caption(f"Ticker: {row['ティッカー']}")
                                st.metric("AI Score", f"{score}pt", delta=f"{score-70}%", delta_color=color)
                                st.write(f"**💡 根拠・コメント:**\n{row['根拠・コメント']}")
                else:
                    st.write(f"{term_label}の推奨銘柄は現在ありません。")

        display_term_cards("短期", tab_short)
        display_term_cards("中期", tab_mid)
        display_term_cards("長期", tab_long)
    else:
        st.warning("スプレッドシートの形式を確認してください（推奨期間列が必要です）")
except Exception as e:
    st.error(f"AIデータの読み込みに失敗しました: {e}")

st.divider()

# --- 2. 資産管理 ---
st.subheader("💰 資産推移・ポートフォリオ")
try:
    pf_df = pd.read_csv(portfolio_sheet_url)
    pf_df['評価額'] = pd.to_numeric(pf_df['評価額'], errors='coerce').fillna(0)
    pf_df['損益'] = pd.to_numeric(pf_df['損益'], errors='coerce').fillna(0)
    
    total_asset = pf_df['評価額'].sum()
    total_pl = pf_df['損益'].sum()
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.metric(label="現在の総評価額", value=f"¥ {total_asset:,.0f}", delta=f"¥ {total_pl:,.0f} (トータル損益)")
        st.caption("※株価は約20分遅れで自動更新されます")
    with col_b:
        st.write("📋 **現在のポートフォリオ**")
        
        # 不要な列を省いて表示用のデータを作る
        valid_cols = [col for col in pf_df.columns if "Unnamed" not in str(col) and col != "AIポートフォリオ診断"]
        display_df = pf_df[valid_cols]
        
        st.dataframe(
            display_df,
            column_config={
                "購入単価": st.column_config.NumberColumn(format="¥%d"),
                "現在値": st.column_config.NumberColumn(format="¥%d"),
                "評価額": st.column_config.NumberColumn(format="¥%d"),
                "損益": st.column_config.NumberColumn(format="¥%d"),
                # 👇 新しいお天気判定の列を広めに表示する設定を追加したで！
                "最新ニュースお天気判定": st.column_config.TextColumn("AIお天気判定 🌤️", width="large"),
            },
            hide_index=True,
            use_container_width=True
        )
except Exception as e:
    st.warning(f"保有株データの読み込みに失敗しました: {e}")

# --- 3. AIポートフォリオ診断 ---
st.divider()
st.subheader("🤖 専属AI ポートフォリオ診断")
try:
    if "AIポートフォリオ診断" in pf_df.columns:
        advice = pf_df["AIポートフォリオ診断"].dropna().iloc[0]
        st.info(f"**【AIからのアドバイス
