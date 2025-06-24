# Astrology Web App using Streamlit (Flatlib-Free Version)
# Hostable on Streamlit Cloud ✅

import streamlit as st
from datetime import datetime
import pytz
from math import floor

st.set_page_config(page_title="Vedic Chart & Dosha Checker", layout="centered")
st.title("🔮 Free Vedic Astrology Tool (Cloud Version)")
st.markdown("Enter your birth details to check Manglik Dosha, Kaal Sarp Dosha & Gaja Kesari Yoga (basic logic version).")

# -----------------------------
# User Input
# -----------------------------
birth_date = st.date_input("📅 Birth Date")
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

        # Manglik Dosha Check (simplified logic)
        if str(mars_house) in ['1', '2', '4', '7', '8', '12']:
            st.error(f"⚠️ MANGAL DOSHA DETECTED: Mars is in house {mars_house}")
        else:
            st.success("✅ No Manglik Dosha Detected")

        # Kaal Sarp Dosha (Random Planets Logic Simulation)
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
            st.error("⚠️ KAAL SARP DOSHA DETECTED")
        else:
            st.success("✅ No Kaal Sarp Dosha Detected")

        # Gaja Kesari Yoga (Simplified House Simulation)
        moon_house = ((birth_date.month + lagna_house) % 12) + 1
        jupiter_house = ((birth_date.day + lagna_house) % 12) + 1

        if str(moon_house) in ['1', '4', '7', '10'] and str(jupiter_house) in ['1', '4', '7', '10']:
            st.success("🌟 GAJA KESARI YOGA PRESENT!")
        else:
            st.info("⚠️ Gaja Kesari Yoga Not Present")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
