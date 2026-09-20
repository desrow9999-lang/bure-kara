import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="ブレてからが本番。",
    page_icon="📸",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0d0f19;
        color: #fafaef;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #e6ff6f 0%, #a335f7 50%, #0ec499 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #9ca3af;
        font-size: 0.95rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .step-header {
        font-weight: 700;
        font-size: 1.05rem;
        color: #e5e7eb;
        margin-top: 2rem;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">ブレてからが本番。 <span style="font-size: 1.2rem;">✨</span></p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">微小なブレから、皆が目を引く強烈な1枚へ！失敗作を高衝撃変形エンジンでランダムアップサイクル。</p>', unsafe_allow_html=True)

st.markdown('<p class="step-header">ステップ1: 失敗写真をアップロード</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    try:
        # 画像を安全に読み込み
        image = Image.open(uploaded_file)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎲 ガチャを回して強烈な1枚を生成する"):
            st.success("✨ ガチャが正常に動作しました！（現在、安定性確認テスト中）")
            # まずは確実にエラーを出さずに画像を表示できることを確認するため、元の画像を表示します
            st.image(image, caption="プレビュー画像", use_column_width=True)
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    st.info("💡 まずはスマホのブレた写真を選択してください。")
