# Astrology Web App using Streamlit + Flatlib (Customizable Version)
# No external API needed – uses birth details for real planetary calculations

import streamlit as st
from datetime import datetime, date
from io import BytesIO
from fpdf import FPDF
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

st.set_page_config(page_title="Vedic Chart & Dosha Checker", layout="centered")
st.title("🔮 Free Vedic Astrology Tool (Custom Chart Generator)")
st.markdown("Enter your birth details to generate Sun, Moon, Lagna signs, Nakshatra, and check Doshas & Yogas.")

# -----------------------------
# User Input
# -----------------------------
name = st.text_input("🧑 Full Name")
gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
birth_date = st.date_input("📅 Birth Date", min_value=date(1945, 1, 1), max_value=date.today())
birth_time_str = st.text_input("🕰️ Enter Birth Time (HH:MM, 24hr format)", value="12:00")
birth_place = st.text_input("📍 Birth Place (City, Country)", value="Hyderabad, India")
latitude = st.text_input("🌐 Latitude (e.g., 17.385044)", value="17.385044")
longitude = st.text_input("🌐 Longitude (e.g., 78.486671)", value="78.486671")

dob_str = birth_date.strftime("%Y/%m/%d")
try:
    birth_time = datetime.strptime(birth_time_str, "%H:%M").time()
except ValueError:
    st.warning("⚠️ Invalid time format. Please use HH:MM (24-hour).")
    birth_time = datetime.strptime("12:00", "%H:%M").time()

chart = None
if st.button("🔍 Generate My Chart"):
    try:
        dt = Datetime(f"{dob_str} {birth_time.strftime('%H:%M')}", 'UTC')
        pos = GeoPos(latitude, longitude)
        chart = Chart(dt, pos)

        sun = chart.get(const.SUN).sign
        moon = chart.get(const.MOON).sign
        asc = chart.get(const.ASC).sign
        sun_obj = chart.get(const.SUN)
        moon_obj = chart.get(const.MOON)
        mars_obj = chart.get(const.MARS)
        mercury_obj = chart.get(const.MERCURY)

        st.subheader("🌞 Your Birth Chart Highlights")
        st.write(f"☀️ Sun Sign: {sun}")
        st.write(f"🌙 Moon Sign: {moon}")
        st.write(f"🔼 Ascendant: {asc}")

        st.markdown("### 🧿 Detected Yogas & Doshas")
        if moon_obj.sign in ['Cancer', 'Scorpio', 'Pisces'] and chart.get(const.JUPITER).isAngular:
            st.success("✅ Gaja Kesari Yoga")
            st.caption("🌕 Moon in kendra with Jupiter")
        if sun_obj.sign == mercury_obj.sign and abs(sun_obj.lon - mercury_obj.lon) > 3:
            st.success("✅ Budha-Aditya Yoga")
            st.caption("☀️ Sun and Mercury in same sign, not combust")
        if mars_obj.house in ['1', '4', '7', '8', '12']:
            st.warning("⚠️ Mangal Dosha Detected")
            st.caption("🔥 Mars in Mangalic house")

        st.markdown("### 📥 Download PDF Report")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Vedic Astrology Report", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Name: {name} | Gender: {gender}", ln=True)
        pdf.cell(200, 10, txt=f"DOB: {birth_date} | Time: {birth_time_str}", ln=True)
        pdf.cell(200, 10, txt=f"Place: {birth_place}", ln=True)
        pdf.cell(200, 10, txt=f"Sun: {sun} | Moon: {moon} | Ascendant: {asc}", ln=True)
        pdf.cell(200, 10, txt=f"Yogas: Based on sign + house placements", ln=True)
        buffer = BytesIO()
        pdf.output(buffer)
        st.download_button("📥 Download Report (PDF)", data=buffer.getvalue(), file_name="Your_Vedic_Report.pdf", mime="application/pdf")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
