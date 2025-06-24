# vedic_astrology_app.py — Final version with updated pricing, UPI, and enhanced offers

import streamlit as st
from datetime import datetime, date
from io import BytesIO
from fpdf import FPDF
import requests
import json

st.set_page_config(page_title="Vedic Astrology | Swathi Vishwakarma", layout="centered")
st.title("🌠 Book Your Personal Vedic Astrology Consultation ✨")

st.markdown("""
---
### ✨ Astrology Services & Charges ✨

💫 **Lagna Chart + Doubt Clearing (Messages)** – ₹999  
Know your chart. Ask anything. Receive crystal-clear answers.

💫 **30-Min Focused Call (Love / Career / Health)** – ₹1999  
One topic. Pinpointed insights. Powerful remedies.

💫 **1-Hour Full Chart Call** – ₹3999  
Deep dive into all areas + Customized Remedies + PDF Report.

💫 **Two Charts Reading** – ₹5000  
Twin flame or compatibility? Discover shared soul patterns.

🪐 *Your Lagna Chart reveals the truth — I’ll help you see it with soul-level clarity.*
""")

st.markdown("""
---
### 📆 Book Your Session
Fill in your birth details accurately for the most precise reading:
""")

name = st.text_input("👤 Full Name")
contact = st.text_input("📱 Instagram Handle or Email")
birth_date = st.date_input("📅 Date of Birth")
birth_time = st.time_input("🕒 Time of Birth")
birth_place = st.text_input("📍 Place of Birth")
purpose = st.selectbox("🎯 Purpose of the Session", [
    "General Guidance",
    "Marriage/Partner Match",
    "Career & Finances",
    "Health / Childbirth Delay",
    "Karmic & Spiritual Reading",
    "Other (Specify in DM)"
])

if st.button("📩 Confirm Booking"):
    if name and contact and birth_place:
        # Log to Google Sheets via webhook
        sheet_url = "https://sheet.best/api/sheets/1ZxoURNCk4WuCz-SRg8ua3L-aRH9S6i78H9mBpMFC0Mk"
        payload = {
            "Name": name,
            "Contact": contact,
            "Birth Date": str(birth_date),
            "Birth Time": str(birth_time),
            "Birth Place": birth_place,
            "Purpose": purpose,
            "Timestamp": str(datetime.now())
        }
        try:
            requests.post(sheet_url, json=payload)
        except:
            st.warning("⚠️ Unable to save to Google Sheet.")

        # Send Email Notification using FormSubmit
        email_form_url = "https://formsubmit.co/ajax/vedicvishwakarma11@gmail.com"
        try:
            requests.post(email_form_url, data={
                "Name": name,
                "Contact": contact,
                "Birth Date": birth_date,
                "Birth Time": birth_time,
                "Birth Place": birth_place,
                "Purpose": purpose
            })
        except:
            st.warning("⚠️ Email could not be sent. Please check manually.")

        st.success(f"🙏 Thank you {name}! You'll be contacted via {contact} within 24 hours.")
        st.info("🔔 Make sure you're following [@vedic.vishwakarma](https://instagram.com/vedic.vishwakarma) on Instagram to receive messages.")
    else:
        st.warning("⚠️ Please fill in your name, contact and place of birth.")

st.markdown("""
---
### 🌟 What You’ll Experience in a Reading

🔭 **Accurate Horoscope Interpretation & Karmic Guidance**  
❤️ **Relationship Compatibility, Twin Flame & Soulmate Karma**  
👶 **Conception Delay, Fertility & Health Karma Cleansing**  
💼 **Career Destiny Clarity & Wealth Block Removal**  
🧿 **Dosha Diagnosis & Deep Energy Cleansing Rituals**  
🕉 **Lal Kitab Remedies & Personalized Spiritual Guidance**

✨ *Each session brings divine clarity, emotional relief, and actionable solutions you'll be grateful for.*
""")

st.markdown("""
---
### 💰 UPI Payment Details
Pay through any UPI app using the ID below:

```
📲 UPI ID: swathiastro@upi
```

✅ Once paid, send a *screenshot* via DM or email. You can also take a screenshot here.

📌 *Booking will be confirmed after successful payment.*
""")

st.markdown("""
---
### 🔐 Privacy & Terms
- Your birth details are sacred — never shared or misused.
- All sessions are one-on-one and energetically protected.
- Prepaid bookings only. Non-refundable after session starts.

---
🪷 **© 2025 Vedic Vishwakarma**  
🌙 Follow [@vedic.vishwakarma](https://instagram.com/vedic.vishwakarma) for daily spiritual wisdom.
""")
