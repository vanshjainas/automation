import os
import re
import tkinter as tk
from tkinter import messagebox
import instaloader
from instagrapi import Client

# --- Paths ---
COOKIES_DIR = "cookies"
DOWNLOADS_DIR = "downloads"
os.makedirs(COOKIES_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# --- Download Instagram Reel using instaloader ---
def download_reel(reel_url):
    match = re.search(r"instagram\.com/reel/([A-Za-z0-9_-]+)", reel_url)
    if not match:
        raise ValueError("Invalid Instagram Reel URL.")
    shortcode = match.group(1)

    subfolder = os.path.join(DOWNLOADS_DIR, shortcode)
    os.makedirs(subfolder, exist_ok=True)

    L = instaloader.Instaloader(
        dirname_pattern=subfolder,
        save_metadata=False,
        download_comments=False
    )

    post = instaloader.Post.from_shortcode(L.context, shortcode)
    L.download_post(post, target=subfolder)

    for file in os.listdir(subfolder):
        if file.endswith(".mp4"):
            return os.path.join(subfolder, file)

    raise FileNotFoundError("Downloaded reel video (.mp4) not found.")

# --- Upload Reel using instagrapi with cookies ---
def upload_with_cookies(video_path, caption):
    username = "wolfinroyals"
    password = "adikart"  # Change if needed

    cl = Client()
    cookie_path = os.path.join(COOKIES_DIR, f"{username}.pkl")

    try:
        if os.path.exists(cookie_path):
            cl.load_settings(cookie_path)
            cl.login(username, password)
        else:
            cl.login(username, password)
        cl.dump_settings(cookie_path)
        cl.clip_upload(video_path, caption)
    except Exception as e:
        raise RuntimeError(f"Upload failed: {e}")

# --- Main Button Action ---
def process():
    reel_url = entry_url.get().strip()
    caption = text_caption.get("1.0", tk.END).strip()

    if not reel_url or not caption:
        messagebox.showerror("Missing Info", "Reel URL and caption are required.")
        return

    try:
        btn_process.config(state=tk.DISABLED)
        lbl_status.config(text="⬇️ Downloading Reel...")
        window.update()

        video_path = download_reel(reel_url)

        lbl_status.config(text="⏫ Uploading Reel...")
        window.update()

        upload_with_cookies(video_path, caption)

        lbl_status.config(text="✅ Reel Uploaded Successfully!")
        messagebox.showinfo("Success", f"Reel uploaded to @wolfinroyals\n{video_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        lbl_status.config(text="❌ Upload Failed")
    finally:
        btn_process.config(state=tk.NORMAL)

# --- GUI Setup ---
window = tk.Tk()
window.title("Instagram Reel Reposter")
window.geometry("400x350")

tk.Label(window, text="Reel URL:").pack(pady=(10, 0))
entry_url = tk.Entry(window, width=50)
entry_url.pack(pady=5)

tk.Label(window, text="Caption:").pack(pady=(10, 0))
text_caption = tk.Text(window, height=6, width=45)
text_caption.pack(pady=5)

btn_process = tk.Button(window, text="Download & Upload Reel", command=process)
btn_process.pack(pady=10)

lbl_status = tk.Label(window, text="", fg="blue")
lbl_status.pack()

window.mainloop()
