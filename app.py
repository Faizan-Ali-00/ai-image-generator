python
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
    layout="centered"
)

# --------------------------------------------------
# CHECK HUGGING FACE TOKEN
# --------------------------------------------------

if not HF_TOKEN:
    st.error("Hugging Face API token is missing.")
    st.info("Add HF_TOKEN to your .env file or Streamlit Secrets.")
    st.stop()

# --------------------------------------------------
# HUGGING FACE MODEL
# --------------------------------------------------

MODEL_NAME = "black-forest-labs/FLUX.1-schnell"

client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎨 AI Image Generator")

st.write(
    "Turn your ideas into images using AI."
)

# --------------------------------------------------
# PROMPT
# --------------------------------------------------

prompt = st.text_area(
    "✍️ Enter your prompt",
    placeholder="Example: A futuristic city at night, cinematic lighting, highly detailed",
    height=120
)

# --------------------------------------------------
# GENERATE IMAGE
# --------------------------------------------------

if st.button("🎨 Generate Image", use_container_width=True):

    if not prompt.strip():
        st.warning("Please enter a prompt first.")
        st.stop()

    with st.spinner("Generating your image... Please wait."):
        try:
            image = client.text_to_image(
                prompt=prompt,
                model=MODEL_NAME
            )

            # --------------------------------------------------
            # DISPLAY IMAGE
            # --------------------------------------------------

            st.success("Image generated successfully!")

            st.image(
                image,
                caption="Generated Image",
                use_container_width=True
            )

            # --------------------------------------------------
            # CONVERT IMAGE TO BYTES
            # --------------------------------------------------

            image_bytes = BytesIO()
            image.save(image_bytes, format="PNG")

            # --------------------------------------------------
            # DOWNLOAD BUTTON
            # --------------------------------------------------

            st.download_button(
                label="⬇️ Download Image",
                data=image_bytes.getvalue(),
                file_name="ai_generated_image.png",
                mime="image/png",
                use_container_width=True
            )

        except Exception as e:
            st.error("Image generation failed.")
            st.exception(e)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Powered by Hugging Face • Model: FLUX.1-schnell"
)

