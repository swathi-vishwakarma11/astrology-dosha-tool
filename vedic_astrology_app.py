# vedic_astrology_app.py — Final version with local SDK folder

import streamlit as st
from datetime import datetime, date
from io import BytesIO
from fpdf import FPDF
import sys
import os

st.set_page_config(page_title="Vedic Astrology | Swathi Vishwakarma", layout="centered")
st.title("🌟 Book Personal Vedic Astrology Consultation")

st.markdown("""
### 🙋‍♀️ About Me
I'm **Swathi Vishwakarma**, a Vedic astrologer and spiritual guide with a deep passion for decoding karmic patterns, past-life influences, and planetary doshas.

I specialize in:
- 🔮 **Birth Chart Analysis**
- 💑 **Marriage, Love & Compatibility Insights**
- 👶 **Delay in Childbirth Remedies**
- 📿 **Karmic Healing Guidance**
- 🧿 **Dosha Checks** (Mangal, Nadi, Pitru, Kaal Sarp, etc.)
- 🕉 **Lal Kitab Remedies & Rituals**

All sessions are **voice-only** through Instagram (DM/calls).

---
### 💰 Pricing
- 🧘‍♀️ One-Time Karmic Reading – ₹999
- 💕 Compatibility Reading (Couples) – ₹1499
- 📜 Full PDF Report (Optional Add-on) – ₹199

---
### 📅 Book a Consultation
""")

name = st.text_input("🧑 Your Full Name")
contact = st.text_input("📲 Your Instagram Handle or Email")
birth_date = st.date_input("📅 Date of Birth")
birth_time = st.time_input("🕐 Time of Birth")
birth_place = st.text_input("📍 Place of Birth")
purpose = st.selectbox("💬 What's the purpose of your consultation?", [
    "General Guidance",
    "Marriage/Partner Match",
    "Career & Money",
    "Health or Delay in Childbirth",
    "Spiritual/Karmic Insight",
    "Other"
])

if st.button("📩 Request Booking"):
    if name and contact and birth_place:
        st.success(f"✅ Thank you {name}! I will contact you via {contact} within 24 hours. 💌")
        st.caption("🔔 Please make sure you're following [@vedic.vishwakarma](https://instagram.com/vedic.vishwakarma) on Instagram to receive messages.")
    else:
        st.warning("⚠️ Please fill in all the required fields including birth place.")

st.markdown("""
---
### 💳 Payment QR Code
Scan the QR code below to complete your payment:
""")

st.image("payment_qr.png", caption="Pay via UPI or any mobile wallet", width=250)

st.markdown("""
---
### 📜 Terms & Privacy
- This consultation is based on Vedic astrology principles and is for self-awareness and spiritual growth.
- I do not store or misuse your birth details.
- Payment is to be made before consultation (details will be shared privately).
- No refunds once session starts.

---
© 2025 Vedic Vishwakarma | DM for collaborations
""")
