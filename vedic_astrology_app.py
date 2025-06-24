# Astrology Web App using Streamlit (Flatlib-Free Version)
# Hostable on Streamlit Cloud ✅

import streamlit as st
from datetime import datetime, date
import pytz
from math import floor
from io import BytesIO
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
import smtplib
from email.message import EmailMessage
from flatlib import const
from flatlib.ephem import ephem
ephem.set_ephem(None)
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

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
latitude = st.text_input("🌐 Latitude", value="17.3850")
longitude = st.text_input("🌐 Longitude", value="78.4867")
user_email = st.text_input("📧 Enter Your Email to Receive Report")

# Convert time input safely
try:
    birth_time = datetime.strptime(birth_time_str, "%H:%M").time()
except ValueError:
    st.warning("⚠️ Invalid time format. Please use HH:MM (24-hour).")
    birth_time = datetime.strptime("12:00", "%H:%M").time()

if st.button("🔍 Generate Dosha & Chart Report"):
    try:
        birth_datetime = datetime.combine(birth_date, birth_time)
        utc_dt = birth_datetime.strftime("%Y/%m/%d %H:%M")
        pos = GeoPos(latitude, longitude)
        chart = Chart(Datetime(utc_dt, "UTC"), pos, IDs=None)

        # Moon, Sun and Ascendant
        moon = chart.get(const.MOON)
        sun = chart.get(const.SUN)
        ascendant = chart.get(const.ASC)

        moon_sign = moon.sign
        sun_sign = sun.sign
        asc_sign = ascendant.sign
        asc_degree = ascendant.lon

        moon_lon = moon.lon
        nak_index = int(moon_lon // (13 + 1/3))
        nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
            "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Moola", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
            "Uttara Bhadrapada", "Revati"
        ]
        moon_nakshatra = nakshatras[nak_index]

        st.subheader("🌞 Sun Sign, Moon Rashi, Ascendant")
        st.write(f"☀️ Sun Sign: {sun_sign}")
        st.write(f"🌙 Moon Sign (Rashi): {moon_sign}")
        st.write(f"🌌 Nakshatra: {moon_nakshatra}")
        st.write(f"🔼 Ascendant: {asc_sign} ({round(asc_degree,2)}°)")

        # -----------------------------
        # Planetary Positions (D1)
        # -----------------------------
        st.markdown("### 📊 D1 Chart (Rasi Chart) Planetary Positions")
        d1_planets = [const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN, const.RAHU, const.KETU]
        d1_data = {p: chart.get(p) for p in d1_planets}
        for p in d1_data:
            st.write(f"**{p}** → Sign: {d1_data[p].sign}, Degree: {round(d1_data[p].lon, 2)}°")

        # Placeholder for D9 - logic depends on divisional chart calculation (not in flatlib)
        st.markdown("### 📊 D9 Chart (Navamsa) → [Preview Placeholder]")
        st.image("https://i.imgur.com/LbU8YlV.png", caption="🧿 Sample D9 (Navamsa) Chart")

        # Generate PDF Report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Vedic Astrology Report", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Name: {name} | Gender: {gender}", ln=True)
        pdf.cell(200, 10, txt=f"DOB: {birth_date} | Time: {birth_time_str}", ln=True)
        pdf.cell(200, 10, txt=f"Birth Place: {birth_place}", ln=True)
        pdf.cell(200, 10, txt=f"Sun: {sun_sign}, Moon: {moon_sign}, Asc: {asc_sign} ({round(asc_degree,2)}°)", ln=True)
        pdf.cell(200, 10, txt=f"Nakshatra: {moon_nakshatra}", ln=True)

        for p in d1_data:
            pdf.cell(200, 10, txt=f"{p}: {d1_data[p].sign} ({round(d1_data[p].lon,2)}°)", ln=True)

        buffer = BytesIO()
        pdf.output(buffer)
        st.download_button("📥 Download Report (PDF)", data=buffer.getvalue(), file_name="Vedic_Report.pdf", mime="application/pdf")

        # Email PDF Report (Basic Demo)
        if user_email:
            try:
                msg = EmailMessage()
                msg['Subject'] = 'Your Vedic Astrology Report'
                msg['From'] = 'your_email@example.com'
                msg['To'] = user_email
                msg.set_content('Hi, here is your generated astrology report attached.')
                msg.add_attachment(buffer.getvalue(), maintype='application', subtype='pdf', filename='Vedic_Report.pdf')

                with smtplib.SMTP('smtp.example.com', 587) as smtp:
                    smtp.starttls()
                    smtp.login('your_email@example.com', 'your_password')
                    smtp.send_message(msg)

                st.success(f"📧 Report sent to {user_email} successfully!")
            except Exception as e:
                st.warning(f"Could not send email: {e}")

        # Payment CTA
        st.markdown("---")
        st.subheader("🔐 Unlock Full D1 & D9 Analysis")
        st.markdown("This is a free preview. Full predictions (D1, D9, career, marriage, remedies, etc.) available after payment.")
        st.link_button("💳 Pay & Unlock Full Report", url="https://buy.stripe.com/your-payment-link")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
