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

st.title("🎨 Faizi AI Image Generator")
st.write("Generate realistic AI images using Cloudflare FLUX.2 Klein 4B")

# =========================
# CLOUDFLARE SECRETS
# =========================

ACCOUNT_ID = st.secrets["CLOUDFLARE_ACCOUNT_ID"]
API_TOKEN = st.secrets["CLOUDFLARE_API_TOKEN"]

MODEL = "@cf/black-forest-labs/flux-2-klein-4b"

URL = (
    f"https://api.cloudflare.com/client/v4/accounts/"
    f"{ACCOUNT_ID}/ai/run/{MODEL}"
)

# =========================
# SIDEBAR
# =========================

st.sidebar.header("⚙️ Image Settings")

resolution = st.sidebar.selectbox(
    "Resolution",
    [
        "512 × 512",
        "768 × 768",
        "1024 × 1024",
        "1280 × 720",
        "1920 × 1080"
    ]
)

quality = st.sidebar.selectbox(
    "Quality",
    ["Standard", "High", "Maximum"]
)

output_format = st.sidebar.selectbox(
    "Download Format",
    ["PNG", "JPEG", "WEBP"]
)

# =========================
# RESOLUTION
# =========================

resolution_map = {
    "512 × 512": (512, 512),
    "768 × 768": (768, 768),
    "1024 × 1024": (1024, 1024),
    "1280 × 720": (1280, 720),
    "1920 × 1080": (1920, 1080)
}

width, height = resolution_map[resolution]

# =========================
# PROMPT
# =========================

prompt = st.text_area(
    "📝 Enter your prompt",
    placeholder=(
        "Example: A cinematic portrait of a Pakistani warrior "
        "standing in an ancient fortress at sunset, ultra realistic, "
        "dramatic lighting, highly detailed"
    ),
    height=120
)

# =========================
# GENERATE
# =========================

if st.button("🚀 Generate Image", use_container_width=True):

    if not prompt.strip():
        st.warning("Please enter a prompt first.")
        st.stop()

    # Prompt enhancement
    final_prompt = f"""
Create a highly detailed, realistic image.

{prompt}

Quality requirements:
- photorealistic
- highly detailed
- natural lighting
- realistic textures
- professional composition
- sharp details
- cinematic quality
- no text or watermark
"""

    # =========================
    # IMPORTANT:
    # DO NOT manually specify
    # Content-Type.
    # requests will create the
    # multipart boundary.
    # =========================

    files = {
        "prompt": (None, final_prompt),
        "width": (None, str(width)),
        "height": (None, str(height)),
    }

    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    with st.spinner("🎨 Generating your image..."):

        try:

            response = requests.post(
                URL,
                headers=headers,
                files=files,
                timeout=180
            )

            # =========================
            # ERROR HANDLING
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
                st.error("Cloudflare failed to generate the image.")
                st.json(data)
                st.stop()

            # =========================
            # GET BASE64 IMAGE
            # =========================

            image_base64 = data["result"]["image"]

            image_bytes = base64.b64decode(image_base64)

            image = Image.open(BytesIO(image_bytes))

            # =========================
            # DISPLAY
            # =========================

            st.success("✅ Image generated successfully!")

            st.image(
                image,
                caption=f"{width} × {height}",
                use_container_width=True
            )

            # =========================
            # CONVERT FORMAT
            # =========================

            output_buffer = BytesIO()

            if output_format == "PNG":

                image.save(
                    output_buffer,
                    format="PNG"
                )

                mime = "image/png"
                filename = "faizi_ai_image.png"

            elif output_format == "JPEG":

                if image.mode != "RGB":
                    image = image.convert("RGB")

                image.save(
                    output_buffer,
                    format="JPEG",
                    quality=95
                )

                mime = "image/jpeg"
                filename = "faizi_ai_image.jpg"

            else:

                image.save(
                    output_buffer,
                    format="WEBP",
                    quality=95
                )

                mime = "image/webp"
                filename = "faizi_ai_image.webp"

            # =========================
            # DOWNLOAD
            # =========================

            st.download_button(
                label=f"⬇️ Download {output_format}",
                data=output_buffer.getvalue(),
                file_name=filename,
                mime=mime,
                use_container_width=True
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Request timed out. Please try again."
            )

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )
