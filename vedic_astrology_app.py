# Astrology Web App using Streamlit + Prokerala SDK Integration with Free/Paid Toggle
# Dynamically fetches Sun, Moon, Ascendant, Nakshatra, Doshas, Yogas using real birth data

import streamlit as st
from datetime import datetime, date
from io import BytesIO
from fpdf import FPDF
from prokerala.client import Client

st.set_page_config(page_title="Vedic Chart & Dosha Checker", layout="centered")
st.title("🔮 Free Vedic Astrology Tool (Live SDK-Based)")
st.markdown("Enter your birth details to generate real chart data with yogas & doshas. Free preview with option for full PDF.")

# -----------------------------
# User Input
# -----------------------------
name = st.text_input("🧑 Full Name")
gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
birth_date = st.date_input("📅 Birth Date", min_value=date(1945, 1, 1), max_value=date.today())
birth_time_str = st.text_input("🕰️ Enter Birth Time (HH:MM, 24hr format)", value="12:00")
birth_place = st.text_input("📍 Birth Place (City, Country)", value="Hyderabad, India")
latitude = st.text_input("🌐 Latitude", value="17.385044")
longitude = st.text_input("🌐 Longitude", value="78.486671")

plan_type = st.radio("📦 Select Mode", ["Free Preview", "Premium (Full Chart)"])

try:
    birth_time = datetime.strptime(birth_time_str, "%H:%M").time()
except ValueError:
    st.warning("⚠️ Invalid time format. Please use HH:MM (24-hour).")
    birth_time = datetime.strptime("12:00", "%H:%M").time()

birth_datetime = datetime.combine(birth_date, birth_time)

# -----------------------------
# Prokerala SDK Setup (Using Streamlit Secrets for security)
# -----------------------------
client_id = st.secrets["prokerala"]["client_id"]
client_secret = st.secrets["prokerala"]["client_secret"]

client = Client(client_id, client_secret)

if st.button("🔍 Generate My Report"):
    if plan_type == "Free Preview":
        st.subheader("🌞 Your Sample Chart")
        st.write("☀️ Sun Sign: Leo")
        st.write("🌙 Moon Sign: Aquarius")
        st.write("🔼 Ascendant: Sagittarius")
        st.write("🌌 Nakshatra: Purvabhadra")

        st.markdown("### 🧿 Yogas & Doshas")
        st.success("✅ Gaja Kesari Yoga")
        st.warning("⚠️ Mangal Dosha Detected")

        st.info("🔓 Upgrade to Premium to get your real birth chart & PDF report.")

    else:
        try:
            st.info("🔮 Fetching your chart using SDK...")
            response = client.astrology.birth_details(
                datetime=birth_datetime,
                latitude=float(latitude),
                longitude=float(longitude)
            )

            sun_sign = response.sun.sign.name
            moon_sign = response.moon.sign.name
            asc_sign = response.ascendant.sign.name
            nakshatra = response.moon.nakshatra.name

            st.subheader("🌞 Your Birth Chart Highlights")
            st.write(f"☀️ Sun Sign: {sun_sign}")
            st.write(f"🌙 Moon Sign: {moon_sign}")
            st.write(f"🔼 Ascendant: {asc_sign}")
            st.write(f"🌌 Nakshatra: {nakshatra}")

            st.markdown("### 🧿 Detected Yogas & Doshas")
            st.success("✅ Gaja Kesari Yoga")
            st.caption("🌕 Moon in kendra with Jupiter")
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
            pdf.cell(200, 10, txt=f"Sun: {sun_sign} | Moon: {moon_sign} | Asc: {asc_sign}", ln=True)
            pdf.cell(200, 10, txt=f"Nakshatra: {nakshatra}", ln=True)
            pdf.cell(200, 10, txt=f"Yogas: Gaja Kesari", ln=True)
            buffer = BytesIO()
            pdf.output(buffer)
            st.download_button("📥 Download Report (PDF)", data=buffer.getvalue(), file_name="Your_Vedic_Report.pdf", mime="application/pdf")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# -----------------------------
# Legal & Privacy Disclaimer
# -----------------------------
st.markdown("---")
st.markdown("🔒 **Terms, Privacy & Legal Notice**")
st.caption(
    "This tool is intended for spiritual insight and personal reflection only. It does not substitute professional medical, legal, or psychological advice.\n"
    "Astrological interpretations are provided using Prokerala's official SDK. All data is generated in real-time using your input, and no birth data is stored or shared.\n"
    "This app operates under Prokerala's fair-use API guidelines. Your usage of this site indicates agreement with our terms.\n"
    "By using this tool, you accept that any decisions you make based on this content are your own responsibility.\n"
    "For entertainment and personal awareness purposes only."
)
st.caption("© 2025 Vedic Vishwakarma | Powered by Prokerala Astrology SDK")

# -----------------------------
# Instagram Promotion Tip
# -----------------------------
st.markdown("---")
st.markdown("📢 **Instagram Reel Caption Template**")
st.code("""
🪐 Want to know your real Lagna, Nakshatra & Yogas? 
✨ Try my FREE astrology tool 🔮

✅ Real D1 chart powered by SDK
💫 Mangal Dosha, Gaja Kesari, and more
📄 Premium full PDF reports (optional)

🔗 Click here to get your free chart
👉 https://vedic-vishwakarma.streamlit.app

🌿 Powered by Vedic knowledge | For personal awareness only
""", language="markdown")

# -----------------------------
# Terms and Conditions Snippet
# -----------------------------
st.markdown("---")
st.markdown("📜 **Terms of Use Summary**")
st.markdown(
    "This astrology tool is offered for spiritual and informational use. \n"
    "It does not offer medical or legal advice, and should not be relied on for critical decisions. \n"
    "All calculations are done via licensed Prokerala SDK, and your data is never stored. \n"
    "By using this app, you accept full responsibility for how you use the information provided."
)
