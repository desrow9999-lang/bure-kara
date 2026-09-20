import random
import io
import numpy as np
import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

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
        letter-spacing: -0.01em;
    }
    [data-testid="stFileUploader"] {
        background-color: #111827;
        border: 1px dashed #374151;
        border-radius: 12px;
        padding: 1rem;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
    }
    .stButton button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.8rem 1rem;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">ブレてからが本番。 <span style="font-size: 1.2rem;">✨</span></p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">微小なブレから、皆が目を引く強烈な1枚へ！失敗作を高衝撃変形エンジンでアップサイクル。</p>', unsafe_allow_html=True)

def apply_impact_art(image, style_choice):
    image = image.convert("RGB")
    
    image = ImageEnhance.Contrast(image).enhance(2.8)
    image = ImageEnhance.Color(image).enhance(2.2)
    
    if style_choice == "グリッチ・ポップ":
        edges = image.filter(ImageFilter.FIND_EDGES)
        inverted = ImageOps.invert(edges)
        image = Image.blend(image, inverted, alpha=0.5)
        image = image.filter(ImageFilter.SHARPEN)
        
    elif style_choice == "ネオン・フロー":
        blurred = image.filter(ImageFilter.GaussianBlur(radius=4))
        edges = image.filter(ImageFilter.FIND_EDGES)
        image = Image.blend(blurred, edges, alpha=0.7)
        image = ImageOps.solarize(image, threshold=100)
        
    elif style_choice == "抽象的破片":
        image = image.quantize(colors=6).convert("RGB")
        image = image.filter(ImageFilter.DETAIL)
        image = image.filter(ImageFilter.FIND_EDGES)
        
    elif style_choice == "カラーウェーブ":
        for _ in range(2):
            image = image.filter(ImageFilter.SMOOTH_MORE)
        image = ImageOps.solarize(image, threshold=128)
        image = ImageEnhance.Brightness(image).enhance(1.3)
        
    return image

st.markdown('<p class="step-header">ステップ1: 失敗写真をアップロード</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    
    st.markdown('<p class="step-header">ステップ2: 変換スタイルを選択</p>', unsafe_allow_html=True)
    style_choice = st.selectbox(
        "目を引く強烈なスタイルを選んでください",
        ["グリッチ・ポップ", "ネオン・フロー", "抽象的破片", "カラーウェーブ"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔥 強烈な1枚を生成する"):
        with st.spinner("高衝撃変形エンジン作動中... 🚀"):
            processed_image = apply_impact_art(original_image, style_choice)
            
        st.success("✨ 強烈な1枚の生成が完了しました！")
        
        st.image(processed_image, caption=f"「{style_choice}」でアップサイクルされた作品", use_column_width=True)
        
        buf = io.BytesIO()
        processed_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.download_button(
            label="📥 この強烈な1枚をダウンロード (PNG)",
            data=byte_im,
            file_name=f"bure-kara-impact-{style_choice}.png",
            mime="image/png"
        )
else:
    st.info("💡 まずはスマホのブレた写真を選択してください。小さなブレほど、強烈なアートに生まれ変わります！")
