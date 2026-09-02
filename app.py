import base64
from io import BytesIO

import streamlit as st
from google import genai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)


# ============================================================
# GET GEMINI API KEY
# ============================================================

try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("❌ GEMINI_API_KEY is missing.")
    st.info(
        "Add GEMINI_API_KEY to Streamlit Secrets."
    )
    st.stop()


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "gemini-3.1-flash-image"


# ============================================================
# TITLE
# ============================================================

st.title("🎨 AI Image Generator")

st.write(
    "Create high-quality realistic images from your ideas using Gemini AI."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Image Settings")

    aspect_ratio = st.selectbox(
        "Aspect Ratio",
        [
            "1:1",
            "16:9",
            "9:16",
            "4:3",
            "3:4"
        ],
        index=0
    )

    image_size = st.selectbox(
        "Image Quality",
        [
            "1K",
            "2K",
            "4K"
        ],
        index=1
    )

    st.divider()

    st.info(
        "💡 For the most realistic results, describe "
        "the subject, environment, lighting, camera "
        "style, and important details."
    )


# ============================================================
# PROMPT
# ============================================================

prompt = st.text_area(
    "✍️ Enter your image prompt",
    placeholder=(
        "Example: A realistic adult male lion walking "
        "beside a lion cub in the African savanna at "
        "golden hour, natural wildlife photography, "
        "realistic fur, realistic anatomy, cinematic lighting"
    ),
    height=160
)


# ============================================================
# GENERATE BUTTON
# ============================================================

if st.button(
    "🎨 Generate Image",
    use_container_width=True
):

    # --------------------------------------------------------
    # CHECK PROMPT
    # --------------------------------------------------------

    if not prompt.strip():

        st.warning(
            "⚠️ Please enter a prompt first."
        )

        st.stop()


    # --------------------------------------------------------
    # REALISM INSTRUCTIONS
    # --------------------------------------------------------

    final_prompt = f"""
Create a highly realistic, high-quality image based on this request:

{prompt}

IMPORTANT VISUAL REQUIREMENTS:

- Photorealistic appearance
- Realistic anatomy and proportions
- Natural facial features
- Realistic textures and materials
- Physically accurate lighting
- Natural shadows and reflections
- Realistic depth and perspective
- Detailed environment
- Natural colors
- Professional photography quality when appropriate
- Sharp important details
- Coherent composition
- Realistic scale between objects
- No unnecessary objects or subjects
- Do not make the image cartoon-like
- Do not make it childish
- Do not use exaggerated anatomy
- Do not add extra limbs, fingers, eyes, faces, or body parts
- Do not distort objects
- Follow the user's requested scene exactly
"""


    # --------------------------------------------------------
    # GENERATE IMAGE
    # --------------------------------------------------------

    with st.spinner(
        "🎨 Generating your image... Please wait."
    ):

        try:

            response = client.interactions.create(
                model=MODEL_NAME,

                input=final_prompt,

                response_format={
                    "type": "image",
                    "mime_type": "image/jpeg",
                    "aspect_ratio": aspect_ratio,
                    "image_size": image_size
                },

                generation_config={
                    "thinking_level": "high"
                }
            )


            # ------------------------------------------------
            # FIND GENERATED IMAGE
            # ------------------------------------------------

            generated_image = None

            for output in response.output:

                if hasattr(output, "data"):

                    generated_image = output.data

                    break


            # ------------------------------------------------
            # CHECK IMAGE
            # ------------------------------------------------

            if not generated_image:

                st.error(
                    "❌ Gemini did not return an image."
                )

                st.stop()


            # ------------------------------------------------
            # DECODE BASE64 IMAGE
            # ------------------------------------------------

            image_data = base64.b64decode(
                generated_image
            )


            # ------------------------------------------------
            # OPEN IMAGE
            # ------------------------------------------------

            from PIL import Image

            image = Image.open(
                BytesIO(image_data)
            )


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            st.success(
                "✅ Image generated successfully!"
            )


            # ------------------------------------------------
            # DISPLAY IMAGE
            # ------------------------------------------------

            st.image(
                image,
                caption="Generated Image",
                use_container_width=True
            )


            # ------------------------------------------------
            # CONVERT TO JPEG
            # ------------------------------------------------

            image_bytes = BytesIO()

            # Convert RGB/RGBA to RGB for JPEG
            if image.mode != "RGB":

                image = image.convert("RGB")


            image.save(
                image_bytes,
                format="JPEG",
                quality=95
            )


            # ------------------------------------------------
            # DOWNLOAD BUTTON
            # ------------------------------------------------

            st.download_button(
                label="⬇️ Download Image",
                data=image_bytes.getvalue(),
                file_name="ai_generated_image.jpg",
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
    "Powered by Google Gemini • Model: gemini-3.1-flash-image"
)
