# 🌏 Heritage Explorer

**Heritage Explorer** is an AI-powered interactive cultural map that allows users to submit and explore stories, legends, songs, and historical facts from across India. The platform collects multilingual, location-based contributions, creating a rich corpus of cultural and historical data.

## Features

- Interactive map displaying user contributions
- Multilingual support (English + Indian languages)
- AI-powered language detection and category classification
- Media upload support (images, audio, video)
- Lightweight and mobile-friendly Streamlit interface

## Tech Stack

- Python, Streamlit
- Folium / streamlit-folium for maps
- SQLite / PostgreSQL for database
- HuggingFace Transformers for NLP
- langdetect for language detection

## Installation

```bash
git clone https://github.com/your-username/heritage-explorer.git
cd heritage-explorer
pip install -r requirements.txt

---

## Usage

```bash
streamlit run heritage_explorer.py
Open http://localhost:8501 in your browser to access the app.