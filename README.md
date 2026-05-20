# GoPro Batch Downloader

Download **all** your GoPro Plus cloud media in bulk — no 25-file limit, no hassle.

GoPro Plus subscribers are stuck with a 25-file download cap on the website. This free tool (a simplified and optimized version of the original `gopro-plus` utility) removes that limit and lets you download your entire library directly to your computer.

---

## Quick Start (Windows)

### Step 1 — Install Python (one-time)

If you don't already have Python installed:

1. Go to [python.org/downloads](https://www.python.org/downloads/) and click the big **"Download Python"** button.
2. **Important!** On the installer's first screen, check the box that says **"Add Python to PATH"** before clicking Install.
3. Finish the installation.

### Step 2 — Download This Tool

1. Download this project as a ZIP from GitHub (green **"Code"** button → **"Download ZIP"**).
2. Extract the ZIP to a folder on your computer (e.g. your Desktop or Downloads).

### Step 3 — Install Dependencies (one-time)

1. Open the extracted folder.
2. **Double-click `install.bat`** and wait for it to finish.
3. You should see **"Setup Completed Successfully!"** — you're ready to go.

### Step 4 — Get Your GoPro Credentials

You need two pieces of information from the GoPro website. This takes about 60 seconds:

1. Open your browser (Chrome or Firefox recommended).
2. Go to [plus.gopro.com/media-library](https://plus.gopro.com/media-library/) and **sign in**.
3. Press **F12** on your keyboard (or right-click → "Inspect") to open Developer Tools.
4. Click the **Network** tab at the top of the Developer Tools panel.
5. Type **`user`** into the filter/search box.
6. Click on any request that appears in the list.
7. Look for the **Cookies** section and find these two values:
   - **`gp_access_token`** — a very long string starting with `eyJ...`
   - **`gp_user_id`** — a shorter ID like `436979f8-a681-4f1b-9fc4-5949e7a5fbc9`

> **Tip:** You can also find these by clicking on any network request, going to the **Headers** tab, and scrolling down to the **Cookie** section.

### Step 5 — Run the Downloader

1. **Double-click `run.bat`**.
2. If this is your first time, the tool will ask you to paste your credentials:
   - It will ask for your **AUTH_TOKEN** — paste the long `gp_access_token` value and press Enter.
   - It will ask for your **USER_ID** — paste the `gp_user_id` value and press Enter.
   - It will ask for a **download folder** — type a folder path (e.g. `G:/goprodownloads`) or just press Enter to use the default.
3. Your credentials are saved automatically so you won't be asked again.
4. The tool will start downloading your files one by one!

---

## How It Works

- Downloads each file individually for maximum reliability.
- Automatically **skips files you've already downloaded** — you can stop and restart at any time without losing progress.
- If a download fails (e.g. internet drops), it **retries up to 3 times** before moving on.
- Files are saved as raw `.MP4` / `.JPG` files directly in your download folder — no ZIP files to deal with.

---

## FAQ

### Can I stop and resume later?
**Yes!** Just close the window and double-click `run.bat` again whenever you want. It will skip everything you've already downloaded and pick up where it left off.

### How do I download only a few files?
When you double-click `run.bat`, it will ask you:

```
How many files would you like to download?

  - Press ENTER to download everything
  - Or type a number (e.g. 10) to download only that many

Your choice:
```

Just type a number (e.g. `10`) and press Enter. It will download that many files and then stop. The next time you run it, it will skip the files you already have and continue from where you left off.

### My token expired — what do I do?
GoPro tokens expire after a while. Simply:
1. Log into [plus.gopro.com/media-library](https://plus.gopro.com/media-library/) again.
2. Grab a fresh `gp_access_token` and `gp_user_id` using the steps above.
3. Open the `.env` file in the project folder with Notepad and update the values.

### Where is my `.env` file?
It's in the same folder as `run.bat`. It may be hidden by default — in File Explorer, click **View** → check **Hidden items** to see it.

### Can I change the download folder?
Open the `.env` file with Notepad and change the `DOWNLOAD_PATH` line:
```
DOWNLOAD_PATH=D:/MyGoPro/Videos
```

---

## For Advanced Users

If you prefer using the command line:

```powershell
# Activate the virtual environment
.venv\Scripts\Activate.ps1

# Run the downloader (downloads everything, skips existing files)
python main.py

# Download only a specific number of files
python main.py --limit 20
```

### Configuration

All settings are stored in a `.env` file in the project root:

```env
AUTH_TOKEN=your_gp_access_token_here
USER_ID=your_gp_user_id_here
DOWNLOAD_PATH=G:/goprodownloads
```

If the `.env` file doesn't exist when you run the tool, you'll be prompted to enter your credentials interactively.

---

## Requirements

- **Python 3.10+** — [Download here](https://www.python.org/downloads/)
- **Windows** (macOS/Linux users: use `python3 -m venv .venv && pip3 install -r requirements.txt && python3 main.py`)

---

## Credits & Attribution

This tool is a simplified, user-friendly, and optimized batch downloader based on the original [gopro-plus](https://github.com/itsankoff/gopro-plus) project by [Ivaylo Tsankov (itsankoff)](https://github.com/itsankoff).

### Key Improvements in This Fork:
- **Zero-Dependency Installation:** Added an automated `install.bat` that sets up a local Python virtual environment and installs everything with a single click.
- **No Command-Line Required:** Interactive `run.bat` script prompts users for credentials (`gp_access_token` and `gp_user_id`) and download limit options dynamically.
- **Robustness:** Simplified codebase focused purely on fast, direct batch downloads with automatic retry mechanism and skip-matching.
- **Clean Structure:** Removed all Docker, containerization, and build pipeline code to keep the project lightweight and dedicated to local user execution.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
Copyright (c) 2023 Ivaylo Tsankov
Copyright (c) 2026 timcarpe
