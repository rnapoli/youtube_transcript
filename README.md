# YouTube Transcript Downloader

A Python script that extracts the most accurate YouTube transcript available and automatically generates:

* 📄 Clean CSV (with line-break–free captions)
* 📘 Structured JSON
* 📑 Simple printable PDF

Supports manual or auto-generated captions, prefers human-reviewed subtitles like **"English (United Kingdom)"**, and works on **Windows, macOS, and Linux**.

---

## ✅ Features

* Automatically detects and extracts video ID from any YouTube link
* Prefers manually-created transcripts over auto-generated ones
* Normalizes smart quotes, symbols, and Unicode
* Creates 3 clean output formats: `.csv`, `.json`, `.pdf`
* Works without downloading any external fonts
* No browser automation or Selenium required

---

## 🚀 Installation

### 1. Clone the repo or download the script

```bash
git clone https://github.com/yourusername/youtube-transcript-downloader.git
cd youtube-transcript-downloader
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, use:

```bash
pip install youtube-transcript-api fpdf
```

---

## 🛠 Usage

```bash
python transcript.py https://www.youtube.com/watch?v=VIDEO_ID
```

This will generate:

* `VIDEO_ID.csv`  – Clean caption text with timestamps
* `VIDEO_ID.json` – Machine-readable transcript
* `VIDEO_ID.pdf`  – ASCII-safe, printable version

### Example

```bash
python transcript.py https://www.youtube.com/watch?v=-d8Hj0SEFR0
```

---

## 🧩 Example Output (CSV)

```
"Start Time (s)","Duration (s)","Text"
"2.88","5.84","This is a portable handheld computer released in 2025, but it feels much more like a"
"8.72","6.48","retro 8-bit computer, even if it is a lot more capable than those."
```

---

## 🧰 Requirements

* Python 3.7+
* `youtube-transcript-api`
* `fpdf`

---

## 📁 Project Structure

```
youtube-transcript-downloader/
├── transcript.py            # Main script
├── README.md                # This file
├── requirements.txt         # Dependencies
```

---

## 📝 License

MIT License

---

## 🙌 Credits

* [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
* [fpdf2](https://py-pdf.github.io/fpdf2/)

---

## 💡 Coming Soon (Ideas)

* `--lang` option to specify transcript language
* `--start` / `--end` to limit range
* Word count and duration stats
* Markdown output for docs/blogs

---

Feel free to fork, contribute, or request a feature!

