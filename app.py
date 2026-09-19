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
st.write("ピンボケして消そうとしていたその写真は、あなただけの抽象アート素材。失敗を、作品に変えよう。")

# 画像のアップロード
uploaded_file = st.file_uploader("スマホからピンボケ写真を選ぶ...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 画像を開く
    original_image = Image.open(uploaded_file)
    
    st.subheader("1. 元のピンボケ写真")
    st.image(original_image, use_container_width=True)
    
    st.markdown("---")
    st.subheader("2. アートに生まれ変わった素材")
    
    # ユーザーがエフェクトを選べるようにする
    effect_type = st.selectbox(
        "変換スタイルを選んでください",
        ["ネオン・ブラー (幻想的な光)", "モノクロ・エッジ (退廃的な質感)", "サイケデリック・シフト (色を反転)"]
    )
    
    # 画像の加工処理
    processed_image = original_image.copy()
    
    if effect_type == "ネオン・ブラー (幻想的な光)":
        # 極端にぼかして、色調を鮮やかにする
        processed_image = processed_image.filter(ImageFilter.GaussianBlur(radius=25))
        processed_image = ImageOps.autocontrast(processed_image, cutoff=10)
        
    elif effect_type == "モノクロ・エッジ (退廃的な質感)":
        # モノクロにしてコントラストを強くする
        processed_image = ImageOps.grayscale(processed_image)
        processed_image = processed_image.filter(ImageFilter.FIND_EDGES)
        processed_image = ImageOps.invert(processed_image)
        
    elif effect_type == "サイケデリック・シフト (色を反転)":
        # 色を反転させてぼかす
        processed_image = ImageOps.invert(processed_image.convert("RGB"))
        processed_image = processed_image.filter(ImageFilter.BoxBlur(radius=10))

    # 加工後の画像を表示
    st.image(processed_image, caption=f"スタイル: {effect_type}", use_container_width=True)
    
    # ダウンロードボタン（Canvaに取り込みやすくする）
    img_byte_arr = io.BytesIO()
    processed_image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    st.download_button(
        label="📥 この素材をダウンロードしてCanvaで使う",
        data=img_byte_arr,
        file_name="buretekara_material.png",
        mime="image/png"
    )
    
    st.info("💡 ヒント：ダウンロードした画像をCanvaアプリで開き、お気に入りのテンプレートや文字と組み合わせると、最高におしゃれなポスターやスマホ壁紙になります！")
