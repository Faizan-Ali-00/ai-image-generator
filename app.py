python
import base64
from io import BytesIO

import requests
import streamlit as st
from PIL import Image


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="centered"
)


# ============================================================
# CLOUDFLARE CREDENTIALS
# ============================================================

try:
    CLOUDFLARE_ACCOUNT_ID = st.secrets["CLOUDFLARE_ACCOUNT_ID"]
    CLOUDFLARE_API_TOKEN = st.secrets["CLOUDFLARE_API_TOKEN"]

except Exception:
    st.error("❌ Cloudflare credentials are missing.")

    st.info(
        "Add CLOUDFLARE_ACCOUNT_ID and "
        "CLOUDFLARE_API_TOKEN to Streamlit Secrets."
    )

    st.stop()


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = "@cf/black-forest-labs/flux-2-klein-4b"


# ============================================================
# CLOUDFLARE API
# ============================================================

API_URL = (
    f"https://api.cloudflare.com/client/v4/accounts/"
    f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/"
    f"{MODEL_NAME}"
)


# ============================================================
# TITLE
# ============================================================

st.title("🎨 AI Image Generator")

st.write(
    "Create high-quality realistic images using "
    "Cloudflare Workers AI."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Image Settings")


    # --------------------------------------------------------
    # QUALITY
    # --------------------------------------------------------

    quality = st.selectbox(
        "🎯 Quality",
        [
            "Standard",
            "High",
            "Maximum"
        ],
        index=1
    )


    # --------------------------------------------------------
    # ASPECT RATIO
    # --------------------------------------------------------

    aspect_ratio = st.selectbox(
        "📐 Aspect Ratio",
        [
            "1:1",
            "16:9",
            "9:16",
            "4:3",
            "3:4"
        ],
        index=0
    )


    # --------------------------------------------------------
    # RESOLUTION
    # --------------------------------------------------------

    resolution = st.selectbox(
        "🖼️ Resolution",
        [
            "512p",
            "768p",
            "1024p",
            "1536p",
            "1920p"
        ],
        index=2
    )


    # --------------------------------------------------------
    # OUTPUT FORMAT
    # --------------------------------------------------------

    output_format = st.selectbox(
        "📁 Output Format",
        [
            "PNG",
            "JPEG",
            "WEBP"
        ],
        index=0
    )


    # --------------------------------------------------------
    # STEPS
    # --------------------------------------------------------

    if quality == "Standard":

        default_steps = 4

    elif quality == "High":

        default_steps = 6

    else:

        default_steps = 8


    steps = st.slider(
        "⚡ Generation Steps",
        min_value=4,
        max_value=8,
        value=default_steps,
        step=1
    )


    st.divider()


    st.info(
        "Higher resolution and quality can increase "
        "generation time and usage."
    )


# ============================================================
# PROMPT
# ============================================================

prompt = st.text_area(
    "✍️ Enter your image prompt",

    placeholder=(
        "Example: A photorealistic adult male lion "
        "walking beside a lion cub in the African savanna "
        "during golden hour, realistic fur, natural anatomy, "
        "professional wildlife photography, 85mm telephoto "
        "lens, shallow depth of field"
    ),

    height=170
)


# ============================================================
# GENERATE BUTTON
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
    # RESOLUTION CALCULATION
    # ========================================================

    resolution_value = int(
        resolution.replace("p", "")
    )


    # --------------------------------------------------------
    # ASPECT RATIO
    # --------------------------------------------------------

    if aspect_ratio == "1:1":

        width = resolution_value
        height = resolution_value


    elif aspect_ratio == "16:9":

        width = resolution_value
        height = int(
            resolution_value * 9 / 16
        )


    elif aspect_ratio == "9:16":

        width = int(
            resolution_value * 9 / 16
        )
        height = resolution_value


    elif aspect_ratio == "4:3":

        width = resolution_value
        height = int(
            resolution_value * 3 / 4
        )


    else:

        width = int(
            resolution_value * 3 / 4
        )
        height = resolution_value


    # ========================================================
    # CLOUDFLARE LIMIT
    # ========================================================

    width = min(width, 1920)
    height = min(height, 1920)


    # ========================================================
    # REALISM PROMPT
    # ========================================================

    final_prompt = f"""
Create a highly realistic, detailed, professional-quality
image based exactly on this request:

{prompt}

VISUAL QUALITY:

- Photorealistic appearance
- Realistic anatomy
- Natural proportions
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
- Coherent composition

DO NOT:

- Make it cartoon-like
- Make it childish
- Use exaggerated anatomy
- Add extra limbs
- Add extra fingers
- Add extra eyes
- Distort faces
- Distort bodies
- Add unnecessary people
- Add unnecessary objects
- Change the requested subject

Follow the user's original request precisely.
"""


    # ========================================================
    # API REQUEST
    # ========================================================

    with st.spinner(
        "🎨 Generating your image... Please wait."
    ):

        try:

            headers = {
                "Authorization": (
                    f"Bearer {CLOUDFLARE_API_TOKEN}"
                ),
                "Content-Type": "multipart/form-data"
            }


            # ------------------------------------------------
            # MULTIPART DATA
            # ------------------------------------------------

            data = {
                "prompt": final_prompt,
                "width": str(width),
                "height": str(height),
                "steps": str(steps)
            }


            # ------------------------------------------------
            # REQUEST
            # ------------------------------------------------

            response = requests.post(
                API_URL,
                headers=headers,
                files={
                    key: (None, value)
                    for key, value in data.items()
                },
                timeout=300
            )


            # =================================================
            # HTTP ERROR
            # =================================================

            if response.status_code != 200:

                try:

                    error_data = response.json()

                except Exception:

                    error_data = response.text


                st.error(
                    f"❌ Cloudflare API Error "
                    f"({response.status_code})"
                )

                st.code(
                    str(error_data)
                )

                st.stop()


            # =================================================
            # RESPONSE
            # =================================================

            result = response.json()


            if not result.get("success", False):

                st.error(
                    "❌ Cloudflare failed to generate "
                    "the image."
                )

                st.code(
                    str(result)
                )

                st.stop()


            # =================================================
            # GET IMAGE
            # =================================================

            image_base64 = result["result"]["image"]


            # =================================================
            # DECODE
            # =================================================

            image_bytes = base64.b64decode(
                image_base64
            )


            # =================================================
            # OPEN IMAGE
            # =================================================

            image = Image.open(
                BytesIO(image_bytes)
            )


            # =================================================
            # SUCCESS
            # =================================================

            st.success(
                "✅ Image generated successfully!"
            )


            # =================================================
            # DISPLAY
            # =================================================

            st.image(
                image,
                caption=(
                    f"Generated Image • "
                    f"{width} × {height}"
                ),
                use_container_width=True
            )


            # =================================================
            # FORMAT CONVERSION
            # =================================================

            download_buffer = BytesIO()


            if output_format == "PNG":

                if image.mode not in ["RGB", "RGBA"]:

                    image = image.convert("RGB")


                image.save(
                    download_buffer,
                    format="PNG"
                )

                file_name = (
                    "ai_generated_image.png"
                )

                mime_type = "image/png"


            elif output_format == "WEBP":

                if image.mode != "RGB":

                    image = image.convert("RGB")


                image.save(
                    download_buffer,
                    format="WEBP",
                    quality=95
                )

                file_name = (
                    "ai_generated_image.webp"
                )

                mime_type = "image/webp"


            else:

                if image.mode != "RGB":

                    image = image.convert("RGB")


                image.save(
                    download_buffer,
                    format="JPEG",
                    quality=95
                )

                file_name = (
                    "ai_generated_image.jpg"
                )

                mime_type = "image/jpeg"


            # =================================================
            # DOWNLOAD
            # =================================================

            st.download_button(
                label=(
                    f"⬇️ Download {output_format}"
                ),

                data=download_buffer.getvalue(),

                file_name=file_name,

                mime=mime_type,

                use_container_width=True
            )


        # ====================================================
        # TIMEOUT
        # ====================================================

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Generation timed out. "
                "Try a smaller resolution."
            )


        # ====================================================
        # CONNECTION ERROR
        # ====================================================

        except requests.exceptions.RequestException as e:

            st.error(
                "❌ Could not connect to Cloudflare."
            )

            st.exception(e)


        # ====================================================
        # GENERAL ERROR
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
    "Powered by Cloudflare Workers AI • "
    "FLUX.2 Klein 4B"
)

