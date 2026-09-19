import streamlit as st
from PIL import Image, ImageFilter, ImageOps
import io

# ページの設定
st.set_page_config(
    page_title="ブレてからが本番",
    page_icon="📸",
    layout="centered"
)

# タイトルとコンセプト
st.title("📸 ブレてからが本番")
st.write("複数のピンボケ写真を組み合わせて、世界に一つだけの抽象アート・コラージュを作ろう！")

# 複数ファイルのアップロード
uploaded_files = st.file_uploader(
    "スマホからピンボケ写真を複数選んでください（複数選択可）...", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.subheader(f"選択された写真: {len(uploaded_files)}枚")
    
    # ユーザーがエフェクトを選べるようにする
    effect_choice = st.selectbox(
        "全体に適用する変換スタイル",
        ["ネオン・ブラー (幻想的な光)", "モノクロ・エッジ (退廃的な質感)", "サイケデリック・シフト (色を反転)"]
    )
    
    processed_images = []
    
    # アップロードされた全画像を処理
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        
        if effect_choice == "ネオン・ブラー (幻想的な光)":
            img = img.filter(ImageFilter.GaussianBlur(radius=20))
            img = ImageOps.autocontrast(img, cutoff=10)
        elif effect_choice == "モノクロ・エッジ (退廃的な質感)":
            img = ImageOps.grayscale(img)
            img = img.filter(ImageFilter.FIND_EDGES)
            img = ImageOps.invert(img)
        elif effect_choice == "サイケデリック・シフト (色を反転)":
            img = ImageOps.invert(img.convert("RGB"))
            img = img.filter(ImageFilter.BoxBlur(radius=10))
            
        processed_images.append(img)
    
    # 複数画像を横並びのコラージュ画像に合成する処理
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
            
        st.subheader("🎨 生成されたコラージュアート素材")
        st.image(collage, use_container_width=True)
        
        # ダウンロードボタン
        img_byte_arr = io.BytesIO()
        collage.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        st.download_button(
            label="📥 このコラージュ素材をダウンロードしてCanvaで使う",
            data=img_byte_arr,
            file_name="buretekara_collage.png",
            mime="image/png"
        )
        
        st.info("💡 ヒント：このダウンロードした素材をCanvaアプリで開き、お気に入りのフォントやイラストを乗せるだけで、一瞬でおしゃれなデザインが完成します！")
