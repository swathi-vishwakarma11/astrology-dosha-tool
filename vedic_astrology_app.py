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

🔹 **Lagna Chart + Doubt Clearing (Messages)** – ₹999  
Know your chart. Ask anything. Get clear answers.

🔹 **30-Min Focused Call (Love / Career / Health)** – ₹1999  
One topic. Straightforward guidance and remedies.

🔹 **1-Hour Full Chart Call** – ₹3999  
All areas covered + Remedies + PDF summary.

🔹 **Two Charts Reading** – ₹5000  
For those on a shared journey — deep connection insights.

🪐 *Your Lagna Chart holds the truth — I’ll help you understand it with clarity.*
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
### 💡 What You’ll Gain From a Reading

🔭 **Accurate Horoscope Interpretation & Karmic Guidance**  
❤️ **Relationship Compatibility, Twin Flame & Soulmate Karma**  
👶 **Delay in Conception, Fertility & Health Blocks Cleansing**  
💼 **Career Destiny Clarity & Wealth Block Removal**  
🧿 **Powerful Dosha Analysis + Energy Cleansing Rituals**  
🕉 **Personalized Lal Kitab Remedies & Spiritual Healing**

✨ *Every consultation is deeply intuitive, spiritually guided, and leaves you with clarity you’ll never regret.*
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
- All sessions are deeply personal, intuitive and rooted in traditional Vedic astrology.
- Your data is never stored, sold or reused.
- Consultations are prepaid and non-refundable once started.

---
🪷 **Copyright © 2025 Vedic Vishwakarma**  
✨ Follow [@vedic.vishwakarma](https://instagram.com/vedic.vishwakarma) for daily astro tips & healing codes 🌙
""")
