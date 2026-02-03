import setuptools  # <-- ADD THIS LINE FIRST

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os

app = Flask(__name__)

# --------- PUT YOUR VTOP LOGIN HERE ---------
VTOP_REGNO = "23BCE9275"
VTOP_PASSWORD = "Leodas@7106"
# --------------------------------------------

def get_driver():
    """
    Creates a headless Chrome that works on Render
    """
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # This line is critical for Render
    options.binary_location = "/usr/bin/chromium"

    driver = uc.Chrome(options=options)
    return driver


def get_attendance_from_vtop():
    driver = get_driver()

    try:
        driver.get("https://vtop.vitap.ac.in/vtop/login")
        time.sleep(6)

        driver.find_element(By.ID, "regno").send_keys(VTOP_REGNO)
        driver.find_element(By.ID, "passwd").send_keys(VTOP_PASSWORD)
        driver.find_element(By.ID, "loginsubmit").click()
        time.sleep(8)

        driver.get("https://vtop.vitap.ac.in/vtop/student/attendance")
        time.sleep(8)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        rows = soup.find_all("tr")
        result = "📚 *Your Attendance*\n\n"

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 8:
                course = cols[2].text.strip()
                percent = cols[6].text.strip()
                debar = cols[8].text.strip()

                if percent:
                    line = f"• {course} — {percent}"
                    if "Debar" in debar:
                        line += " ⚠️(Debarred)"
                    result += line + "\n"

        return result

    except Exception as e:
        print("Error:", e)
        return "⚠️ Error fetching attendance. Try again."

    finally:
        driver.quit()


@app.route("/")
def home():
    return "WhatsApp VTOP Bot is Running 🚀"


@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming = request.form.get("Body", "").lower()
    reply = MessagingResponse()
    msg = reply.message()

    if "attendance" in incoming:
        msg.body("Fetching your attendance... ⏳")
        attendance = get_attendance_from_vtop()
        msg.body(attendance)

    else:
        msg.body("Send: attendance")

    return str(reply)

