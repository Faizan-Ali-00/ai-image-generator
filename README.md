# 🎨 AI Image Generator

A simple AI image generation web application built with **Python, Streamlit, and Hugging Face**.

The application allows users to enter a text description and generate an AI-created image using the **FLUX.1-schnell** model.

## 🚀 Features

- 📝 Text-to-image generation
- 🎨 FLUX AI image generation
- 🖥️ Simple Streamlit interface
- 🖼️ Image preview
- ⬇️ Download generated images
- ⚠️ Basic error handling

## 🛠️ Technologies Used

- Python
- Streamlit
- Hugging Face Inference API
- FLUX.1-schnell
- python-dotenv

## 📁 Project Structure

```text
ai-image-generator/
│
├── app.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## ⚙️ Run Locally

Clone the repository:

```bash
git clone https://github.com/Faizan-Ali-00/ai-image-generator.git
```

Open the project folder:

```bash
cd ai-image-generator
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
HF_TOKEN=your_hugging_face_token
```

Then start the application:

```bash
streamlit run app.py
```

## 🔐 Security

The Hugging Face API token is stored in environment variables and is **not included in the GitHub repository**.

Never publish your API token publicly.

## 🌐 Deployment

The application can be deployed using **Streamlit Community Cloud**.

Add the Hugging Face token to Streamlit's **Secrets** configuration:

```toml
HF_TOKEN = "your_hugging_face_token"
```

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Faizan Ali**

GitHub: https://github.com/Faizan-Ali-00
