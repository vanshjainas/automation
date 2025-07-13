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
    "this is peace redefined 🔥",
    "brb building my own tent 🏕️",
    "never knew words could hug like this",
    "needed this reminder today fr",
    "silent resets > loud escapes",
    "this post feels like home",
    "shelter isn't hiding, it's healing",
    "a tent for the mind... wow",
    "the kind of peace we all deserve",
    "bro this hit different",
    "logging out to log in 🧠",
    "cried a little not gonna lie",
    "this made me breathe slower",
    "actual soul food 🔥",
    "gonna save this forever",
    "can we talk about this art too??",
    "this vibe is everything rn",
    "who else needed this today?",
    "peace looks good on everyone",
    "reset is my fav button",
    "not escaping. just resting. 💆",
    "i wanna live inside this caption",
    "shelter my soul plss",
    "the world’s loud, i’m tired",
    "tent > traffic",
    "i feel safe just reading this",
    "kinda wanna disappear into this",
    "introvert anthem unlocked",
    "this is aesthetic therapy",
    "pure serotonin post 🌌",
    "me rn: 🧍‍♂️🏕️🔥",
    "real peace never asks for attention",
    "not dramatic but i need this life",
    "caption so soft it healed me",
    "i miss this kind of quiet",
    "reset isn’t weakness",
    "why does this feel like a dream",
    "one word: sheltered",
    "turning this into my wallpaper",
    "quiet places are sacred",
    "a campfire for the soul 🔥",
    "less noise, more peace",
    "this post hugged me",
    "emotionally camping here now",
    "i claim this kind of calm",
    "biggest truth in smallest words",
    "deep breaths and forest thoughts",
    "healing looks like this",
    "reality needs more of this energy",
    "not all who wander want noise",
    "bro this caption is SO ME",
    "this tent >>> my room rn",
    "i’m in love with this idea",
    "sometimes solitude is sacred",
    "soft reminder we needed today",
    "this feels like a sunday morning",
    "this tent’s in my mind now",
    "i felt that. deeply.",
]






# --- Check count match ---
if len(accounts) != len(comments):
    print("❌ Number of comments must match number of accounts in accounts.txt")
    exit()

# --- Cookies folder ---
COOKIE_DIR = "cookies"
os.makedirs(COOKIE_DIR, exist_ok=True)

# --- Target Reel URL ---
POST_URL = "https://www.instagram.com/reel/DL91jxyT4IX/?igsh=ZmxlNW50Z2NubDE="

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
