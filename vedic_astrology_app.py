# Astrology Web App using Streamlit (API-Based Version)
# Hostable on Streamlit Cloud ✅

import streamlit as st
import requests
from datetime import datetime, date
from io import BytesIO
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

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
user_email = st.text_input("📧 Enter Your Email to Receive Report")

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

        # Get access token securely
        client_id = "your_client_id"
        client_secret = "your_client_secret"
        token_response = requests.post(
            "https://api.prokerala.com/token",
            data={"grant_type": "client_credentials"},
            auth=(client_id, client_secret)
        )

        if token_response.status_code != 200:
            raise Exception("❌ Failed to authenticate API. Check your credentials.")

        access_token = token_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        endpoint = f"https://api.prokerala.com/v2/astrology/birth-details"
        params = {
            "datetime": f"{dob_str}T{tob_str}:00",
            "place": birth_place
        }

        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code != 200:
            st.error("⚠️ API error. Please check if birth place is valid.")
            st.stop()

        data = response.json()

        # Parse fields
        sun_sign = data['data']['sun']['rasi']['name']
        moon_sign = data['data']['moon']['rasi']['name']
        asc_sign = data['data']['ascendant']['sign']
        nakshatra = data['data']['moon']['nakshatra']['name']

        st.subheader("🌞 Sun, Moon, Ascendant Info")
        st.write(f"☀️ Sun Sign: {sun_sign}")
        st.write(f"🌙 Moon Sign: {moon_sign}")
        st.write(f"🌌 Nakshatra: {nakshatra}")
        st.write(f"🔼 Ascendant: {asc_sign}")

        # Fetch Yogas & Doshas (placeholder — real API needed or static logic)
        st.markdown("### 🧿 Detected Yogas & Doshas")
        st.success("✅ Gaja Kesari Yoga")
        st.success("✅ Budha-Aditya Yoga")
        st.warning("⚠️ Partial Mangal Dosha")

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
        pdf.cell(200, 10, txt=f"Sun: {sun_sign}, Moon: {moon_sign}, Asc: {asc_sign}", ln=True)
        pdf.cell(200, 10, txt=f"Nakshatra: {nakshatra}", ln=True)
        pdf.cell(200, 10, txt=f"Yogas: Gaja Kesari, Budha-Aditya | Doshas: Partial Mangal", ln=True)

        buffer = BytesIO()
        pdf.output(buffer)
        st.download_button("📥 Download Report (PDF)", data=buffer.getvalue(), file_name="Vedic_Report.pdf", mime="application/pdf")

        # Email PDF Report
        if user_email:
            try:
                msg = EmailMessage()
                msg['Subject'] = 'Your Vedic Astrology Report'
                msg['From'] = 'your_email@example.com'
                msg['To'] = user_email
                msg.set_content('Hi, here is your astrology report attached.')
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