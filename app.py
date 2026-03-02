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

# --- URL設定 ---
# ① AI分析データのURL (gid=0)
ai_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=0"
# ② 保有株データのURL (あなたのGID適用済み)
portfolio_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=1796285252"

# --- 1. AI注目銘柄セクション ---
try:
    df = pd.read_csv(ai_sheet_url)
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
    st.error(f"AI分析データの読み込みに失敗しました。")

st.divider()

# --- 2. 資産管理（本物と連動！） ---
st.subheader("💰 資産推移・ポートフォリオ")

try:
    # 保有株データを読み込む
    pf_df = pd.read_csv(portfolio_sheet_url)
    
    # 評価額と損益の合計を計算
    total_asset = pf_df['評価額'].sum()
    total_pl = pf_df['損益'].sum()
    
    # プラスマイナスで色を変えるための処理
    delta_color = "normal" if total_pl >= 0 else "inverse"
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        # トータル資産の表示
        st.metric(
            label="現在の総評価額", 
            value=f"¥ {total_asset:,.0f}", 
            delta=f"¥ {total_pl:,.0f} (トータル損益)",
            delta_color=delta_color
        )
        st.caption("※株価は約20分遅れで自動更新されます")
        
    with col_b:
        # 保有株リストを綺麗な表で表示
        st.write("📋 **現在のポートフォリオ**")
        
        # ここが途切れていた部分です！
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
    st.warning("保有株データの読み込みに失敗しました。スプレッドシートの「保有株」シートにデータが正しく入力されているか確認してください。")
