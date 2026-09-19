import streamlit as st
from PIL import Image, ImageFilter, ImageOps
import io

# ページの設定（ワイドすぎずスッキリ見せる）
st.set_page_config(
    page_title="ブレてからが本番",
    page_icon="✨",
    layout="centered"
)

# スタイリッシュなカスタムCSS（余白とフォントの調整）
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
st.markdown('<p class="sub-title">不要なピンボケ写真を、洗練された抽象アート素材へアップサイクル。</p>', unsafe_allow_html=True)

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
    
    # --- STEP 2: スタイルの選択 ---
    st.markdown('<p class="step-header">🎨 Step 2. 変換スタイルを選ぶ</p>', unsafe_allow_html=True)
    effect_choice = st.selectbox(
        "変換スタイル",
        ["ネオン・ブラー (幻想的な光)", "モノクロ・エッジ (退廃的な質感)", "サイケデリック・シフト (色を反転)"],
        label_visibility="collapsed"
    )
    
    processed_images = []
    
    # 画像処理
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        
        if effect_choice == "ネオン・ブラー (幻想的な光)":
            img = img.filter(ImageFilter.GaussianBlur(radius=25))
            img = ImageOps.autocontrast(img, cutoff=15)
        elif effect_choice == "モノクロ・エッジ (退廃的な質感)":
            img = ImageOps.grayscale(img)
            img = img.filter(ImageFilter.FIND_EDGES)
            img = ImageOps.invert(img)
        elif effect_choice == "サイケデリック・シフト (色を反転)":
            img = ImageOps.invert(img.convert("RGB"))
            img = img.filter(ImageFilter.BoxBlur(radius=12))
            
        processed_images.append(img)
    
    # コラージュ合成
    if processed_images:
        target_height = 400
        resized_imgs = []
        for img in processed_images:
            w, h = img.size
            new_w = int(w * (target_height / h))
            resized_imgs.append(img.resize((new_w, target_height)))
            
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
            label="✨ アート素材を保存する",
            data=img_byte_arr,
            file_name="buretekara_art.png",
            mime="image/png",
            use_container_width=True
        )
        
        st.info("💡 **次のステップ**: 保存した画像をCanvaアプリで開き、お気に入りの文字やレイアウトを重ねてデザインを完成させましょう！")

else:
    # 写真が選択されていない時のガイド
    st.info("👆 上のボックスをタップして、スマホの写真フォルダからピンボケ写真を選んでみてください。")
