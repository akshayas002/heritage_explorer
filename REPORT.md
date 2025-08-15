# Heritage Explorer - Project Report

## Overview
AI-powered interactive cultural map collecting stories, legends, songs, and historical facts.

## Objectives
- Collect location-based contributions
- Multilingual support
- AI-based language detection and classification

## Tech Stack
- Streamlit, Folium, SQLite, HuggingFace Transformers

## Features
- Contribution Form
- Interactive Map
- AI Integration
- Multilingual Support
- Media Uploads

## Database Schema
Table: contributions (id, username, title, description, category, language, lat, lon, media_url, timestamp)

## Deployment
Run with `streamlit run heritage_explorer.py`

## Future Enhancements
- Analytics dashboard
- Gamification
- PostgreSQL migration
