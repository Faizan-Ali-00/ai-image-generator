import os
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered",
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎨 AI Image Generator")
st.write("Turn your ideas into images with AI.")


# --------------------------------------------------
# CHECK HUGGING FACE TOKEN
# --------------------------------------------------

if not HF_TOKEN:
    st.error(
        "Hugging Face token not found. "
        "Make sure your .env file contains HF_TOKEN."
    )
    st.stop()


# --------------------------------------------------
# HUGGING FACE CLIENT
# --------------------------------------------------

client = InferenceClient(
    api_key=HF_TOKEN
)


# --------------------------------------------------
# PROMPT INPUT
# --------------------------------------------------

prompt = st.text_area(
    "Describe the image you want:",
    placeholder=(
        "Example: A futuristic city at sunset "
        "with flying cars and neon lights..."
    ),
    height=140,
)


# --------------------------------------------------
# GENERATE IMAGE
# --------------------------------------------------

if st.button("🎨 Generate Image", use_container_width=True):

    if not prompt.strip():

        st.warning("Please enter a description first.")

    else:

        with st.spinner("Generating your image..."):

            try:

                image = client.text_to_image(
                    prompt=prompt,
                    model="black-forest-labs/FLUX.1-schnell",
                )

                st.success("Image generated successfully!")

                # Display image
                st.image(
                    image,
                    caption="AI Generated Image",
                    use_container_width=True,
                )

                # Convert image to PNG bytes
                image_bytes = BytesIO()

                image.save(
                    image_bytes,
                    format="PNG",
                )

                image_bytes.seek(0)

                # Download button
                st.download_button(
                    label="⬇️ Download Image",
                    data=image_bytes.getvalue(),
                    file_name="ai_generated_image.png",
                    mime="image/png",
                    use_container_width=True,
                )

            except Exception as e:

                st.error("Image generation failed.")

                st.write(
                    "Please check your Hugging Face token "
                    "and internet connection."
                )

                st.code(str(e))


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Powered by Streamlit + Hugging Face FLUX"
)