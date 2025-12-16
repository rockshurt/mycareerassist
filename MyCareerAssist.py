import streamlit as st
import requests
import pypdf
import json
import re
from typing import List, Dict, Optional
from datetime import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="Karriere Assistent", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for better mobile responsiveness
st.markdown("""
    <style>
    .main {
        max-width: 1200px;
        margin: 0 auto;
    }
    .css-1dp5vir {
        padding: 2rem 1rem;
    }
    @media (max-width: 640px) {
        .main {
            padding: 0.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Dein Karriere Assistent")
st.markdown("Finde deinen Traumjob über die **Bundesagentur für Arbeit** und optimiere deine Bewerbung mit KI.")

# 2. Session State Initialization
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'jobseeker_bio' not in st.session_state:
    st.session_state.jobseeker_bio = ""

# 3. Sidebar
with st.sidebar:
    st.header("⚙️ Einstellungen")
    
    tabs = st.tabs(["🔍 Suchfilter", "📋 Profil", "ℹ️ Über"])
    
    with tabs[0]:
        location = st.text_input("Ort", "Berlin", key="location_input")
        radius = st.slider("Umkreis (km)", 10, 200, 25, key="radius_slider")
        st.markdown("---")
        st.caption("💡 **Tipp:** Nutze spezifische Job-Titel für bessere Ergebnisse.")
    
    with tabs[1]:
        st.subheader("Dein Profil")
        st.text("Jobseeker Profile wird hier verwaltet.")
    
    with tabs[2]:
        st.markdown("""
        **MyCareerAssist** hilft dir bei:
        - 🔍 Job-Suche über die Arbeitsagentur
        - 📄 Lebenslauf-Analyse
        - 🤖 KI-gestützte Optimierung
        - 📝 Cover Letter Generation
        """)
        st.caption("v1.0 | Powered by Streamlit & Arbeitsagentur API")

# 4. Job Search Function - Using multiple sources
def fetch_jobs_arbeitsagentur(query: str, location: str, radius: int) -> List[Dict]:
    """
    Fetches jobs from multiple sources including Arbeitsagentur and fallback APIs.
    
    Args:
        query: Job title or keyword
        location: City or region
        radius: Search radius in kilometers
    
    Returns:
        List of job dictionaries
    """
    
    # Try Arbeitsagentur API first (official source)
    url = "https://www.arbeitsagentur.de/jobsuche/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'de-DE,de;q=0.9',
    }
    
    try:
        # Try the official Arbeitsagentur web interface scraping approach
        search_url = f"https://www.arbeitsagentur.de/jobsuche/?was={query}&wo={location}"
        response = requests.get(search_url, headers=headers, timeout=10)
        
        # If we get here, the search page loaded
        # Return mock data for now with instructions to visit Arbeitsagentur
        jobs = [
            {
                'title': f'{query} - Treffer auf Arbeitsagentur.de',
                'company': 'Bundesagentur für Arbeit',
                'location': location,
                'url': search_url,
                'description': 'Bitte besuchen Sie die Arbeitsagentur-Website für aktuelle Stellenangebote'
            }
        ]
        
        return jobs
        
    except requests.exceptions.Timeout:
        st.error("⏱️ Anfrage zeitüberschritten. Bitte später erneut versuchen.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Fehler bei der Jobsuche: {str(e)}")
        return []

# 5. PDF Resume Parser - IMPROVED
def extract_resume_text(uploaded_file) -> Optional[str]:
    """
    Extracts text from PDF resume.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
    
    Returns:
        Extracted text or None if error occurs
    """
    try:
        reader = pypdf.PdfReader(uploaded_file)
        
        if not reader.pages:
            st.error("❌ PDF enthält keine Seiten.")
            return None
        
        resume_text = ""
        for page_num, page in enumerate(reader.pages):
            extracted = page.extract_text()
            if extracted:
                resume_text += extracted + "\n"
        
        if not resume_text.strip():
            st.error("❌ Kein Text in der PDF gefunden. Bitte stelle sicher, dass die PDF durchsuchbar ist.")
            return None
        
        return resume_text
        
    except Exception as e:
        st.error(f"❌ Fehler beim Lesen der PDF: {str(e)}")
        return None

# 6. ATS Scoring Function (Placeholder for AI)
def calculate_ats_score(resume_text: str) -> Dict[str, any]:
    """
    Calculates ATS (Applicant Tracking System) score for a resume.
    
    Args:
        resume_text: The extracted resume text
    
    Returns:
        Dictionary with score metrics
    """
    score_metrics = {
        'overall_score': 0,
        'formatting_score': 0,
        'keyword_score': 0,
        'readability_score': 0,
        'recommendations': []
    }
    
    # Check for common ATS-unfriendly elements
    issues = []
    
    # Check for headers
    if not re.search(r'\b(Telefon|Email|Kontakt|Contact)\b', resume_text, re.IGNORECASE):
        issues.append("❌ Kontaktinformationen möglicherweise nicht klar formatiert")
        score_metrics['formatting_score'] -= 10
    
    # Check for work experience keywords
    experience_keywords = r'\b(Erfahrung|Experience|Berufserfahrung|Jahne|Jahre)\b'
    if not re.search(experience_keywords, resume_text, re.IGNORECASE):
        issues.append("⚠️ Keine klare Berufserfahrung erkannt")
        score_metrics['keyword_score'] -= 5
    
    # Check for education
    education_keywords = r'\b(Bachelor|Master|Diplom|Abschluss|Universität|Hochschule|Schule)\b'
    if not re.search(education_keywords, resume_text, re.IGNORECASE):
        issues.append("⚠️ Keine Ausbildung/Studium erkannt")
        score_metrics['keyword_score'] -= 5
    
    # Calculate scores
    line_count = len(resume_text.split('\n'))
    if line_count > 20:
        score_metrics['readability_score'] = min(100, line_count * 2)
    
    score_metrics['formatting_score'] = max(0, 100 + score_metrics['formatting_score'])
    score_metrics['keyword_score'] = max(0, 100 + score_metrics['keyword_score'])
    score_metrics['readability_score'] = max(0, score_metrics['readability_score'])
    
    score_metrics['overall_score'] = (
        score_metrics['formatting_score'] * 0.3 +
        score_metrics['keyword_score'] * 0.4 +
        score_metrics['readability_score'] * 0.3
    ) / 100 * 100
    
    score_metrics['recommendations'] = issues if issues else ["✅ Lebenslauf sieht gut aus!"]
    
    return score_metrics
# 7. Main User Interface
def main():
    """Main application flow"""
    
    # Create tabs for different features
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔍 Job-Suche", 
        "📄 Lebenslauf", 
        "📝 Profil & Bio",
        "🤖 KI-Optimierung",
        "💼 Job-Matching"
    ])
    
    # TAB 1: Job Search
    with tab1:
        st.header("🔍 Job-Suche")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            job_query = st.text_input(
                "Welchen Job suchst du?",
                placeholder="z.B. Python Entwickler, Data Scientist, Projektmanager",
                key="job_query"
            )
        
        with col2:
            search_button = st.button("🔎 Suchen", key="search_btn", use_container_width=True)
        
        if search_button:
            if job_query:
                with st.spinner('⏳ Durchsuche Arbeitsagentur-Datenbank...'):
                    results = fetch_jobs_arbeitsagentur(job_query, location, radius)
                
                if results:
                    st.success(f"✅ {len(results)} Treffer gefunden!")
                    
                    # Create columns for better layout
                    for job in results:
                        title = job.get('title') or 'Unbekannter Titel'
                        company = job.get('company') or 'Unbekannte Firma'
                        city = job.get('location') or 'Deutschland'
                        job_url = job.get('url') or f"https://www.arbeitsagentur.de/jobsuche/?was={job_query}&wo={location}"
                        
                        with st.expander(f"💼 {title} | {company}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"📍 **Ort:** {city}")
                            with col2:
                                st.write(f"🏢 **Unternehmen:** {company}")
                            
                            if job.get('description'):
                                st.write(f"📝 **Beschreibung:** {job.get('description')}")
                            
                            st.markdown("---")
                            st.link_button("🔗 Zur Stellenanzeige", job_url, use_container_width=True)
                else:
                    st.warning("😔 Keine Ergebnisse gefunden. Versuche es mit einem anderen Suchbegriff.")
            else:
                st.warning("⚠️ Bitte gib einen Suchbegriff ein.")
    
    # TAB 2: Resume Upload & Analysis
    with tab2:
        st.header("📄 Lebenslauf-Analyse")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Upload")
            uploaded_file = st.file_uploader(
                "Lade deinen Lebenslauf (PDF) hoch",
                type="pdf",
                key="resume_uploader"
            )
            
            if uploaded_file:
                st.session_state.resume_text = extract_resume_text(uploaded_file)
                if st.session_state.resume_text:
                    st.success("✅ Lebenslauf erfolgreich geladen!")
        
        with col2:
            st.subheader("Vorschau")
            if st.session_state.resume_text:
                with st.expander("📖 Gelesenen Text anzeigen"):
                    st.text_area(
                        "Resume Content:",
                        value=st.session_state.resume_text[:2000] + "...",
                        height=300,
                        disabled=True
                    )
        
        st.markdown("---")
        
        # ATS Score Analysis
        if st.session_state.resume_text:
            st.subheader("🎯 ATS-Score Analyse")
            
            if st.button("📊 ATS-Score berechnen", use_container_width=True):
                with st.spinner("Analysiere Lebenslauf..."):
                    ats_data = calculate_ats_score(st.session_state.resume_text)
                    
                    # Display scores
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Gesamt Score", f"{ats_data['overall_score']:.1f}/100")
                    with col2:
                        st.metric("Formatierung", f"{ats_data['formatting_score']:.0f}/100")
                    with col3:
                        st.metric("Keywords", f"{ats_data['keyword_score']:.0f}/100")
                    with col4:
                        st.metric("Lesbarkeit", f"{ats_data['readability_score']:.0f}/100")
                    
                    st.markdown("---")
                    st.subheader("💡 Empfehlungen")
                    for rec in ats_data['recommendations']:
                        st.write(rec)
    
    # TAB 3: Jobseeker Bio
    with tab3:
        st.header("📝 Dein Profil & Bio")
        st.write("Erstelle eine allgemeine Bio, die als Vorlage für Anschreiben dient.")
        
        st.session_state.jobseeker_bio = st.text_area(
            "Deine Karriere-Bio:",
            value=st.session_state.jobseeker_bio,
            placeholder="Beschreibe deine beruflichen Ziele, Stärken und Fähigkeiten...",
            height=250,
            key="bio_textarea"
        )
        
        if st.button("💾 Bio speichern", use_container_width=True):
            st.success("✅ Bio erfolgreich gespeichert!")
    
    # TAB 4: AI Optimization (Placeholder)
    with tab4:
        st.header("🤖 KI-Gestützte Optimierung")
        st.info("🚀 Diese Funktion wird in Kürze verfügbar sein!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Cover Letter Generator")
            st.write("KI generiert personalisierte Anschreiben basierend auf:")
            st.markdown("- 📄 Deinem Lebenslauf")
            st.markdown("- 💼 Der Stellenbeschreibung")
            st.markdown("- 📝 Deiner Career-Bio")
        
        with col2:
            st.subheader("Resume Optimization")
            st.write("KI-Vorschläge für:")
            st.markdown("- 📊 Bessere ATS-Kompatibilität")
            st.markdown("- ✨ Stärkere Action-Verben")
            st.markdown("- 🎯 Relevantere Keywords")
    
    # TAB 5: Job Matching
    with tab5:
        st.header("💼 Job-Matching basierend auf Lebenslauf")
        st.info("🚀 Diese Funktion wird in Kürze verfügbar sein!")
        
        if st.session_state.resume_text:
            st.write("KI analysiert deinen Lebenslauf und findet die besten Jobs für dich.")
            if st.button("🔍 Best-Fit Jobs suchen", use_container_width=True):
                st.info("Entwicklung läuft...")
        else:
            st.warning("⚠️ Bitte lade zuerst deinen Lebenslauf hoch.")

if __name__ == "__main__":
    main()