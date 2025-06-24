# Astrology Web App using Streamlit (Flatlib-Free Version)
# Hostable on Streamlit Cloud ✅

import streamlit as st
from datetime import datetime, date
import pytz
from math import floor
from io import BytesIO
from fpdf import FPDF

st.set_page_config(page_title="Vedic Chart & Dosha Checker", layout="centered")
st.title("🔮 Free Vedic Astrology Tool (Cloud Version)")
st.markdown("Enter your birth details to check Manglik Dosha, Kaal Sarp Dosha & Gaja Kesari Yoga (basic logic version).")

# -----------------------------
# User Input
# -----------------------------
name = st.text_input("🧑 Full Name")
gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
birth_date = st.date_input("📅 Birth Date", min_value=date(1945, 1, 1), max_value=date.today())
birth_time = st.time_input("⏰ Birth Time")
lat = st.number_input("🌐 Latitude", value=17.385044)
lon = st.number_input("🌐 Longitude", value=78.486671)

if st.button("🔍 Generate Dosha Report"):
    try:
        # Simulated calculations instead of flatlib
        hour = birth_time.hour
        minute = birth_time.minute

        total_minutes = hour * 60 + minute
        lagna_house = (total_minutes // 120) % 12 + 1  # basic rotation logic every 2 hours = 1 house
        mars_house = ((birth_date.day + birth_date.month) % 12) + 1
        rahu_deg = (birth_date.day * 12) % 360
        ketu_deg = (rahu_deg + 180) % 360

        st.subheader("🌌 Lagna Estimation")
        st.write(f"🧭 Estimated Lagna House: {lagna_house}")

        # Lagna Grid Chart (12 Houses Text Grid)
        st.markdown("#### 🗺️ Basic Lagna Chart (12 Houses)")
        chart = ["" for _ in range(12)]
        chart[lagna_house - 1] = "Lagna"
        chart[mars_house - 1] += " 🔴 Mars"
        for i in range(0, 12, 4):
            row = " | ".join(chart[i:i+4])
            st.markdown(row)

        # Lagna chart image (optional visual aid)
        st.image("https://i.imgur.com/tbL3VTx.png", caption="🌀 Sample Lagna Chart")

        # Navamsa chart image placeholder
        st.image("https://i.imgur.com/LbU8YlV.png", caption="🧿 Sample Navamsa Chart")

        # Manglik Dosha Check (simplified logic)
        if str(mars_house) in ['1', '2', '4', '7', '8', '12']:
            manglik = True
            st.error(f"⚠️ MANGAL DOSHA DETECTED: Mars is in house {mars_house}")
            st.markdown("**🔮 Interpretation:** You may experience delays in marriage, arguments in relationships, or inner restlessness. Remedial measures recommended.")
        else:
            manglik = False
            st.success("✅ No Manglik Dosha Detected")

        # Kaal Sarp Dosha
        planets_degrees = [(birth_date.day * i * 7) % 360 for i in range(1, 8)]
        inside = 0
        for deg in planets_degrees:
            if rahu_deg < ketu_deg:
                if rahu_deg < deg < ketu_deg:
                    inside += 1
            else:
                if deg > rahu_deg or deg < ketu_deg:
                    inside += 1

        if inside == len(planets_degrees):
            kaal_sarp = True
            st.error("⚠️ KAAL SARP DOSHA DETECTED")
            st.markdown("**🔮 Interpretation:** You may face frequent ups and downs in career, emotions, and family life. You might benefit from spiritual practices and ancestral healing.")
        else:
            kaal_sarp = False
            st.success("✅ No Kaal Sarp Dosha Detected")

        # Gaja Kesari Yoga
        moon_house = ((birth_date.month + lagna_house) % 12) + 1
        jupiter_house = ((birth_date.day + lagna_house) % 12) + 1

        if str(moon_house) in ['1', '4', '7', '10'] and str(jupiter_house) in ['1', '4', '7', '10']:
            gaja_kesari = True
            st.success("🌟 GAJA KESARI YOGA PRESENT!")
            st.markdown("**🔮 Interpretation:** You have leadership qualities, good intelligence, and protection from life troubles. Excellent for fame and recognition.")
        else:
            gaja_kesari = False
            st.info("⚠️ Gaja Kesari Yoga Not Present")

        # PDF Report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Vedic Astrology Basic Report", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Name: {name} | Gender: {gender}", ln=True)
        pdf.cell(200, 10, txt=f"DOB: {birth_date} | Time: {birth_time}", ln=True)
        pdf.cell(200, 10, txt=f"Lagna: House {lagna_house}", ln=True)
        pdf.cell(200, 10, txt=f"Manglik Dosha: {'Yes' if manglik else 'No'}", ln=True)
        pdf.cell(200, 10, txt=f"Kaal Sarp Dosha: {'Yes' if kaal_sarp else 'No'}", ln=True)
        pdf.cell(200, 10, txt=f"Gaja Kesari Yoga: {'Yes' if gaja_kesari else 'No'}", ln=True)

        buffer = BytesIO()
        pdf.output(buffer)
        st.download_button("📥 Download Report (PDF)", data=buffer.getvalue(), file_name="Vedic_Report.pdf", mime="application/pdf")

        st.markdown("---")
        st.markdown("### 🧾 Want Full Personalized Report?")
        st.info("🔐 This is a basic demo. For full chart analysis, remedies & career/love/marriage predictions — DM us or click below.")
        st.link_button("💌 Buy Full Report Now", url="https://your-consultation-link.com")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
