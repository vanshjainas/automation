import os
import pickle
import time
import random
from instagrapi import Client

# --- Read accounts from accounts.txt ---
def load_accounts(file_path):
    accounts = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) >= 2:
                username = parts[0].strip()
                password = parts[1].strip()
                accounts.append({"username": username, "password": password})
    return accounts

# --- Load accounts ---
ACCOUNTS_FILE = "accounts.txt"
accounts = load_accounts(ACCOUNTS_FILE)

# --- Provide comments for each account manually ---
comments = [
    "fr sometimes silence says more than words 😶‍🌫️",
    "this one's a vibe fr 🧘‍♀️🌾",
    "no reaction, just observing. that’s the mood 😌👁️",
    "some things just need you to *be there* 💭✨",
    "the peace in this >>> 🧘‍♂️",
    "felt this in my soul ngl 🌌",
    "lowkey wanna live in this moment forever 🌅",
    "quiet doesn’t mean weak. it means wise 🧠🕊️",
    "this gave my mind a break 😮‍💨",
    "brb finding stillness like this 🌾📴",
    "not everything needs a post or a story 📵🌙",
    "the calm this pic brings is unreal 😮‍💨💗",
    "me when I realize I don’t always have to respond 🔇🧍‍♀️",
    "peaceful minds win the loudest battles 🤝🕊️",
    "sometimes just breathing is enough 😌💨",
    "i didn’t know i needed to read this 🫂",
    "idk why this made me tear up a little 🥹",
    "just vibes. no chaos. just stillness 🤍",
    "deep breaths and deeper thoughts 🧘‍♀️💭",
    "maturity is learning when to stay silent 🤫💡",
    "stillness = real luxury these days 💆‍♂️📴",
    "omg this caption speaks FACTS 🔥🧠",
    "protecting my peace like this 🛡️🧘",
    "been trying to live more like this lately 🌿",
    "why does this feel like a hug? 🫂🧡",
    "sometimes presence is the loudest love 💌",
    "this is your sign to pause. just pause ⏸️🧠",
    "this energy feels safe 🤍🧍",
    "caption hit harder than expected 😵‍💫",
    "thank you for putting this into words 💬🫶",
    "mood: staring into the sky with no thoughts ☁️🌥️",
    "my mind after reading this: calm. just calm 🧘‍♀️",
    "so underrated to just exist in the moment 🧍🌍",
    "pause without guilt. feel without noise 🛑💭",
    "don’t react. just breathe. just feel 🫁",
    "the girl, the cat, the sunset... perfection 💫🐾",
    "no more explaining myself. just vibes 📴🤍",
    "life’s too short to rush through moments like these 🕰️🌿",
    "wish we talked more about inner peace like this ☯️",
    "this belongs in a museum of emotions 🎨🖼️",
    "the stillness that screams truth 📣💭",
    "protect this energy at all costs 🚫🌊",
    "mental reset activated 💆‍♀️📴",
    "just me, myself & the moment 🧍‍♀️🌄",
    "needed this reminder more than I knew 🫠🧡",
    "unbothered. centered. still. ✅🧘‍♀️",
    "don’t explain. don’t justify. just exist 🌌🧠",
    "okay but this is art AND therapy 🎭🧠",
    "pausing > performing 🔄🚫",
    "just observing life like 👁️👄👁️",
    "quiet moments hit diff 🫶🫧",
    "when your soul matches the sunset 🌅🧘‍♀️",
    "less noise, more presence 📴💭",
    "this is what peace *feels* like 🕊️💆",
    "gonna come back to this post when life feels loud 🔁🔇",
    "silence is a whole language. and I’m learning it 🔤💤",
    "some posts just... feel like home 🏡🫂"
]




# --- Check count match ---
if len(accounts) != len(comments):
    print("❌ Number of comments must match number of accounts in accounts.txt")
    exit()

# --- Cookies folder ---
COOKIE_DIR = "cookies"
os.makedirs(COOKIE_DIR, exist_ok=True)

# --- Target Reel URL ---
POST_URL = "https://www.instagram.com/reel/DLzoVgTTrJ-/?igsh=MWJ5bnN4OTBuaHV1dA=="

# --- Extract media_id using the first account (login required) ---
first_account = accounts[0]
temp_client = Client()

try:
    temp_client.login(first_account["username"], first_account["password"])
    media_id = temp_client.media_id(temp_client.media_pk_from_url(POST_URL))
    print(f"📌 Found media ID: {media_id}")
except Exception as e:
    print("❌ Failed to extract media ID:", e)
    exit()
# --- Main loop ---
for idx, account in enumerate(accounts):
    username = account["username"]
    password = account["password"]
    comment_text = comments[idx]
    cookie_path = os.path.join(COOKIE_DIR, f"{username}.pkl")

    print(f"\n🔄 [{idx + 1}/{len(accounts)}] Processing: {username}")

    cl = Client()

    # --- Load or login session ---
    if os.path.exists(cookie_path):
        try:
            with open(cookie_path, "rb") as f:
                cl = pickle.load(f)
            cl.get_timeline_feed()  # Validate session
            print("✅ Loaded session from cookie.")
        except Exception:
            print("⚠️ Cookie invalid, logging in again...")
            try:
                cl.login(username, password)
                with open(cookie_path, "wb") as f:
                    pickle.dump(cl, f)
                print("✅ Logged in & session saved.")
            except Exception as e:
                print(f"❌ Login failed for {username}: {e}")
                continue
    else:
        try:
            cl.login(username, password)
            with open(cookie_path, "wb") as f:
                pickle.dump(cl, f)
            print("✅ Logged in & session saved.")
        except Exception as e:
            print(f"❌ Login failed for {username}: {e}")
            continue

       # --- Like and Comment with retry option ---
    while True:
        try:
            cl.media_like(media_id)
            print("❤️ Liked the post.")
            cl.media_comment(media_id, comment_text)
            print(f"✅ Commented: {comment_text}")
            break
        except Exception as e:
            print(f"❌ Error during like/comment: {e}")
            retry = input("🔁 Retry with this account? (y/n): ").strip().lower()
            if retry != 'y':
                print("⏭️ Skipping to next account.")
                break
            else:
                print("🔁 Retrying in 5 seconds...")
                time.sleep(5)


    # time.sleep(random.uniform(1,2))  # Delay between accounts
