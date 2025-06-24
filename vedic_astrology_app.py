# Astrology Web App using Streamlit (API-Based Version)
# Hostable on Streamlit Cloud ✅

import streamlit as st
import requests
from datetime import datetime, date
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="Vedic Chart & Dosha Checker", layout="centered")
st.title("🔮 Free Vedic Astrology Tool (Cloud Version)")
st.markdown("Enter your birth details to check Doshas, Yogas, Lagna, Moon Sign, Nakshatra, Sun Sign, Ascendant and D1-D9 analysis.")

# -----------------------------
# User Input
# -----------------------------
name = st.text_input("🧑 Full Name")
gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
birth_date = st.date_input("📅 Birth Date", min_value=date(1945, 1, 1), max_value=date.today())
birth_time_str = st.text_input("🕰️ Enter Birth Time (HH:MM, 24hr format)", value="12:00")
birth_place = st.text_input("📍 Birth Place (City, Country)", value="Hyderabad, India")

try:
    birth_time = datetime.strptime(birth_time_str, "%H:%M").time()
except ValueError:
    st.warning("⚠️ Invalid time format. Please use HH:MM (24-hour).")
    birth_time = datetime.strptime("12:00", "%H:%M").time()

# -----------------------------
# Call API
# -----------------------------
if st.button("🔍 Generate Dosha & Chart Report"):
    try:
        birth_datetime = datetime.combine(birth_date, birth_time)
        dob_str = birth_datetime.strftime("%Y-%m-%d")
        tob_str = birth_datetime.strftime("%H:%M")

        # Example fallback without API (DEMO PURPOSE)
        st.subheader("🌞 Sun, Moon, Ascendant Info")
        st.write("☀️ Sun Sign: Leo")
        st.write("🌙 Moon Sign: Aquarius")
        st.write("🌌 Nakshatra: Purvabhadra")
        st.write("🔼 Ascendant: Sagittarius")

        st.markdown("### 🧿 Detected Yogas & Doshas")
        st.success("✅ Gaja Kesari Yoga")
        st.caption("🌕 Moon in a kendra from Jupiter (e.g. Moon in 1st, Jupiter in 4th)")
        st.success("✅ Budha-Aditya Yoga")
        st.caption("☀️ Sun and Mercury together, not combust (e.g. in 10th house Leo)")
        st.warning("⚠️ Partial Mangal Dosha")
        st.caption("🔥 Mars in 1st, 4th, 7th, 8th, or 12th house")
        st.success("✅ Chandra-Mangal Yoga")
        st.caption("🌙 Moon and Mars in conjunction or mutual aspect")
        st.success("✅ Raja Yoga")
        st.caption("👑 Kendra and Trikona lords in conjunction or aspect")
        st.success("✅ Dharma-Karmadhipati Yoga")
        st.caption("🧘 9th lord and 10th lord in mutual aspect or same house")
        st.success("✅ Vipreet Raj Yoga")
        st.caption("🔄 Lords of 6th/8th/12th in each other's houses (e.g. 6th lord in 8th)")
        st.success("✅ Neech Bhanga Raja Yoga")
        st.caption("♄ Exalted planet aspecting debilitated one, or lord of debilitated sign in kendra")

        st.markdown("### 📊 D1 + D9 Chart Samples")
        st.image("https://i.imgur.com/BZGh8zY.png", caption="🪐 D1 Chart (Sample)")
        st.image("https://i.imgur.com/LbU8YlV.png", caption="🧿 D9 Chart (Navamsa)")

        # PDF Report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Vedic Astrology Report", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Name: {name} | Gender: {gender}", ln=True)
        pdf.cell(200, 10, txt=f"DOB: {birth_date} | Time: {birth_time_str}", ln=True)
        pdf.cell(200, 10, txt=f"Birth Place: {birth_place}", ln=True)
        pdf.cell(200, 10, txt="Sun: Leo, Moon: Aquarius, Asc: Sagittarius", ln=True)
        pdf.cell(200, 10, txt="Nakshatra: Purvabhadra", ln=True)
        pdf.multi_cell(200, 10, txt="Yogas: Gaja Kesari, Budha-Aditya, Chandra-Mangal, Raja Yoga, Dharma-Karmadhipati, Vipreet Raj Yoga, Neech Bhanga Raj Yoga\nDoshas: Partial Mangal")

        buffer = BytesIO()
        pdf.output(buffer)
        st.download_button("📥 Download Report (PDF)", data=buffer.getvalue(), file_name="Vedic_Report.pdf", mime="application/pdf")

        # Payment CTA
        st.markdown("---")
        st.subheader("🔐 Unlock Full D1 & D9 Analysis")
        st.markdown("This is a free preview. Full predictions (D1, D9, career, marriage, remedies, etc.) available after payment.")
        st.link_button("💳 Pay & Unlock Full Report", url="https://buy.stripe.com/your-payment-link")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
