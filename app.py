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
    </style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown('<p class="main-title">✨ ブレてからが本番</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">写真をアップするだけで、AIが無限のスタイルで抽象アートへ自動変換。</p>', unsafe_allow_html=True)

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
    
    processed_images = []
    
    # 完全にスタイル選択をなくし、無限のランダムエフェクトを自動適用
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file).convert("RGB")
        w, h = img.size
        
        # 1. ランダムなぼかし
        if random.choice([True, False]):
            img = img.filter(ImageFilter.GaussianBlur(radius=random.randint(10, 45)))
        
        # 2. ランダムな色反転
        if random.choice([True, False]):
            img = ImageOps.invert(img)
            
        # 3. ランダムなコントラスト調整
        if random.choice([True, False]):
            img = ImageOps.autocontrast(img, cutoff=random.randint(5, 30))
            
        # 4. ランダムなドット絵・モザイク化
        if random.choice([True, False]):
            p_size = random.randint(10, 60)
            img_s = img.resize((max(1, w // p_size), max(1, h // p_size)), Image.Resampling.NEAREST)
            img = img_s.resize((w, h), Image.Resampling.NEAREST)
            
        # 5. ランダムな左右ミラー反転
        if random.choice([True, False]):
            half = img.crop((0, 0, w // 2, h))
            flipped = half.transpose(Image.FLIP_LEFT_RIGHT)
            img.paste(flipped, (w // 2, 0))
            
        # 6. ランダムなエッジ（線画風）抽出
        if random.choice([True, False]):
            img = ImageOps.grayscale(img).filter(ImageFilter.FIND_EDGES)
            img = ImageOps.invert(img)
            img = img.convert("RGB")
            
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
            
        # --- STEP 2: プレビュー & ダウンロード ---
        st.markdown('<p class="step-header">📥 Step 2. ダウンロードしてCanvaへ</p>', unsafe_allow_html=True)
        st.image(collage, use_container_width=True)
        
        # ダウンロードデータ作成
        img_byte_arr = io.BytesIO()
        collage.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        st.download_button(
            label="✨ 無限アート素材を保存する",
            data=img_byte_arr,
            file_name="buretekara_infinite_art.png",
            mime="image/png",
            use_container_width=True
        )
        
        st.info("💡 **ヒント**: 画面を再読み込み（リロード）するたびに、完全に異なる無限のスタイルで新しいアートが生成されます！気に入るまで何度でも楽しめます。")

else:
    st.info("👆 上のボックスをタップして、スマホの写真フォルダからピンボケ写真を選んでみてください。")
