import streamlit as st
from PIL import Image, ImageFilter, ImageOps
import random
import io

# ページの設定
st.set_page_config(
    page_title="ブレてからが本番",
    page_icon="✨",
    layout="centered"
)

# スタイリッシュなカスタムCSS
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }
    .step-header {
        font-weight: 700;
        font-size: 1.1rem;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .stButton button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown('<p class="main-title">✨ ブレてからが本番</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">不要なピンボケ写真を、スタイリッシュな抽象アートへ昇華。</p>', unsafe_allow_html=True)

# --- STEP 1: 写真の選択 ---
st.markdown('<p class="step-header">📁 Step 1. 写真を選ぶ</p>', unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "ピンボケ写真を複数選択してください", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:
    st.success(f"selected: {len(uploaded_files)}枚の写真がセットされました")
    
    # ガチャを回すボタン（押すたびに新しいランダムアートになる）
    st.markdown('<p class="step-header">🎨 Step 2. アートを生成する</p>', unsafe_allow_html=True)
    
    # セッション状態でガチャのトリガーを管理
    if 'seed' not in st.session_state:
        st.session_state.seed = 0

    if st.button("🎲 別のアートスタイルをガチャる（再生成）", use_container_width=True):
        st.session_state.seed += 1

    processed_images = []
    
    # スタイリッシュなエフェクト候補から、写真ごとにランダムで1つを綺麗に適用
    styles = ["neon_blur", "mirror_art", "edge_art", "retro_dot"]
    
    for i, uploaded_file in enumerate(uploaded_files):
        img = Image.open(uploaded_file).convert("RGB")
        w, h = img.size
        
        # 写真ごとに洗練されたどれか一つのスタイルを選択
        chosen_style = random.choice(styles)
        
        if chosen_style == "neon_blur":
            # 幻想的なネオン・ブラー
            img = img.filter(ImageFilter.GaussianBlur(radius=20))
            img = ImageOps.autocontrast(img, cutoff=20)
            
        elif chosen_style == "mirror_art":
            # 左右対称のスタイリッシュなミラー
            half = img.crop((0, 0, w // 2, h))
            flipped = half.transpose(Image.FLIP_LEFT_RIGHT)
            img = Image.new('RGB', (w, h))
            img.paste(half, (0, 0))
            img.paste(flipped, (w // 2, 0))
            img = img.filter(ImageFilter.GaussianBlur(radius=4))
            
        elif chosen_style == "edge_art":
            # カッコいいモノクロ線画風
            img = ImageOps.grayscale(img).filter(ImageFilter.FIND_EDGES)
            img = ImageOps.invert(img)
            img = img.convert("RGB")
            
        elif chosen_style == "retro_dot":
            # おしゃれなレトロ・ピクセル
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
        collage = Image.new('RGB', (total_width, target_height))
        
        x_offset = 0
        for im in resized_imgs:
            collage.paste(im, (x_offset, 0))
            x_offset += im.width
            
        # --- STEP 3: プレビュー & ダウンロード ---
        st.markdown('<p class="step-header">📥 Step 3. ダウンロードしてCanvaへ</p>', unsafe_allow_html=True)
        st.image(collage, use_container_width=True)
        
        # ダウンロードデータ作成
        img_byte_arr = io.BytesIO()
        collage.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        st.download_button(
            label="✨ このアート素材を保存する",
            data=img_byte_arr,
            file_name="buretekara_art.png",
            mime="image/png",
            use_container_width=True
        )
        
        st.info("💡 **ヒント**: 「別のアートスタイルをガチャる」ボタンを押すと、一瞬で別のカッコいいデザインに生まれ変わります！")

else:
    st.info("👆 上のボックスをタップして、スマホの写真フォルダからピンボケ写真を選んでみてください。")
