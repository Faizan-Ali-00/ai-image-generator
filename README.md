# 🎨 AI Image Generator

A simple AI image generation web application built with Python, Streamlit, and Hugging Face.

The application allows users to enter a text description and generate an AI-created image using the FLUX.1-schnell model.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=black)
![FLUX](https://img.shields.io/badge/FLUX.1-schnell-9B59B6)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Overview

AI Image Generator is a lightweight web app that turns your text prompts into images. Powered by Hugging Face's FLUX.1-schnell model, it delivers fast and high-quality AI-generated visuals through a simple Streamlit interface.

## ✨ Features

- 📝 Text-to-image generation
- ⚡ FLUX AI image generation
- 🖥️ Simple Streamlit interface
- 🖼️ Image preview
- ⬇️ Download generated images
- ⚠️ Basic error handling

## 🛠️ Tech Stack

- Frontend: Streamlit
- Model: FLUX.1-schnell (via Hugging Face)
- Image Processing: Pillow
- Language: Python 3.10+

## 📂 Project Structure

    ai-image-generator/
    ├── app.py                # Streamlit app (main entry point)
    ├── requirements.txt      # Python dependencies
    ├── .gitignore            # Git ignore rules
    └── README.md

## ⚙️ Installation

### 1. Clone the repository

    git clone https://github.com/Faizan-Ali-00/ai-image-generator.git
    cd ai-image-generator

### 2. Create a virtual environment

    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Set up your API key

Create a `.env` file in the root directory:

    HUGGINGFACE_API_KEY=your_huggingface_api_key_here

Get your API key from https://huggingface.co/settings/tokens

## ▶️ Usage

Run the Streamlit app:

    streamlit run app.py

Then open your browser at http://localhost:8501

1. Enter a text description of the image you want
2. Click Generate
3. Preview the AI-generated image
4. Download the image if you like it

## 🔒 Notes

- Never commit your `.env` file — it contains your Hugging Face API key
- Make sure `.env` is listed in `.gitignore`
- If you accidentally expose a key, revoke it immediately at https://huggingface.co/settings/tokens

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m "Add some AmazingFeature"`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Faizan Ali

- GitHub: https://github.com/Faizan-Ali-00
- Repository: https://github.com/Faizan-Ali-00/ai-image-generator

## ⭐ Show Your Support

If this project helped you, please give it a star on GitHub.

## 🙏 Acknowledgments

- Hugging Face — https://huggingface.co
- FLUX.1-schnell — https://huggingface.co/black-forest-labs/FLUX.1-schnell
- Streamlit — https://streamlit.io
