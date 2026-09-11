<div align="center">
  <img src="logos/lumina.svg" width="440" alt="Lumina Logo" />
</div>

# Lumina — AI Image Generator

Turn words into light. Lumina transforms your text prompts into stunning AI-generated visuals — powered by a resilient multi-model chain that never leaves you waiting.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare_Workers_AI-F38020?logo=cloudflare&logoColor=white)
![Replicate](https://img.shields.io/badge/Replicate-000000?logo=replicate&logoColor=white)
![Together](https://img.shields.io/badge/Together_AI-0F6FFF?logoColor=white)
![fal.ai](https://img.shields.io/badge/fal.ai-8B5CF6?logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Overview

Lumina is a beautiful, modern AI image generator with a **7-model fallback chain**. It converts any text prompt into a high-quality image using state-of-the-art models like FLUX and SDXL. If one provider is down, another instantly takes over — so you never get stuck waiting.

Built with a **multi-provider fallback architecture** and a clean teal/violet UI, Lumina also ships with a **History** panel and a **Settings** panel that persist between sessions.

## ✨ Features

- 🎨 Text-to-image generation — describe anything, get a stunning image
- 🔗 7-model fallback chain — Cloudflare FLUX → SDXL → Schnell → Replicate → Together → fal.ai → Pollinations
- 🎚️ Three quality levels — Standard · High · Maximum
- 📐 Multiple aspect ratios — Square · Landscape · Portrait
- 📏 Smart resolutions — from 512×512 up to 1920×1080
- 🖼️ Three output formats — PNG · JPEG · WEBP
- 📚 History panel — auto-saves last 50 generations with thumbnails
- ⚙️ Settings panel — save + reset defaults (persistent)
- 💾 Download button — one click to save your image
- 🎯 Provider indicator — shows which model generated the image
- 🌈 Beautiful UI — teal/violet gradient, animated sun logo, glassmorphism cards

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Primary Image Model | Cloudflare FLUX.2 Klein 4B |
| Fallback 1 | Cloudflare SDXL |
| Fallback 2 | Cloudflare FLUX.1 Schnell |
| Fallback 3 | Replicate FLUX-schnell |
| Fallback 4 | Together AI FLUX.1-schnell-Free |
| Fallback 5 | fal.ai FLUX schnell |
| Fallback 6 | Pollinations.ai (no key needed) |
| Language | Python 3.10+ |
| Storage | Local JSON (history.json, settings.json) |

## 🔗 Multi-Model Architecture

Lumina uses a provider chain so it never fails due to a single provider running out of credits:

🎨 Image → 1. Cloudflare FLUX.2 Klein 4B  (primary)
              ↓ (fails)
           2. Cloudflare SDXL              (fallback 1)
              ↓ (fails)
           3. Cloudflare FLUX.1 Schnell    (fallback 2)
              ↓ (fails)
           4. Replicate FLUX-schnell       (fallback 3)
              ↓ (fails)
           5. Together AI FLUX.1           (fallback 4)
              ↓ (fails)
           6. fal.ai FLUX schnell          (fallback 5)
              ↓ (fails)
           7. Pollinations.ai              (fallback 6 — free, no key)
              ↓ (fails)
           ❌ Error

You only need one provider key to start, but adding all seven means zero downtime. Pollinations works without any key as a guaranteed last resort.

## 📂 Project Structure

ai-image-generator/
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── history.json          # Auto-generated — saved generations
├── settings.json         # Auto-generated — saved preferences
├── thumbnails/           # Auto-generated — history thumbnails
├── logos/
│   └── lumina.svg        # Lumina logo (used in README)
├── .gitignore            # Git ignore rules
└── README.md

## ⚙️ Installation (Local)

1. Clone the repository

git clone https://github.com/Faizan-Ali-00/ai-image-generator.git
cd ai-image-generator

2. Create a virtual environment

Windows:
python -m venv venv
venv\Scripts\activate

macOS / Linux:
python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Set up your API keys

Create a .env file in the root directory:

CLOUDFLARE_ACCOUNT_ID=your_account_id_here
CLOUDFLARE_API_TOKEN=your_cloudflare_token_here
REPLICATE_API_TOKEN=r8_your_replicate_token_here
TOGETHER_API_KEY=your_together_key_here
FAL_API_KEY=your_fal_key_here

You only need Cloudflare to get started. Pollinations needs no key.

## 🔑 Getting Free API Keys

| Provider | Models | Free Tier | Get Key |
|----------|--------|-----------|---------|
| Cloudflare | FLUX, SDXL, Schnell | 10,000 neurons/day | https://dash.cloudflare.com/profile/api-tokens |
| Replicate | FLUX-schnell | $5 credit on signup | https://replicate.com/account/api-tokens |
| Together AI | FLUX.1-schnell-Free | $1 credit on signup | https://api.together.xyz/settings/api-keys |
| fal.ai | FLUX schnell | $1 credit on signup | https://fal.ai/dashboard/keys |
| Pollinations | FLUX | Unlimited | No key needed ✅ |

### Getting Your Cloudflare Account ID

1. Log in to https://dash.cloudflare.com/
2. Go to Workers & Pages
3. Find Account details on the right
4. Copy the Account ID

### Creating Your Cloudflare API Token

1. Go to https://dash.cloudflare.com/profile/api-tokens
2. Click Create Token → Custom token
3. Set permission: Account → Workers AI → Read
4. Include your Account
5. Click Create Token and copy it

## 🚀 Deployment (Streamlit Cloud)

1. Push to GitHub

git add .
git commit -m "Deploy Lumina"
git push origin main

2. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click New app
3. Select your repo: Faizan-Ali-00/ai-image-generator
4. Main file path: app.py
5. Click Deploy

3. Add your API keys as Secrets

Important: Never put API keys in app.py on GitHub — they become public. Use Streamlit Secrets instead.

1. Go to share.streamlit.io → your app → ⋮ → Settings
2. Click the Secrets tab
3. Paste your keys:

CLOUDFLARE_ACCOUNT_ID = "your_account_id_here"
CLOUDFLARE_API_TOKEN = "your_cloudflare_token_here"
REPLICATE_API_TOKEN = "r8_your_replicate_token_here"
TOGETHER_API_KEY = "your_together_key_here"
FAL_API_KEY = "your_fal_key_here"

4. Click Save → Reboot app

## ▶️ Usage

1. Enter a text prompt describing the image you want
2. Adjust quality, aspect ratio, resolution, and format from the sidebar
3. Click 💫 Generate Image
4. Wait for the image to be generated (usually 5–20 seconds)
5. Preview the result and download it
6. Every generation is auto-saved to History

### Example Prompts

- A bioluminescent forest at midnight, glowing mushrooms, cinematic lighting
- Van Gogh style painting of a coffee shop in the rain
- A cyberpunk samurai in a neon-lit Tokyo alley, 8K, ultra detailed
- A golden retriever puppy in a sunflower field, soft bokeh
- A futuristic space station orbiting a purple gas giant

## 🎛️ Settings

Open the ⚙️ Settings tab in the sidebar to configure:

| Setting | Options | Default |
|---------|---------|---------|
| Quality | Standard / High / Maximum | High |
| Aspect Ratio | Square / Landscape / Portrait | Square (1:1) |
| Format | PNG / JPEG / WEBP | PNG |

Click Save Settings to persist them. Click Reset to Defaults to restore original values.

## 📚 History

Every generation is automatically saved in the 📚 History tab (up to the last 50). Each entry includes:

- 🕐 Timestamp
- 🖼️ Thumbnail of the image
- 📝 Original prompt
- ⚡ Provider that generated it
- 📐 Size and quality

You can View, Delete individual entries, or Clear All at once.

## 🎨 UI Highlights

- Lumina sun logo — animated glow with rays in teal/violet/magenta
- Teal → violet gradient — modern, cool palette
- Glassmorphism cards — soft transparency effects
- Scanning animation — glowing sun pulses during generation
- Result header — shows dimensions, quality, and provider
- Sidebar — three tabs: Create, History, Settings

## 🔒 Security Notes

- Never commit .env to GitHub
- Always use Streamlit Secrets for deployed apps
- Revoke keys immediately if accidentally exposed
- Store each provider's key separately for easy rotation
- On Streamlit Cloud, history.json and thumbnails/ are wiped on reboot

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: git checkout -b feature/AmazingFeature
3. Commit your changes: git commit -m "Add some AmazingFeature"
4. Push to the branch: git push origin feature/AmazingFeature
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Faizan Ali
GitHub: https://github.com/Faizan-Ali-00
Repository: https://github.com/Faizan-Ali-00/ai-image-generator

## ⭐ Show Your Support

If this project helped you, please give it a star on GitHub — it means a lot!

## 🙏 Acknowledgments

Cloudflare Workers AI — https://developers.cloudflare.com/workers-ai/
Replicate — https://replicate.com
Together AI — https://together.ai
fal.ai — https://fal.ai
Pollinations — https://pollinations.ai
Streamlit — https://streamlit.io
