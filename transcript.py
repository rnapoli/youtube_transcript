import sys
import csv
import json
import unicodedata
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from fpdf import FPDF
import os
import urllib.request


def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    elif query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        elif query.path.startswith('/embed/'):
            return query.path.split('/')[2]
    raise ValueError("❌ Invalid YouTube URL format")


def fetch_best_transcript(video_id):
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

        preferred_langs = ['en-GB', 'en-UK', 'en', 'en-US']
        for lang in preferred_langs:
            try:
                return transcripts.find_manually_created_transcript([lang])
            except:
                continue

        return transcripts.find_generated_transcript(['en'])

    except TranscriptsDisabled:
        print("❌ Transcripts are disabled for this video.")
        sys.exit(1)
    except NoTranscriptFound:
        print("❌ No transcript found for this video.")
        sys.exit(1)


def normalize_text(text):
    text = text.replace('\u00A0', ' ')
    text = unicodedata.normalize('NFKD', text)
    text = text.replace('\n', ' ').replace('\r', ' ')
    return ' '.join(text.split())


def write_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(["Start Time (s)", "Duration (s)", "Text"])
        for entry in data:
            writer.writerow([
                round(entry.start, 2),
                round(entry.duration, 2),
                normalize_text(entry.text)
            ])
    print(f"✅ CSV saved to {filename}")


def write_json(data, filename):
    output = [
        {
            "start": round(entry.start, 2),
            "duration": round(entry.duration, 2),
            "text": normalize_text(entry.text)
        }
        for entry in data
    ]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ JSON saved to {filename}")


def download_font(font_path):
    print("📥 Downloading DejaVuSans.ttf...")
    url = "https://raw.githubusercontent.com/dejavu-fonts/dejavu-fonts/master/ttf/DejaVuSans.ttf"
    try:
        urllib.request.urlretrieve(url, font_path)
        print(f"✅ Font downloaded to {font_path}")
    except Exception as e:
        print(f"❌ Failed to download font: {e}")
        sys.exit(1)




def write_pdf(data, filename):
    import re

    def to_ascii(text):
        text = normalize_text(text)
        return text.encode("ascii", "ignore").decode("ascii")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    pdf.cell(200, 10, txt="YouTube Transcript", ln=True, align='C')
    pdf.ln(10)

    for entry in data:
        start = round(entry.start, 2)
        duration = round(entry.duration, 2)
        text = to_ascii(entry.text)
        line = f"[{start}s - {start + duration}s] {text}"
        pdf.multi_cell(0, 8, line)
        pdf.ln(1)

    pdf.output(filename)
    print(f"✅ PDF saved to {filename}")




if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcript.py <YouTube URL>")
        sys.exit(1)

    video_url = sys.argv[1]

    try:
        video_id = extract_video_id(video_url)
        transcript = fetch_best_transcript(video_id)
        transcript_data = transcript.fetch()

        base_filename = f"{video_id}"

        write_csv(transcript_data, f"{base_filename}.csv")
        write_json(transcript_data, f"{base_filename}.json")
        write_pdf(transcript_data, f"{base_filename}.pdf")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
