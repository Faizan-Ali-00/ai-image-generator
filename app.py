import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Faizi AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

# =========================
# TITLE
# =========================

st.title("🎨 Faizi AI Image Generator")
st.write("Generate realistic AI images using Cloudflare FLUX.2 Klein 4B")

# =========================
# CLOUDFLARE
# =========================

ACCOUNT_ID = st.secrets["CLOUDFLARE_ACCOUNT_ID"]
API_TOKEN = st.secrets["CLOUDFLARE_API_TOKEN"]

MODEL = "@cf/black-forest-labs/flux-2-klein-4b"

URL = (
    f"https://api.cloudflare.com/client/v4/accounts/"
    f"{ACCOUNT_ID}/ai/run/{MODEL}"
)

# =========================
# PROMPT
# =========================

prompt = st.text_area(
    "📝 Enter your prompt",
    placeholder="Example: A realistic Ferrari racing through Dubai at night, cinematic lighting, detailed photography",
    height=120
)

# =========================
# SETTINGS
# =========================

st.subheader("⚙️ Image Settings")

col1, col2 = st.columns(2)

with col1:

    quality = st.selectbox(
        "🎨 Quality",
        [
            "Standard",
            "High",
            "Maximum"
        ]
    )

    resolution = st.selectbox(
        "📐 Resolution",
        [
            "512 × 512",
            "768 × 768",
            "1024 × 1024",
            "1280 × 720",
            "1920 × 1080"
        ]
    )

with col2:

    image_format = st.selectbox(
        "🖼️ Image Format",
        [
            "PNG",
            "JPEG",
            "WEBP"
        ]
    )

    aspect_ratio = st.selectbox(
        "📏 Aspect Ratio",
        [
            "Square (1:1)",
            "Landscape (16:9)",
            "Portrait (9:16)"
        ]
    )

# =========================
# RESOLUTION
# =========================

if aspect_ratio == "Square (1:1)":

    resolution_options = {
        "512 × 512": (512, 512),
        "768 × 768": (768, 768),
        "1024 × 1024": (1024, 1024)
    }

    resolution = st.selectbox(
        "Square Resolution",
        list(resolution_options.keys())
    )

elif aspect_ratio == "Landscape (16:9)":

    resolution_options = {
        "1280 × 720": (1280, 720),
        "1920 × 1080": (1920, 1080)
    }

    resolution = st.selectbox(
        "Landscape Resolution",
        list(resolution_options.keys())
    )

else:

    resolution_options = {
        "720 × 1280": (720, 1280),
        "1080 × 1920": (1080, 1920)
    }

    resolution = st.selectbox(
        "Portrait Resolution",
        list(resolution_options.keys())
    )

width, height = resolution_options[resolution]

# =========================
# QUALITY
# =========================

quality_text = {
    "Standard": "good image quality",
    "High": "highly detailed and sharp image quality",
    "Maximum": "maximum realistic detail, sharp textures, cinematic professional quality"
}

# =========================
# GENERATE BUTTON
# =========================

st.write("")

if st.button(
    "🚀 Generate Image",
    use_container_width=True
):

    if not prompt.strip():

        st.warning("⚠️ Please enter a prompt first.")

        st.stop()

    final_prompt = f"""
{prompt.strip()}

Create the image with {quality_text[quality]}.
Use realistic lighting, natural textures,
professional composition and detailed visual quality.
"""

    # =========================
    # MULTIPART REQUEST
    # =========================

    files = {
        "prompt": (None, final_prompt),
        "width": (None, str(width)),
        "height": (None, str(height))
    }

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    with st.spinner("🎨 Generating image..."):

        try:

            response = requests.post(
                URL,
                headers=headers,
                files=files,
                timeout=180
            )

            # =========================
            # API ERROR
            # =========================

            if response.status_code != 200:

                st.error(
                    f"Cloudflare API Error: {response.status_code}"
                )

                try:
                    st.json(response.json())

                except:
                    st.code(response.text)

                st.stop()

            data = response.json()

            if not data.get("success"):

                st.error("❌ Image generation failed.")

                st.json(data)

                st.stop()

            # =========================
            # IMAGE
            # =========================

            image_base64 = data["result"]["image"]

            image_bytes = base64.b64decode(
                image_base64
            )

            image = Image.open(
                BytesIO(image_bytes)
            )

            # =========================
            # DISPLAY
            # =========================

            st.success(
                f"✅ Image generated successfully! "
                f"{width} × {height}"
            )

            st.image(
                image,
                use_container_width=True
            )

            # =========================
            # DOWNLOAD FORMAT
            # =========================

            output = BytesIO()

            if image_format == "PNG":

                if image.mode not in ["RGB", "RGBA"]:
                    image = image.convert("RGB")

                image.save(
                    output,
                    format="PNG"
                )

                mime_type = "image/png"

                filename = "faizi_ai_image.png"

            elif image_format == "JPEG":

                if image.mode != "RGB":
                    image = image.convert("RGB")

                image.save(
                    output,
                    format="JPEG",
                    quality=95
                )

                mime_type = "image/jpeg"

                filename = "faizi_ai_image.jpg"

            else:

                if image.mode not in ["RGB", "RGBA"]:
                    image = image.convert("RGB")

                image.save(
                    output,
                    format="WEBP",
                    quality=95
                )

                mime_type = "image/webp"

                filename = "faizi_ai_image.webp"

            # =========================
            # DOWNLOAD BUTTON
            # =========================

            st.download_button(
                label=f"⬇️ Download {image_format}",
                data=output.getvalue(),
                file_name=filename,
                mime=mime_type,
                use_container_width=True
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Cloudflare took too long to respond. "
                "Please try again."
            )

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )
