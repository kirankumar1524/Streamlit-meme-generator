import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Meme Generator", layout="centered")
st.title("🎉 Meme Generator")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    top_text = st.text_input("Top Text", "")
    bottom_text = st.text_input("Bottom Text", "")

    font_size = st.slider("Font Size", 20, 100, 40)
    font_color = st.color_picker("Font Color", "#FFFFFF")

    if st.button("Generate Meme"):
        img = image.convert("RGB")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        def get_text_size(draw_obj, text, font):
            bbox = draw_obj.textbbox((0, 0), text, font=font)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            return width, height

        def draw_text_with_outline(draw_obj, text, position, font, text_color, outline_color="black", outline_width=2):
            x, y = position
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw_obj.text((x + dx, y + dy), text, font=font, fill=outline_color)
            draw_obj.text((x, y), text, font=font, fill=text_color)

        if top_text:
            text_width, text_height = get_text_size(draw, top_text, font)
            x = (img.width - text_width) / 2
            y = 10
            draw_text_with_outline(draw, top_text.upper(), (x, y), font, font_color)

        if bottom_text:
            text_width, text_height = get_text_size(draw, bottom_text, font)
            x = (img.width - text_width) / 2
            y = img.height - text_height - 10
            draw_text_with_outline(draw, bottom_text.upper(), (x, y), font, font_color)

        st.image(img, caption="Generated Meme", use_column_width=True)

        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        byte_im = buf.getvalue()

        st.download_button(
            label="Download Meme",
            data=byte_im,
            file_name="meme.jpg",
            mime="image/jpeg"
        )
else:
    st.info("Upload an image to start creating a meme!")
