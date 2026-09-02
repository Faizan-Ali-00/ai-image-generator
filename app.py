import os
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# ==============================
# LOAD ENVIRONMENT VARIABLES
# ==============================

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# ==============================
# PAGE SETTINGS
# ==============================

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

# ==============================
# HEADER
# ==============================

st.title("🎨 AI Image Generator")
st.write("Create images from your ideas using AI.")

st.divider()

# ==============================
# CHECK API KEY
# ==============================

if not HF_TOKEN:
    st.error("❌ Hugging Face API token not found.")
    st.info(
        "For local use, create a .env file and add: HF_TOKEN=your_token"
    )
    st.stop()

# ==============================
# HUGGING FACE CLIENT
# ==============================

client = InferenceClient(
    api_key=HF_TOKEN
)

MODEL_NAME = "black-forest-labs/FLUX.1-schnell"

# ==============================
# PROMPT
# ==============================

st.subheader("📝 Describe your image")

prompt = st.text_area(
    "Enter your prompt",
    placeholder=(
        "Example: A futuristic city at night, "
        "neon lights, cinematic atmosphere, "
        "ultra detailed"
    ),
    height=130
)

# ==============================
# GENERATE BUTTON
# ==============================

generate = st.button(
    "🎨 Generate Image",
    type="primary",
    use_container_width=True
)

# ==============================
# IMAGE GENERATION
# ==============================

if generate:

    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
        st.stop()

    with st.spinner("🎨 Creating your image..."):

        try:

            image = client.text_to_image(
                prompt=prompt,
                model=MODEL_NAME
            )

            st.success("✅ Image generated successfully!")

            # ==============================
            # DISPLAY IMAGE
            # ==============================

            st.image(
                image,
                caption="AI Generated Image",
                use_container_width=True
            )

            # ==============================
            # PREPARE DOWNLOAD
            # ==============================

            image_buffer = BytesIO()

            image.save(
                image_buffer,
                format="PNG"
            )

            image_buffer.seek(0)

            # ==============================
            # DOWNLOAD BUTTON
            # ==============================

            st.download_button(
                label="⬇️ Download Image",
                data=image_buffer,
                file_name="ai_generated_image.png",
                mime="image/png",
                use_container_width=True
            )

        except Exception as error:

            st.error("❌ Image generation failed.")

            st.write(
                "Please check your Hugging Face token, "
                "model availability, and API access."
            )

            st.code(str(error))

# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.header("⚙️ Model Information")

    st.write("**Model:**")
    st.code(MODEL_NAME)

    st.write("**Provider:**")
    st.write("Hugging Face")

    st.divider()

    st.write("### 💡 Prompt Tips")

    st.write(
        "Describe the subject, environment, "
        "lighting, style, and level of detail."
    )

    st.write(
        "Example:"
    )

    st.code(
        "A realistic tiger walking through a "
        "misty jungle at sunrise, cinematic "
        "lighting, highly detailed"
    )

# ==============================
# FOOTER
# ==============================

st.divider()

st.caption(
    "🎨 AI Image Generator • Powered by Hugging Face"
)
