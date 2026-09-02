import base64
from io import BytesIO

import streamlit as st
from google import genai


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)


# --------------------------------------------------
# GET API KEY
# --------------------------------------------------

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ GEMINI_API_KEY is missing.")
    st.info(
        "Add GEMINI_API_KEY to your Streamlit Cloud Secrets."
    )
    st.stop()


# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# --------------------------------------------------
# MODEL
# --------------------------------------------------

MODEL_NAME = "gemini-3.1-flash-image"


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎨 AI Image Generator")

st.write(
    "Turn your ideas into high-quality images using AI."
)


# --------------------------------------------------
# PROMPT
# --------------------------------------------------

prompt = st.text_area(
    "✍️ Enter your prompt",
    placeholder=(
        "Example: A realistic male lion standing beside "
        "its cub in the African savanna at sunset, "
        "professional wildlife photography, natural "
        "lighting, realistic fur, detailed environment"
    ),
    height=140
)


# --------------------------------------------------
# IMAGE SETTINGS
# --------------------------------------------------

st.subheader("⚙️ Image Settings")

col1, col2 = st.columns(2)

with col1:
    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        [
            "1:1",
            "16:9",
            "9:16",
            "4:3",
            "3:4"
        ]
    )

with col2:
    image_size = st.selectbox(
        "Image Quality",
        [
            "1K",
            "2K",
            "4K"
        ],
        index=1
    )


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

generate = st.button(
    "🎨 Generate Image",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# GENERATE IMAGE
# --------------------------------------------------

if generate:

    if not prompt.strip():
        st.warning(
            "⚠️ Please enter a prompt first."
        )
        st.stop()

    # Add quality instructions without forcing
    # every image into a fake-looking style.
    final_prompt = f"""
Create the image exactly according to this request:

{prompt.strip()}

Prioritize:
- realistic anatomy
- natural proportions
- physically accurate lighting
- realistic textures
- natural colors
- coherent composition
- realistic depth and perspective
- high visual detail
- professional photography quality when the
  subject is photographic

Do not add subjects or objects that were not requested.
Do not turn the image into a cartoon or illustration
unless the user explicitly asks for that style.
"""

    with st.spinner(
        "🎨 Creating your image..."
    ):

        try:

            # --------------------------------------------------
            # GEMINI IMAGE GENERATION
            # --------------------------------------------------

            interaction = client.interactions.create(
                model=MODEL_NAME,
                input=final_prompt,
                response_format={
                    "type": "image",
                    "mime_type": "image/png",
                    "aspect_ratio": aspect_ratio,
                    "image_size": image_size
                },
                generation_config={
                    "thinking_level": "high"
                }
            )


            # --------------------------------------------------
            # GET GENERATED IMAGE
            # --------------------------------------------------

            generated_image = interaction.output_image

            if not generated_image:
                st.error(
                    "❌ Gemini did not return an image."
                )
                st.stop()


            # --------------------------------------------------
            # DECODE IMAGE
            # --------------------------------------------------

            image_data = base64.b64decode(
                generated_image.data
            )


            # --------------------------------------------------
            # DISPLAY IMAGE
            # --------------------------------------------------

            st.success(
                "✅ Image generated successfully!"
            )

            st.image(
                image_data,
                caption="AI Generated Image",
                use_container_width=True
            )


            # --------------------------------------------------
            # DOWNLOAD BUTTON
            # --------------------------------------------------

            st.download_button(
                label="⬇️ Download Image",
                data=image_data,
                file_name="ai_generated_image.png",
                mime="image/png",
                use_container_width=True
            )


        # --------------------------------------------------
        # ERROR HANDLING
        # --------------------------------------------------

        except Exception as error:

            st.error(
                "❌ Image generation failed."
            )

            st.code(
                str(error)
            )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("🎨 AI Image Generator")

    st.write(
        "**Model:**"
    )

    st.code(
        MODEL_NAME
    )

    st.write(
        "**Provider:**"
    )

    st.write(
        "Google Gemini"
    )

    st.divider()

    st.write(
        "### 💡 Prompt Example"
    )

    st.write(
        "A realistic snow leopard sitting on a "
        "mountain cliff during sunrise, natural "
        "wildlife photography, detailed fur, "
        "realistic mountains and atmospheric lighting."
    )

    st.divider()

    st.caption(
        "Powered by Google Gemini"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "🎨 AI Image Generator • Gemini 3.1 Flash Image"
)
