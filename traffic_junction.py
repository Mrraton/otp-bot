import requests
import time
import re

# --- আপনার তথ্য ---
API_URL = "http://pscall.net/restapi/smsreport"
API_KEY = "SFVWRz1SS4Nyko5_QU5PQg=="
BOT_TOKEN = "8290299840:AAHHo35kgjM6kcY1vIqvIqtBv03RKnlzNpM"
GROUP_ID = "-1003355962140"

# লিঙ্কগুলো
CHAT_GROUP_LINK = "https://t.me/+-jtNnTJfo0VjNzU1"
NUMBER_CHANNEL_LINK = "https://t.me/TrafficJunction999"
DEVELOPER_PROFILE = "https://t.me/Unknown000121" # আপনার প্রোফাইল লিঙ্ক

def get_flag(country_info):
    country_info = str(country_info).lower()
    if "tunisia" in country_info: return "🇹🇳"
    if "venezuela" in country_info or "ve" in country_info: return "🇻🇪"
    if "bangladesh" in country_info: return "🇧🇩"
    if "india" in country_info: return "🇮🇳"
    return "🌍"

def send_to_telegram(otp_full_msg, service, num, country_data):
    flag = get_flag(country_data)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # নাম্বার ফরম্যাট: শেষ ৪ ডিজিটের আগের ৩ ডিজিট কেটে TJN বসানো
    num_str = str(num)
    if len(num_str) >= 7:
        last_4 = num_str[-4:]
        front_part = num_str[:-7]
        formatted_num = f"{front_part}TJN{last_4}"
    else:
        formatted_num = f"TJN{num_str[-4:] if len(num_str) > 4 else num_str}"

    # ওটিপি কোড আলাদা করা
    otp_code = re.findall(r'\b\d{3,7}\b', otp_full_msg)
    final_otp = otp_code[0] if otp_code else "Check SMS"

    # প্রফেশনাল বক্স ডিজাইন
    # এখানে [Developer @Unknown000121] অংশটি ক্লিক করলে প্রোফাইলে নিয়ে যাবে
    text = (
        f"┏━━━━━━◤ **OTP** ◢━━━━━━┓\n"
        f"┃ {flag} #VE  🟢 `{formatted_num}`\n"
        f"┃\n"
        f"┃ **Developer ⚡** [@Unknown000121]({DEVELOPER_PROFILE})\n" 
        f"┗━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"💫🔐 *OTP (Click to Copy) :*\n"
        f"`{final_otp}`"
    )
    
    payload = {
        "chat_id": GROUP_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True, # প্রোফাইল প্রিভিউ বন্ধ রাখতে
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "📞 NUMBER ↗️", "url": CHAT_GROUP_LINK},
                    {"text": "📺 CHANNEL ↗️", "url": NUMBER_CHANNEL_LINK}
                ]
            ]
        }
    }
    
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def start_bot():
    last_id = ""
    print(f"🚀 লেটেস্ট ওটিপি এবং প্রোফাইল লিঙ্ক সহ বট চালু হয়েছে!")
    headers = {"User-Agent": "Mozilla/5.0"}

    while True:
        try:
            params = {"key": API_KEY, "start": 0, "length": 1}
            response = requests.get(API_URL, params=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                json_data = response.json()
                if json_data.get("result") == "success":
                    data_list = json_data.get("data", [])
                    if data_list:
                        latest = data_list[0]
                        date_id = latest.get("dateadded")

                        if date_id != last_id:
                            if last_id != "":
                                send_to_telegram(
                                    latest.get("sms"), 
                                    latest.get("cli"), 
                                    latest.get("num"), 
                                    latest.get("smsrange")
                                )
                                print(f"✅ নতুন ওটিপি পাঠানো হয়েছে: {latest.get('cli')}")
                            last_id = date_id
            
        except Exception as e:
            print(f"❌ এরর: {e}")

        time.sleep(2)

if __name__ == "__main__":
    start_bot()
