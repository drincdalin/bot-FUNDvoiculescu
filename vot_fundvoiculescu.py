import time
import random
import string
import requests
import undetected_chromedriver as uc
import json
import os
import sys
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# ================== CONFIG ==================
CANDIDATE_NAME = "un anumit candidat nu zicem but be sure ca numele e ca si ala de pe card"
NUM_VOTES = 2000
RESTART_EVERY = 10   # restart browser la fiecare X voturi ca sa nu se blocheze
# ===========================================

# fix path pentru cand ruleaza ca .exe
if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
    os.environ["PYTHONIOENCODING"] = "utf-8"
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(SCRIPT_DIR, "votes_log.json")

print("Logs saved in: " + LOG_FILE)

# sleep random ca sa para human
def random_sleep(min_sec=3, max_sec=8):
    time.sleep(random.uniform(min_sec, max_sec))

# incarca logurile vechi daca exista
def load_logs():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

# salveaza un vot in json
def save_log(entry):
    logs = load_logs()
    logs.append(entry)
    try:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        print(f"Logged (Total: {len(logs)})")
    except:
        print("Failed to save log")

# porneste chromedriver
def create_driver():
    try:
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=129)
        return driver
    except Exception as e:
        print("Driver error: " + str(e))
        raise

# creeaza cont temporar pe mail.tm
def get_mail_tm_account():
    try:
        BASE_URL = "https://api.mail.tm"
        domains_resp = requests.get(f"{BASE_URL}/domains", timeout=10)
        domain = domains_resp.json()['hydra:member'][0]['domain']
        
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        email = f"{username}@{domain}"
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        account_data = {"address": email, "password": password}
        requests.post(f"{BASE_URL}/accounts", json=account_data, timeout=10)
        token_resp = requests.post(f"{BASE_URL}/token", json=account_data, timeout=10)
        token = token_resp.json()['token']

        print("Email creat: " + email)
        return email, token
    except Exception as e:
        print("Mail.tm error: " + str(e))
        return None, None

# cauta codul de verificare in email
def get_verification_code(token, timeout=60):
    if not token:
        return None
    BASE_URL = "https://api.mail.tm"
    headers = {"Authorization": f"Bearer {token}"}
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            resp = requests.get(f"{BASE_URL}/messages", headers=headers, timeout=10)
            for msg in resp.json().get('hydra:member', []):
                msg_resp = requests.get(f"{BASE_URL}/messages/{msg['id']}", headers=headers, timeout=10)
                data = msg_resp.json()
                body = data.get('text', '') or data.get('html', '')
                
                if any(word in (body.lower()) for word in ['cod', 'liga', 'confirm', 'vote']):
                    code_match = re.search(r'\b(\d{6})\b', body)
                    if code_match:
                        code = code_match.group(1)
                        print("Code gasit: " + code)
                        return code
        except:
            pass
        time.sleep(4)
    print("No code received")
    return None

# click mai sigur (js + normal)
def safe_click(driver, element):
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.7)
        driver.execute_script("arguments[0].click();", element)
        return True
    except:
        try:
            element.click()
            return True
        except:
            return False

# functia principala de vot
def vote_for_candidate():
    success = 0
    driver = None

    for i in range(NUM_VOTES):
        # restart browser din cand in cand
        if driver is None or (success > 0 and success % RESTART_EVERY == 0):
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            print("Restarting browser...")
            driver = create_driver()

        print(f"ATTEMPT {i+1}/{NUM_VOTES} | Success: {success}")

        try:
            driver.get("https://vot.fundatiadanvoiculescu.ro/")
            random_sleep(8, 12)

            email, token = get_mail_tm_account()
            if not email: 
                continue

            # gaseste cardul candidatului
            card = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((
                    By.XPATH, f"//h5[contains(., '{CANDIDATE_NAME}')]/ancestor::div[contains(@class, 'wpvc_card_row')]"
                ))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
            random_sleep(2, 3.5)

            # apasa voteaza
            vote_btn = card.find_element(By.XPATH, ".//button[contains(., 'Votează')]")
            safe_click(driver, vote_btn)
            random_sleep(3, 5)

            # introduce email
            email_input = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email_address']"))
            )
            email_input.clear()
            email_input.send_keys(email)
            random_sleep(1.5, 2.5)

            # checkbox terms
            try:
                chk = driver.find_element(By.CSS_SELECTOR, "input[name='voter_terms'], input[type='checkbox']")
                if not chk.is_selected():
                    safe_click(driver, chk)
            except: 
                pass

            # trimite cod
            send_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Trimite codul')]"))
            )
            safe_click(driver, send_btn)
            random_sleep(4, 7)

            # introduce codul primit pe mail
            code_input = WebDriverWait(driver, 25).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='enter_email_code']"))
            )
            code = get_verification_code(token, timeout=55) or "000000"
            code_input.clear()
            code_input.send_keys(code)
            random_sleep(2, 3.5)

            # verifica codul
            verify_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Verifică codul')]"))
            )
            safe_click(driver, verify_btn)

            # asteapta mesaj de succes
            WebDriverWait(driver, 18).until(
                EC.any_of(
                    EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "succes"),
                    EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "mulțumim"),
                    EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Votează')]"))
                )
            )

            save_log({
                "timestamp": datetime.now().isoformat(),
                "candidate": CANDIDATE_NAME,
                "email_used": email,
                "attempt": i + 1,
                "status": "SUCCESS"
            })

            success += 1
            random_sleep(10, 15)

        except Exception as e:
            print("Error on attempt " + str(i+1) + ": " + str(type(e).__name__))
            random_sleep(8, 12)

    if driver:
        try:
            driver.quit()
        except:
            pass
    return success

if __name__ == "__main__":
    print("Bot started")
    total = vote_for_candidate()
    print("Run finished - " + str(total) + " successful votes")
    print("Total logged: " + str(len(load_logs())))
