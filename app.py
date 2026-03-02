import streamlit as st
import pandas as pd

# 表示設定：iPadで見やすいワイドレイアウト
st.set_page_config(page_title="My Invest AI", layout="wide")
st.title("🇯🇵 日本株 投資自動分析ボード")

# あなたが作成したスプレッドシートのURL（自動連携用）
sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=0"

try:
    # スプレッドシートから最新データを読み込み
    df = pd.read_csv(sheet_url)
    
    # 資産メトリクス（スプレッドシートのデータに基づき将来的に拡張可能）
    st.header("📈 AI注目銘柄サマリー")
    
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
        # データ一覧表
        st.subheader("📊 銘柄詳細データ一覧")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("スプレッドシートにデータがありません。明日の朝の更新をお待ちください。")

except Exception as e:
    st.error("データの読み込み中にエラーが発生しました。")
    st.info("【確認】スプレッドシートの共有設定が「リンクを知っている全員」になっていますか？")
    st.write(f"詳細エラー: {e}")

st.sidebar.markdown(f"### 📱 アプリステータス\n自動連携モード: **ON**")
st.sidebar.write("最終更新確認: 2026-03-02")
