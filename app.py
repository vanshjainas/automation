from flask import Flask, render_template, request, redirect, url_for, flash
from instagrapi import Client
import os
import json
import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = "supersecretkey"

SESSIONS_FILE = "sessions.json"
SCHEDULED_FILE = "scheduled_posts.json"

def load_sessions():
    with open(SESSIONS_FILE, "r") as f:
        return json.load(f)

def load_scheduled():
    with open(SCHEDULED_FILE, "r") as f:
        return json.load(f)

def save_scheduled(data):
    with open(SCHEDULED_FILE, "w") as f:
        json.dump(data, f, indent=2)

def download_reel(url, sessionid=None, username=None):
    import subprocess
    import uuid

    output_name = f"downloads/{str(uuid.uuid4())}.mp4"
    try:
        result = subprocess.run([
            "yt-dlp", "-o", output_name, url
        ], capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(output_name):
            return output_name
        else:
            print("yt-dlp error:", result.stderr)
    except Exception as e:
        print("yt-dlp exception:", e)
    
    return None


def post_to_instagram(account_name, video_path, caption):
    try:
        cl = Client()
        sessions = load_sessions()
        cl.set_settings(sessions[account_name])
        cl.login_by_sessionid(sessions[account_name]["authorization_data"]["sessionid"])
        cl.reel_upload(video_path, caption)
        print(f"✅ Posted to {account_name}: {caption}")
        return True
    except Exception as e:
        print(f"❌ Error posting: {e}")
        return False

def check_scheduler():
    while True:
        now = datetime.now().timestamp()
        scheduled = load_scheduled()
        remaining = []
        for task in scheduled:
            if task["timestamp"] <= now:
                path = download_reel(task["url"])
                if path:
                    post_to_instagram(task["account"], path, task["caption"])
                    os.remove(path)
            else:
                remaining.append(task)
        save_scheduled(remaining)
        time.sleep(60)

@app.route("/", methods=["GET", "POST"])
def index():
    sessions = load_sessions()
    accounts = list(sessions.keys())
    if request.method == "POST":
        reel_url = request.form.get("reel_url")
        account = request.form.get("account")
        caption = request.form.get("caption") or "#wolfinroyals"
        post_time = request.form.get("post_time")
        if post_time:
            ts = datetime.strptime(post_time, "%Y-%m-%dT%H:%M").timestamp()
            task = {"url": reel_url, "account": account, "caption": caption, "timestamp": ts}
            scheduled = load_scheduled()
            scheduled.append(task)
            save_scheduled(scheduled)
            flash("✅ Reel scheduled successfully!", "success")
        else:
            video_path = download_reel(reel_url)
            if video_path:
                if post_to_instagram(account, video_path, caption):
                    flash("✅ Posted successfully!", "success")
                else:
                    flash("❌ Failed to post", "error")
                os.remove(video_path)
            else:
                flash("❌ Failed to download the reel", "error")
        return redirect(url_for("index"))
    return render_template("index.html", accounts=accounts)

if __name__ == "__main__":
    os.makedirs("downloads", exist_ok=True)
    t = threading.Thread(target=check_scheduler, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000)
