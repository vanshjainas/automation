import os
import pickle
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
import time

# ---------- CONFIG ----------
ACCOUNTS_FILE = "accounts.txt"
COOKIE_FOLDER = "cookies"
os.makedirs(COOKIE_FOLDER, exist_ok=True)
# ----------------------------

def load_accounts(file_path):
    accounts = []
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) >= 2:
                username, password = parts[0], parts[1]
                accounts.append((username.strip(), password.strip()))
    return accounts

def load_cookies(driver, path):
    try:
        with open(path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                if "expiry" in cookie and isinstance(cookie["expiry"], float):
                    cookie["expiry"] = int(cookie["expiry"])
                try:
                    driver.add_cookie(cookie)
                except:
                    pass
    except Exception as e:
        print(f"Error loading cookies: {e}")

def login_with_cookies_only(username):
    cookie_path = os.path.join(COOKIE_FOLDER, f"{username}.pkl")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.instagram.com/")
    time.sleep(2)

    if os.path.exists(cookie_path):
        load_cookies(driver, cookie_path)
        driver.refresh()
    else:
        messagebox.showwarning("No Cookies", f"No cookie file found for {username}")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Instagram Cookies Login Panel")

# Scrollable Canvas
canvas = tk.Canvas(root, width=450, height=500)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Load accounts and display each with a button
accounts = load_accounts(ACCOUNTS_FILE)

for idx, (username, _) in enumerate(accounts):
    frame = tk.Frame(scrollable_frame, pady=2)
    frame.pack(fill="x", padx=10)

    tk.Label(frame, text=f"{idx + 1}.", width=4).pack(side="left")
    tk.Label(frame, text=username, width=20, anchor="w").pack(side="left")
    tk.Button(frame, text="Login with Cookies", command=lambda u=username: login_with_cookies_only(u)).pack(side="left", padx=5)

root.mainloop()
