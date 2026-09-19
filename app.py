import streamlit as st
from PIL import Image, ImageFilter, ImageOps
import random
import io

# ページの設定
st.set_page_config(
    page_title="ブレてからが本番",
    page_icon="📸",
    layout="centered"
)

# プロ仕様のモダンなダーク＆ガラスモーフィズムCSS
st.markdown("""
    <style>
    /* 全体の背景とフォントの洗練 */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* ヘッダーのグラデーション文字 */
    .main-title {
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
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
    
    /* セクションヘッダー */
    .step-header {
        font-weight: 700;
        font-size: 1.05rem;
        color: #e5e7eb;
        margin-top: 2rem;
        margin-bottom: 0.75rem;
        letter-spacing: -0.01em;
    }
    
    /* アップローダーのカスタマイズ（枠線を綺麗に） */
    [data-testid="stFileUploader"] {
        background-color: #111827;
        border: 1px dashed #374151;
        border-radius: 12px;
        padding: 1rem;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
    }
    
    /* ボタンスタイルのリッチ化 */
    .stButton button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1rem;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.5);
        transform: translateY(-1px);
    }
    
    /* ダウンロードボタンの特別感 */
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    [data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(135deg, #047857 0%, #059669 100%);
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.5);
    }
    
    /* インフォボックスのダーク調 */
    .stAlert {
        background-color: #1f2937 !important;
        color: #f3f4f6 !important;
        border: 1px solid #374151 !important;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown('<p class="main-title">📸 ブレてからが本番</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">不要なピンボケ写真を、最先端の抽象アート素材へ昇華する。</p>', unsafe_allow_html=True)

# --- STEP 1: 写真の選択 ---
st.markdown('<p class="step-header">01. 写真をインポート</p>', unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "ピンボケ写真を複数選択してください", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:
    st.success(f"✨ 成功: {len(uploaded_files)}枚の写真が読み込まれました")
    
    # ガチャを回すボタン
    st.markdown('<p class="step-header">02. アートスタイル・ガチャ</p>', unsafe_allow_html=True)
    
    if 'seed' not in st.session_state:
        st.session_state.seed = 0

    if st.button("🎲 別のアートスタイルを再生成する", use_container_width=True):
        st.session_state.seed += 1

    processed_images = []
    styles = ["neon_blur", "mirror_art", "edge_art", "retro_dot"]
    
    for i, uploaded_file in enumerate(uploaded_files):
        img = Image.open(uploaded_file).convert("RGB")
        w, h = img.size
        
        # ガチャごとにランダムなスタイルを決定
        chosen_style = random.choice(styles)
        
        if chosen_style == "neon_blur":
            img = img.filter(ImageFilter.GaussianBlur(radius=25))
            img = ImageOps.autocontrast(img, cutoff=15)
            
        elif chosen_style == "mirror_art":
            half = img.crop((0, 0, w // 2, h))
            flipped = half.transpose(Image.FLIP_LEFT_RIGHT)
            img = Image.new('RGB', (w, h))
            img.paste(half, (0, 0))
            img.paste(flipped, (w // 2, 0))
            img = img.filter(ImageFilter.GaussianBlur(radius=4))
            
        elif chosen_style == "edge_art":
            gray = ImageOps.grayscale(img)
            edges = gray.filter(ImageFilter.FIND_EDGES)
            inverted = ImageOps.invert(edges)
            img = ImageOps.autocontrast(inverted, cutoff=5).convert("RGB")
            
        elif chosen_style == "retro_dot":
            p_size = 20
            img_s = img.resize((max(1, w // p_size), max(1, h // p_size)), Image.Resampling.NEAREST)
            img = img_s.resize((w, h), Image.Resampling.NEAREST)
            
        processed_images.append(img)
    
    # コラージュ合成
    if processed_images:
        target_height = 400
        resized_imgs = []
        for img in processed_images:
            w, h = img.size
            new_w = int(w * (target_height / h))
            resized_imgs.append(img.resize((new_w, target_height), Image.Resampling.LANCZOS))
            
        total_width = sum(im.width for im in resized_imgs)
        collage = Image.new('RGB', (total_width, target_height), (15, 23, 42)) # ダークな背景色に合わせる
        
        x_offset = 0
        for im in resized_imgs:
            collage.paste(im, (x_offset, 0))
            x_offset += im.width
            
        # --- STEP 3: プレビュー & ダウンロード ---
        st.markdown('<p class="step-header">03. プレビュー & エクスポート</p>', unsafe_allow_html=True)
        st.image(collage, use_container_width=True)
        
        # ダウンロードデータ作成
        img_byte_arr = io.BytesIO()
        collage.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        st.download_button(
            label="💾 アート素材をダウンロード (PNG)",
            data=img_byte_arr,
            file_name="buretekara_art.png",
            mime="image/png",
            use_container_width=True
        )
        
        st.info("💡 **Tips**: 「再生成する」ボタンを押すと、いつでも別のデザインパターンにガチャを回せます。")

else:
    st.info("👆 上のボックスに写真をドラッグ＆ドロップ、またはタップして選択してください。")
