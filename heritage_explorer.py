# heritage_explorer.py
import streamlit as st
from streamlit_folium import st_folium
import folium
import sqlite3
from langdetect import detect
from transformers import pipeline
import os
from datetime import datetime

# ----------------------------
# Database Setup
# ----------------------------
DB_FILE = "heritage_explorer.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS contributions (
            contrib_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            title TEXT,
            description TEXT,
            category TEXT,
            language TEXT,
            lat REAL,
            lon REAL,
            media_url TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ----------------------------
# AI Setup
# ----------------------------
classifier = pipeline("zero-shot-classification")

CATEGORIES = ["Story", "Legend", "Song", "Historical Fact"]

# ----------------------------
# Media Upload Setup
# ----------------------------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ----------------------------
# Streamlit Layout
# ----------------------------
st.set_page_config(page_title="Heritage Explorer", layout="wide")
st.title("🌏 Heritage Explorer: Interactive Cultural Map")
st.markdown("Share stories, legends, songs, and historical facts from across India!")

# Language Selector
lang_pref = st.selectbox("Choose your interface language", ["English", "Hindi", "Tamil", "Bengali"], index=0)

# Tabs
tab1, tab2 = st.tabs(["📍 Map", "📝 Submit Contribution"])

# ----------------------------
# Tab 1: Map Display
# ----------------------------
with tab1:
    st.subheader("Contributions Map")
    
    # Initialize map centered in India
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    
    # Fetch contributions from DB
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT title, description, category, language, lat, lon, media_url FROM contributions")
    rows = c.fetchall()
    conn.close()
    
    for row in rows:
        title, desc, category, language, lat, lon, media_url = row
        popup_html = f"<b>{title}</b><br>{desc}<br><i>{category} ({language})</i>"
        if media_url:
            popup_html += f"<br><a href='{media_url}' target='_blank'>Media</a>"
        folium.Marker(location=[lat, lon], popup=popup_html).add_to(m)
    
    st_data = st_folium(m, width=800, height=500)

# ----------------------------
# Tab 2: Form Submission
# ----------------------------
with tab2:
    st.subheader("Submit Your Contribution")
    with st.form("contribution_form"):
        username = st.text_input("Your Name (Optional)")
        title = st.text_input("Title of your Contribution")
        description = st.text_area("Describe your story, legend, song, or historical fact")
        category_input = st.selectbox("Select Category (or leave AI to decide)", ["Auto-detect"] + CATEGORIES)
        lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=20.5937, format="%.6f")
        lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=78.9629, format="%.6f")
        media_file = st.file_uploader("Upload Image/Audio/Video (Optional)", type=["png","jpg","jpeg","mp3","wav","mp4"])
        submitted = st.form_submit_button("Submit Contribution")
        
        if submitted:
            # Language Detection
            try:
                language = detect(description)
            except:
                language = "unknown"
            
            # Category Detection
            if category_input == "Auto-detect":
                result = classifier(description, candidate_labels=CATEGORIES)
                category = result['labels'][0]
            else:
                category = category_input
            
            # Handle Media Upload
            media_url = None
            if media_file:
                filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{media_file.name}"
                filepath = os.path.join(UPLOAD_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(media_file.getbuffer())
                media_url = filepath  # Can be replaced with cloud URL later
            
            # Insert into Database
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute('''
                INSERT INTO contributions (username, title, description, category, language, lat, lon, media_url, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, title, description, category, language, lat, lon, media_url, datetime.now().isoformat()))
            conn.commit()
            conn.close()
            
            st.success(f"Contribution submitted! Detected Language: {language}, Category: {category}")
