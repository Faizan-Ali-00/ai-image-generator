import base64
from io import BytesIO

import streamlit as st
from openai import OpenAI


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Grok AI Image Generator",
    page_icon="🎨",
    layout="centered"
)


# ============================================================
# GET XAI API KEY
# ============================================================

try:
    XAI_API_KEY = st.secrets["XAI_API_KEY"]
except Exception:
    st.error("❌ XAI_API_KEY is missing.")
    st.info("Add XAI_API_KEY to Streamlit Secrets.")
    st.stop()


# ============================================================
# GROK CLIENT
# ============================================================

client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1"
)


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "grok-imagine-image-2.0"


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🎨 Grok AI Image Generator")

st.write(
    "Create realistic, high-quality images using Grok Imagine."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Image Settings")

    resolution = st.selectbox(
        "Resolution",
        ["1k", "2k"],
        index=0
    )

    quality = st.selectbox(
        "Quality",
        ["low", "medium"],
        index=1
    )

    st.divider()

    st.info(
        "💡 Describe your subject, environment, "
        "lighting, camera style and important details "
        "for better results."
    )


# ============================================================
# PROMPT
# ============================================================

prompt = st.text_area(
    "✍️ Enter your image prompt",

    placeholder=(
        "Example: A photorealistic adult male lion "
        "walking beside a lion cub in the African savanna "
        "at golden hour, realistic fur, natural anatomy, "
        "wildlife photography, cinematic lighting, "
        "85mm telephoto lens, shallow depth of field"
    ),

    height=160
)


# ============================================================
# GENERATE IMAGE
# ============================================================

if st.button(
    "🎨 Generate Image",
    use_container_width=True
):

    if not prompt.strip():

        st.warning(
            "⚠️ Please enter a prompt first."
        )

        st.stop()


    # ========================================================
    # REALISM ENHANCEMENT
    # ========================================================

    final_prompt = f"""
Create a highly realistic, photorealistic image based
exactly on this request:

{prompt}

VISUAL QUALITY REQUIREMENTS:

- Photorealistic appearance
- Realistic anatomy and proportions
- Natural facial features
- Realistic skin, fur, hair and materials
- Physically accurate lighting
- Natural shadows
- Realistic reflections
- Realistic depth and perspective
- Natural colors
- Detailed textures
- Professional photography quality
- Cinematic composition
- Correct object scale
- Realistic environment
- Sharp important details
- Natural depth of field
- Coherent scene

AVOID:

- Cartoon appearance
- Childish appearance
- Plastic-looking skin
- Unrealistic anatomy
- Extra limbs
- Extra fingers
- Extra eyes
- Distorted faces
- Deformed bodies
- Unnecessary objects
- Unrequested people
- Unrealistic proportions

Follow the user's requested scene exactly.
"""


    # ========================================================
    # GENERATION
    # ========================================================

    with st.spinner(
        "🎨 Grok is generating your image..."
    ):

        try:

            response = client.images.generate(
                model=MODEL_NAME,

                prompt=final_prompt,

                extra_body={
                    "resolution": resolution,
                    "quality": quality
                }
            )


            # =================================================
            # GET IMAGE URL
            # =================================================

            image_url = response.data[0].url


            if not image_url:

                st.error(
                    "❌ Grok did not return an image URL."
                )

                st.stop()


            # =================================================
            # DOWNLOAD IMAGE
            # =================================================

            import requests

            image_response = requests.get(
                image_url,
                timeout=60
            )

            image_response.raise_for_status()

            image_data = image_response.content


            # =================================================
            # DISPLAY IMAGE
            # =================================================

            st.success(
                "✅ Image generated successfully!"
            )

            st.image(
                image_data,
                caption="Generated by Grok Imagine",
                use_container_width=True
            )


            # =================================================
            # DOWNLOAD BUTTON
            # =================================================

            st.download_button(
                label="⬇️ Download Image",

                data=image_data,

                file_name="grok_generated_image.jpg",

                mime="image/jpeg",

                use_container_width=True
            )


        # ====================================================
        # ERROR HANDLING
        # ====================================================

        except Exception as e:

            st.error(
                "❌ Image generation failed."
            )

            st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Powered by xAI • Grok Imagine Image 2.0"
)
