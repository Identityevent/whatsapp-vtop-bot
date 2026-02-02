from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

# --------- PUT YOUR VTOP LOGIN HERE ---------
VTOP_REGNO = "23BCE9275"
VTOP_PASSWORD = "Leodas@7106"
# --------------------------------------------

@app.route("/")
def home():
    return "WhatsApp VTOP Bot is Running 🚀"

def get_attendance_from_vtop():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get("https://vtop.vitap.ac.in/vtop/login")
        time.sleep(5)

        # Login
        driver.find_element(By.ID, "regno").send_keys(VTOP_REGNO)
        driver.find_element(By.ID, "passwd").send_keys(VTOP_PASSWORD)
        driver.find_element(By.ID, "loginsubmit").click()
        time.sleep(8)

        # Go to Attendance page
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
        return "Error fetching attendance. Try again later."
    finally:
        driver.quit()

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
