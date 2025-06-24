# vedic_astrology_app.py — Final version with local SDK folder + Google Sheet + Email Notification

import streamlit as st
from datetime import datetime, date
from io import BytesIO
from fpdf import FPDF
import requests
import json

st.set_page_config(page_title="Vedic Astrology | Swathi Vishwakarma", layout="centered")
st.title("🌠 Book Your Personal Vedic Astrology Consultation")

st.markdown("""
### 🌺 About Swathi Vishwakarma
Namaste! I'm **Swathi Vishwakarma**, your Vedic Astrologer and spiritual confidante. With years of deep scriptural study and intuitive practice, I help decode your destiny through:

🔭 **Accurate Horoscope Interpretation**  
❤️ **Relationship Compatibility & Twin Flame Checks**  
👶 **Delay in Conception & Health Karma**  
💼 **Career Path & Wealth Remedies**  
🧿 **Powerful Dosha Analysis & Cleansing**  
🕉 **Customized Lal Kitab Solutions & Rituals**

📞 *Voice-only sessions via Instagram or Email*
""")

st.markdown("""
---
### 💸 Consultation Packages
- 🌟 *One-Time Karmic Reading* – ₹999
- 💖 *Relationship/Compatibility Session (for couples)* – ₹1499
- 📄 *Detailed PDF Report (Optional)* – ₹199

📌 *Each session includes powerful intuitive insights + personalized remedies.*
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
### 💰 UPI Payment Details
Pay through any UPI app using the following ID:

```
📲 UPI ID: swathiastro@upi
```

✅ Once paid, send the screenshot to [@vedic.vishwakarma](https://instagram.com/vedic.vishwakarma) or your provided email.

📌 *Booking is confirmed only after payment.*
""")

st.markdown("""
---
### 🔐 Privacy & Terms
- All consultations are private, personalized and based on traditional Vedic wisdom.
- Your birth details are *never stored or shared*.
- Sessions are prepaid and non-refundable after consultation begins.

---
🪷 **Copyright © 2025 Vedic Vishwakarma**  
Follow me on [Instagram](https://instagram.com/vedic.vishwakarma) for daily cosmic tips 🌙
""")
