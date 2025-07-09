import pickle
import time
import random
from instagrapi import Client

# --- Load saved client from pickle file ---
COOKIE_FILE = "avvnii__craze_cookies.pkl"
# COOKIE_FILE = "avvnii__craze_cookies.pkl"

try:
    with open(COOKIE_FILE, "rb") as f:
        cl: Client = pickle.load(f)
    print("✅ Successfully loaded Instagram session from cookie file.")
except Exception as e:
    print("❌ Failed to load cookie file:", e)
    exit()

# --- Confirm session is valid ---
try:
    user_info = cl.account_info()
    print(f"🔐 Logged in as: {user_info.username}")
except Exception as e:
    print("❌ Session expired or invalid:", e)
    exit()

# --- Target Reel URL ---
POST_URL = "https://www.instagram.com/reel/DLU-LYgRyBB/?igsh=MThseW1oeDh2NmtrYw=="

# --- Comment list (20 unique ones) ---
COMMENTS = [
    "@vansh_jain_17 #givaway2025",
    "#givaway2025 @creep_sen",
    "@vansh_jain_17",
    "@vansh_jain_17 wish to be the one",
    "@creep_sen",
    "@man_kind_0001",
    "@bca_batch",

    # Single emoji only
    "🎉",
    "🤞",
    "❤️",
    "🔥",
    "💖",
    "🎁",
    "🙏",
    "😇",
        "🎉",
    "🤞",
    "❤️",
    "🔥",
    "💖",
    "🎁",
    "🙏",
    "😇",
    
    
    

    # Single friend mentions only
    "@CharviChicx_19",
    "@riya_tiwariyyy",
    "@prisha.ink_",
    "@eesha.eclipsed",
    "@anika.chapters_",
    "@ana.nyavibes",
    "@Jhanvi.jn",
    "@shreya.aesthetic.x",
    "@harshita.hearts27",
    "@veda._vibes07",
    "@navya.verse_27",
    "@avvnii__craze",
    "@MehkaaVibes_23",
    "@RuhaniTales99",
    "@NairaSparkz_21",
    "@TanishqaDreams07",
    "@MirayaMystic_22",
    "@RidhiRaga_08",
    "@DesiDhaaniyaa_07",
    "@KavyaaGlow_11",
    "@IndieSuhana_18",
    "@ZyroNovaX",
    "@PixelWisp_07",
    "@VortiqEcho",
    "@BlinkNestle",
    "@SnazzyFloe",
    "@Cravezyne",
    "@TwilixirVibe",
    "@QuirxoBolt",
    "@DazlynTrek",
    "@Aarohaii",
    "@niha.rika20016",
    "@priya.nkkkkaaaa",
    "@riii_.iiya",
    "@meesraaaaa.a",
    "@tannn_vi",
    "@saaaaanvika",
    "@i_shi_.ta",
    "@triiisha_a",
    "@si_mmmiiiii",
]


# --- Number of comments to post ---
NUM_COMMENTS = 80

# --- Convert post URL to media ID ---
try:
    media_id = cl.media_id(cl.media_pk_from_url(POST_URL))
    print(f"📌 Found media ID: {media_id}")
except Exception as e:
    print("❌ Failed to extract media ID:", e)
    exit()

# --- Comment posting loop ---
for i in range(NUM_COMMENTS):
    try:
        comment_text = random.choice(COMMENTS)
        cl.media_comment(media_id, comment_text)
        print(f"[{i+1}/{NUM_COMMENTS}] ✅ Commented: {comment_text}")
        time.sleep(random.uniform(3, 6))  # Random delay to avoid spam detection
    except Exception as e:
        print(f"[{i+1}] ❌ Error posting comment:", e)
        time.sleep(10)  # Longer delay after error
