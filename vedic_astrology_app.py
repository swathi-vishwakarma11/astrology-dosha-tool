# Astrology Web App using Streamlit
# Install with: pip install flatlib streamlit

import streamlit as st
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

st.set_page_config(page_title="Vedic Chart & Dosha Checker", layout="centered")
st.title("🔮 Free Vedic Astrology Tool")
st.markdown("Enter your birth details to get your planetary positions and check for doshas & yogas.")

# -----------------------------
# User Input
# -----------------------------
birth_date = st.date_input("📅 Birth Date")
birth_time = st.time_input("⏰ Birth Time")
lat = st.text_input("🌐 Latitude (e.g., 17.385044 for Hyderabad)", "17.385044")
lon = st.text_input("🌐 Longitude (e.g., 78.486671 for Hyderabad)", "78.486671")
timezone = '+05:30'  # IST timezone

if st.button("🔍 Generate Chart"):
    try:
        dt = Datetime(str(birth_date), birth_time.strftime("%H:%M"), timezone)
        pos = GeoPos(lat, lon)
        chart = Chart(dt, pos, hsys=const.HOUSES_PLACIDUS)

        st.subheader("🪐 Planetary Positions")
        for obj in [const.SUN, const.MOON, const.MARS, const.MERCURY, const.JUPITER, const.VENUS, const.SATURN, const.RAHU, const.KETU]:
            body = chart.get(obj)
            st.write(f"{body}: {body.sign} {body.signlon:.2f}°")

        # Manglik Dosha Check
        mars = chart.get(const.MARS)
        mars_house = chart.house_of(mars)
        if mars_house in ['1', '2', '4', '7', '8', '12']:
            st.error(f"⚠️ MANGAL DOSHA DETECTED: Mars is in house {mars_house}")
        else:
            st.success("✅ No Manglik Dosha Detected")

        # Kaal Sarp Dosha Check
        planets = [chart.get(obj) for obj in [const.SUN, const.MOON, const.MARS, const.MERCURY, const.JUPITER, const.VENUS, const.SATURN]]
        rahu = chart.get(const.RAHU)
        ketu = chart.get(const.KETU)

        rahu_deg = rahu.lon
        ketu_deg = ketu.lon

        inside = 0
        for planet in planets:
            if rahu_deg > ketu_deg:
                if ketu_deg < planet.lon < rahu_deg:
                    inside += 1
            else:
                if planet.lon > rahu_deg or planet.lon < ketu_deg:
                    inside += 1

        if inside == len(planets):
            st.error("⚠️ KAAL SARP DOSHA DETECTED")
        else:
            st.success("✅ No Kaal Sarp Dosha Detected")

        # Gaja Kesari Yoga Check
        moon_house = chart.house_of(chart.get(const.MOON))
        jup_house = chart.house_of(chart.get(const.JUPITER))

        if moon_house in ['1', '4', '7', '10'] and jup_house in ['1', '4', '7', '10']:
            st.success("🌟 GAJA KESARI YOGA PRESENT!")
        else:
            st.info("⚠️ Gaja Kesari Yoga Not Present")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
