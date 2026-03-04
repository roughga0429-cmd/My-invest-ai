import streamlit as st
import pandas as pd
import datetime
import yfinance as yf # 👈 ★株価取得のための新兵器や！

st.set_page_config(page_title="My Invest AI Pro", layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.title("⚙️ System Settings")
    st.write(f"📅 最終更新: {datetime.date.today()}")
    st.divider()
    st.info("💡 **運用方針**: 地政学リスクを考慮したインフラ・ディフェンシブ銘柄の選定")

st.title("🇯🇵 日本株 投資自動分析ボード")

# --- URL設定 ---
ai_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=0"
portfolio_sheet_url = "https://docs.google.com/spreadsheets/d/1FPP88GmznB99b42aXS1mQPmR3au-PgbCe3FJ_soX4Os/export?format=csv&gid=1796285252"

# 💡 株価を爆速で取得するためのキャッシュ機能（1時間保存）
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker_code):
    try:
        # 日本株は「証券コード.T」にする必要があるねん
        tkr = yf.Ticker(f"{ticker_code}.T")
        hist = tkr.history(period="5d")
        if len(hist) >= 2:
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            diff = current - prev
            diff_pct = (diff / prev) * 100
            return current, diff, diff_pct
        return None, None, None
    except:
        return None, None, None

# --- 1. AI注目銘柄セクション（タブ廃止・フルオープン版） ---
try:
    df = pd.read_csv(ai_sheet_url)
    if not df.empty and "推奨期間" in df.columns:
        st.subheader("🔥 AI PickUp - 推奨銘柄リスト（全期間展開）")
        
        def display_term_section(term_label):
            term_df = df[df["推奨期間"].str.contains(term_label, na=False)]
            if not term_df.empty:
                st.markdown(f"#### 🎯 {term_label}目線")
                cols = st.columns(3)
                for i, (idx, row) in enumerate(term_df.iterrows()):
                    with cols[i % 3]:
                        try:
                            score = int(row["AI分析スコア"])
                        except:
                            score = 0
                            
                        color = "inverse" if score >= 80 else "normal"
                        curr, diff, diff_pct = fetch_stock_data(row['ティッカー'])

                        with st.container(border=True):
                            st.markdown(f"### {row['銘柄名']}")
                            st.caption(f"Ticker: {row['ティッカー']}")
                            
                            # スコアと株価を横並びに！
                            col1, col2 = st.columns(2)
                            col1.metric("AI Score", f"{score}pt", delta=f"{score-70}%", delta_color=color)
                            
                            if curr is not None:
                                col2.metric("現在値", f"¥{curr:,.0f}", f"{diff:+.0f}円 ({diff_pct:+.2f}%)")
                            else:
                                col2.metric("現在値", "取得エラー", "")
                                
                            st.write(f"**💡 根拠・コメント:**\n{row['根拠・コメント']}")
                st.divider()

        # タブを使わず、上から順番にドカーンと表示するで
        display_term_section("短期")
        display_term_section("中期")
        display_term_section("長期")
    else:
        st.warning("スプレッドシートの形式を確認してください")
except Exception as e:
    st.error(f"AIデータの読み込みに失敗しました: {e}")

# --- 以下はこれまでの機能そのままや！ ---
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
    with col_b:
        st.write("📋 **現在のポートフォリオ**")
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

# --- 3. AIポートフォリオ診断 ---
st.subheader("🤖 専属AI ポートフォリオ診断")
try:
    if "AIポートフォリオ診断" in pf_df.columns:
        advice = pf_df["AIポートフォリオ診断"].dropna().iloc[0]
        st.info(f"**【AIからのアドバイス】**\n\n{advice}")
except:
    pass

# --- 4. 年間配当金予測カレンダー ---
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
