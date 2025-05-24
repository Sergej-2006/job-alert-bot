import requests
import hashlib
import time
import yagmail
from bs4 import BeautifulSoup
import os

# Konfiguracija
URL = "https://calendar.barcatering.si/"    
CHECK_INTERVAL = 3600  
EMAIL_ADDRESS = "sergej.mandic.sm@gmail.com"
APP_PASSWORD = "sbox qihn glnx zbio"
HASH_FILE = "website_hash.txt"

def get_website_body():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.body
        return str(body)
    except:
        return None

def calculate_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def save_hash(hash_value):
    with open(HASH_FILE, 'w') as f:
        f.write(hash_value)

def load_hash():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, 'r') as f:
            return f.read().strip()
    return None

def send_notification_email():
    try:
        tema = "ODPRTJE DELOVNIH MEST"
        vsebina = f"Sprememba zaznana na {URL}. Prijavi se."
        
        yag = yagmail.SMTP(EMAIL_ADDRESS, APP_PASSWORD)
        yag.send(
            to=EMAIL_ADDRESS,
            subject=tema,
            contents=vsebina
        )
    except:
        pass

def main():
    while True:
        content = get_website_body()
        if not content:
            time.sleep(CHECK_INTERVAL)
            continue
        
        current_hash = calculate_hash(content)
        previous_hash = load_hash()
        
        if previous_hash is None:
            save_hash(current_hash)
        elif previous_hash != current_hash:
            send_notification_email()
            save_hash(current_hash)
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()