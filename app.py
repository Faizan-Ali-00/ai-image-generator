import os
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)


# ==================================================
# CHECK HUGGING FACE TOKEN
# ==================================================

if not HF_TOKEN:
    st.error("❌ Hugging Face API token is missing.")

    st.info(
        "Add your HF_TOKEN in Streamlit Secrets or in a .env file."
    )

    st.stop()


# ==================================================
# HUGGING FACE CLIENT
# ==================================================

client = InferenceClient(
    provider="fal-ai",
    api_key=HF_TOKEN
)


# ==================================================
# MODEL
# ==================================================

MODEL_NAME = "black-forest-labs/FLUX.1-dev"


# ==================================================
# TITLE
# ==================================================

st.title("🎨 AI Image Generator")

st.write(
    "Create high-quality images from your imagination using AI."
)

st.divider()


# ==================================================
# PROMPT
# ==================================================

st.subheader("✍️ Describe your image")

prompt = st.text_area(
    "Enter your prompt",
    placeholder=(
        "Example: A realistic Pakistani cricket player "
        "standing in a large cricket stadium at sunset, "
        "professional photography, cinematic lighting, "
        "highly detailed, photorealistic"
    ),
    height=150
)


# ==================================================
# NEGATIVE PROMPT
# ==================================================

negative_prompt = st.text_area(
    "🚫 What should NOT appear?",
    value=(
        "cartoon, anime, illustration, drawing, "
        "low quality, blurry, distorted, deformed, "
        "bad anatomy, extra fingers, extra limbs, "
        "duplicate person, malformed hands, "
        "text, watermark, logo"
    ),
    height=100
)


# ==================================================
# GENERATE BUTTON
# ==================================================

generate_button = st.button(
    "🎨 Generate Image",
    type="primary",
    use_container_width=True
)


# ==================================================
# IMAGE GENERATION
# ==================================================

if generate_button:

    if not prompt.strip():

        st.warning(
            "⚠️ Please enter a description first."
        )

        st.stop()


    # Combine user prompt with quality instructions
    final_prompt = (
        prompt.strip()
        + ", photorealistic, realistic details, "
        "natural lighting, professional photography, "
        "high quality"
    )


    with st.spinner(
        "🎨 Generating your image... This may take a moment."
    ):

        try:

            # ==========================================
            # GENERATE IMAGE
            # ==========================================

            image = client.text_to_image(
                prompt=final_prompt,
                model=MODEL_NAME,
                negative_prompt=negative_prompt,
                num_inference_steps=28,
                guidance_scale=7.0
            )


            # ==========================================
            # SUCCESS
            # ==========================================

            st.success(
                "✅ Image generated successfully!"
            )


            # ==========================================
            # DISPLAY IMAGE
            # ==========================================

            st.image(
                image,
                caption="AI Generated Image",
                use_container_width=True
            )


            # ==========================================
            # PREPARE DOWNLOAD
            # ==========================================

            image_buffer = BytesIO()

            image.save(
                image_buffer,
                format="PNG"
            )

            image_buffer.seek(0)


            # ==========================================
            # DOWNLOAD
            # ==========================================

            st.download_button(
                label="⬇️ Download Image",
                data=image_buffer.getvalue(),
                file_name="ai_generated_image.png",
                mime="image/png",
                use_container_width=True
            )


        # ==============================================
        # ERROR HANDLING
        # ==============================================

        except Exception as error:

            st.error(
                "❌ Image generation failed."
            )

            st.write(
                "The request could not be completed."
            )

            st.code(
                str(error)
            )


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("⚙️ Model")

    st.write("**Model:**")

    st.code(
        MODEL_NAME
    )

    st.write("**Provider:**")

    st.code(
        "fal-ai"
    )

    st.divider()

    st.header("💡 Prompt Example")

    st.write(
        "Try something detailed like:"
    )

    st.info(
        "A realistic tiger walking through "
        "a misty jungle at sunrise, "
        "professional wildlife photography, "
        "cinematic lighting, highly detailed, "
        "photorealistic"
    )

    st.divider()

    st.caption(
        "Powered by Hugging Face Inference Providers"
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "🎨 AI Image Generator"
)
