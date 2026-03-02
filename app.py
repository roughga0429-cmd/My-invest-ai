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
ai_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=0"
portfolio_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=1796285252" # あなたのGID適用済み

# --- 1. AI注目銘柄セクション（タブ機能追加！） ---
try:
    df = pd.read_csv(ai_sheet_url)
    if not df.empty and "推奨期間" in df.columns:
        st.subheader("🔥 AI PickUp - 期間別・推奨銘柄リスト")
        
        # 短期・中期・長期の3つのタブを作成
        tab_short, tab_mid, tab_long = st.tabs(["⚡ 短期 (1ヶ月)", "📈 中期 (半年)", "🌍 長期 (年単位)"])
        
        # タブの中にカードを表示する関数
        def display_stocks_by_term(term_keyword, target_tab):
            with target_tab:
                # 該当する期間の銘柄だけを絞り込み
                term_df = df[df["推奨期間"].str.contains(term_keyword, na=False)]
                
                if not term_df.empty:
                    cols = st.columns(len(term_df))
                    for i, (idx, row) in enumerate(term_df.iterrows()):
                        with cols[i]:
                            try:
                                score = int(row["AI分析スコア"])
                            except:
                                score = 0 # 変換エラー回避
                            
                            color = "inverse" if score >= 80 else "normal"
                            with st.container(border=True):
                                st.markdown(f"### {row['銘柄名']}")
                                st.caption(f"Ticker: {row['ティッカー']}")
                                st.metric("AI Score", f"{score}pt", delta=f"{score-70}%", delta_color=color)
                                st.write(f"**💡 根拠・コメント:**\n{row['根拠・コメント']}")
                else:
                    st.write("この期間の推奨銘柄は現在ありません。")

        # 各タブに表示処理を割り当て
        display_stocks_by_term("短期", tab_short)
        display_stocks_by_term("中期", tab_mid)
        display_stocks_by_term("長期", tab_long)

    else:
        st.warning("スプレッドシートのデータ形式が古いか、データがありません。GASを再実行してください。")
except Exception as e:
    st.error("AI分析データの読み込みに失敗しました。")

st.divider()

# --- 2. 資産管理 ---
st.subheader("💰 資産推移・ポートフォリオ")

try:
    pf_df = pd.read_csv(portfolio_sheet_url)
    total_asset = pf_df['評価額'].sum()
    total_pl = pf_df['損益'].sum()
    delta_color = "normal" if total_pl >= 0 else "inverse"
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.metric(
            label="現在の総評価額", 
            value=f"¥ {total_asset:,.0f}", 
            delta=f"¥ {total_pl:,.0f} (トータル損益)",
            delta_color=delta_color
        )
        st.caption("※株価は約20分遅れで自動更新されます")
        
    with col_b:
        st.write("📋 **現在のポートフォリオ**")
        st.dataframe(
            pf_df,
            column_config={
                "購入単価": st.column_config.NumberColumn(format="¥%d"),
                "現在値": st.column_config.NumberColumn(format="¥%d"),
                "評価額": st.column_config.NumberColumn(format="¥%d"),
                "損益": st.column_config.NumberColumn(format="¥%d"),
            },
            hide_index=True,
            use_container_width=True
        )

except Exception as e:
    st.warning("保有株データの読み込みに失敗しました。")
