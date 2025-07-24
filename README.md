# Word Cloud Generator

[![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Transform documents into impactful visual summaries** - A Streamlit app that generates customizable word clouds from uploaded files, perfect for data exploration and presentation.

<!-- Centered image at 50% width -->
<div style="text-align:center;">
  <img src="src/WC Title.jpg" alt="Ttile" style="width:50%; margin:0 auto; display:block;">
<!-- Side-by-side images at 45% width each -->
<div style="display: flex; justify-content: space-between; margin: 20px 0;">
  <img src="src/wordcloud.png" alt="Data" width="45%">
  <img src="src/3d.jpg" alt="3d" width="45%">
</div>

</div>

## ✨ Key Features
- **Multi-format support**: Process PDFs, Word docs (DOCX), and plain text files
- **Smart text processing**:
  - Remove stopwords (custom or predefined)
  - Filter numbers/special characters
  - Frequency-based word scaling
- **Real-time customization**:
  - Adjust size (800x400px to 2000x1000px)
  - Change color schemes (20+ matplotlib colormaps)
  - Toggle word frequency table
- **Export-ready outputs**:
  - Save as PNG/SVG/JPEG
  - Download word frequency CSV

## 🚀 Quick Start

### 1. Install requirements
pip install streamlit wordcloud python-docx pdfplumber matplotlib pillow

### 2. Run the app
streamlit run wordcloud_app.py

## 🎨 Customization Options

| Parameter     | Options                                   | Default
| ------------- | --------------------------------------- |
| Width/Height  | 400-2000px                   | 800x400
|Colormap | viridis, plasma, rainbow, etc. | viridis
|Stopwords| Custom list + NLTK | Enabled
|Background Color | Any HEX/RGB | #FFFFFF

## 📂 File Support

| Format | Library Used | Notes
| -
| PDF | pdfplumber | Best for text-heavy
| DOCX | python-docx | Preserves formatting
| TXT | Native Python | Fastest processing

## 🌍 Deployment

#### Option 1: Streamlit Cloud
Create requirements.txt:
```python
streamlit>=1.22
wordcloud>=1.8
python-docx>=0.8
pdfplumber>=0.7
matplotlib>=3.6
```
#### Option 2: Docker
```docker
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "wordcloud_app.py"]
```
## 📜 License
This project is licensed under the MIT License
