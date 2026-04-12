import os
import requests
import pandas as pd
import re
import math
from deep_translator import GoogleTranslator
from word2number import w2n
from dotenv import load_dotenv
from datetime import datetime

def parse_duration(pt_str):
    if not pt_str:
        return '00:00'
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', pt_str)
    if not match:
        return pt_str
    h = int(match.group(1) or 0)
    m = int(match.group(2) or 0)
    s = int(match.group(3) or 0)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

# Load environment variables from .env file
load_dotenv()

# 1. Your Credentials & Target
API_KEY = os.getenv("YOUTUBE_API_KEY")
if not API_KEY:
    raise ValueError("Missing YOUTUBE_API_KEY! Please set it in your .env file.")

PLAYLIST_ID = "UUIB65_E_7XEScU2NB135wDw"  # Coke Studio Bangla Uploads
BASE_URL = "https://www.googleapis.com/youtube/v3/playlistItems"

print("Fetching video IDs via pagination loop...")

# 2. The Pagination Loop: Getting ALL videos
video_ids = []
next_page_token = None

while True:
    query_params = {
        'part': 'contentDetails',
        'playlistId': PLAYLIST_ID,
        'maxResults': 50,
        'key': API_KEY
    }
    
    if next_page_token:
        query_params['pageToken'] = next_page_token
        
    response = requests.get(BASE_URL, params=query_params).json()
    
    # Extract IDs and append to our master list
    for item in response.get('items', []):
        video_ids.append(item['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    
    # Break the loop if there are no more pages
    if not next_page_token:
        break

print(f"Found {len(video_ids)} total videos. Fetching statistics in batches...")

# 3. Fetch Statistics in Batches of 50 and Categorize Dynamically
stats_url = "https://www.googleapis.com/youtube/v3/videos"
video_data = []

# Loop through our IDs in chunks of 50
for i in range(0, len(video_ids), 50):
    chunk = video_ids[i:i+50]
    
    stats_params = {
        'part': 'statistics,snippet,contentDetails',
        'id': ','.join(chunk),  # Joins up to 50 IDs with commas
        'key': API_KEY
    }
    
    stats_response = requests.get(stats_url, params=stats_params).json()
    
    for item in stats_response.get('items', []):
        title = item['snippet']['title']
        description = item['snippet'].get('description', '')
        text_for_search = title + " " + description
        
        # -- DYNAMIC LOGIC --
        
        # A. Translate Title early
        try:
            eng_title = GoogleTranslator(source='auto', target='en').translate(title)
        except Exception:
            eng_title = title  # Fallback to original if translation fails
            
        # B. Parse Description Metadata early
        spotify_link = None
        spotify_match = re.search(r'(?i)(?:Listen on Spotify|Spotify):\s*(https://open\.spotify\.com/[^\s]+)', description)
        if spotify_match:
            spotify_link = spotify_match.group(1)
            
        director = None
        director_match = re.search(r'(?i)Director:\s*([A-Za-z\s\.]+)', description)
        if director_match:
            director = director_match.group(1).strip()
            
        vocals = []
        for line in description.split('\n'):
            line = line.strip()
            if not line or 'engineer' in line.lower() or 'arrangement' in line.lower():
                continue
            # Handle both formats: "Artist: Vocals" (S2/S3) and "Artist - Vocals" (S1)
            if 'vocal' in line.lower():
                # Colon format: e.g. "Vocals: Arnob" or "Lead Vocals: Arnob"
                if ':' in line:
                    parts = line.split(':', 1)
                    left, right = parts[0].strip(), parts[1].strip()
                    artist = right if 'vocal' in left.lower() else left
                # Dash format: e.g. "Arnob - Vocals" or "Arnob - Lead Vocals"
                elif ' - ' in line:
                    parts = line.split(' - ', 1)
                    left, right = parts[0].strip(), parts[1].strip()
                    artist = left if 'vocal' in right.lower() else right
                else:
                    continue
                artist = re.sub(r'\(.*?\)', '', artist).strip()  # Clean up brackets
                # Skip lines that are clearly not artist names (too long or contain symbols)
                if artist and len(artist) < 60 and not re.search(r'[/@#]', artist):
                    vocals.append(artist)
        vocals_str = ', '.join(vocals) if vocals else None

        # C. Prioritized Video Type 
        is_shorts = re.search(r'(?i)#shorts|shorts\b', text_for_search)
        is_reels = re.search(r'(?i)#reels|reels\b', text_for_search)
        is_bts = re.search(r'(?i)Behind The Magic|BTS|Making|Set Design', title)
        is_milestone = re.search(r'(?i)million|views?-এ|ফেলেছে|অভিনন্দন|congratulat', title)
        is_live = re.search(r'(?i)\blive\b|লাইভ', title)
        is_promo = re.search(r'(?i)Teaser|Promo|Trailer|Announcement|আসছে', title)
        
        if is_shorts:
            video_type = "Shorts"
        elif is_reels:
            video_type = "Reels"
        elif is_bts:
            video_type = "Behind the Scenes"
        elif is_milestone:
            video_type = "Celebration / Milestone"
        elif is_live:
            video_type = "Live Event"
        elif is_promo:
            video_type = "Promo / Teaser"
        elif spotify_link or vocals_str:
            video_type = "Official Music Video"
        else:
            video_type = "Uncategorized"

        # F. Genre Detection (only for Official Music Videos)
        GENRE_KEYWORDS = {
            'Folk': ['folk', 'baul', 'bhatiali', 'bhawaiya', 'hajong', 'lalon', 'marfati', 'jari', 'sari'],
            'Qawwali': ['qawwali', 'qawali', 'qalandar', 'sufi'],
            'Rock': ['rock', 'metal', 'hard rock', 'alternative'],
            'Pop': ['pop'],
            'Classical': ['classical', 'raga', 'thumri', 'kheyal'],
            'Fusion': ['fusion'],
            'Latin': ['latin', 'bossa nova', 'samba'],
            'Jazz': ['jazz'],
            'R&B / Soul': ['r&b', 'soul', 'blues'],
            'Hip-Hop': ['hip-hop', 'rap', 'hip hop'],
        }
        if video_type == "Official Music Video":
            detected_genres = []
            desc_lower = description.lower()
            for genre, keywords in GENRE_KEYWORDS.items():
                if any(kw in desc_lower for kw in keywords):
                    detected_genres.append(genre)
            # Default to Fusion for CSB since it's always cross-genre
            if not detected_genres:
                detected_genres = ['Fusion']
            genre_str = ', '.join(detected_genres)
        else:
            genre_str = "Not Applicable"
        
        # D. Extract the Season dynamically
        season_match = re.search(r'(?i)(?:CokeStudioBanglaSeason|CokeStudioBanglaS|CSB S|Season)\s*(\d+|one|two|three|four)', text_for_search)
        season = "Uncategorized"
        if season_match:
            season_val = season_match.group(1).lower()
            try:
                season_num = w2n.word_to_num(season_val)
                season = f"Season {season_num}"
            except ValueError:
                season = f"Season {season_val.title()}"

        # Clean Missing Values
        vocals_str = vocals_str if vocals_str else "Not Applicable"
        spotify_link = spotify_link if spotify_link else "Not Applicable"
        director = director if director else "Not Applicable"
        
        # E. Fetch Thumbnails & Metadata
        thumbnails = item['snippet'].get('thumbnails', {})
        thumbnail_url = None
        if 'maxres' in thumbnails:
            thumbnail_url = thumbnails['maxres'].get('url')
        elif 'high' in thumbnails:
            thumbnail_url = thumbnails['high'].get('url')
        elif 'standard' in thumbnails:
            thumbnail_url = thumbnails['standard'].get('url')
        elif 'medium' in thumbnails:
            thumbnail_url = thumbnails['medium'].get('url')
        elif 'default' in thumbnails:
            thumbnail_url = thumbnails['default'].get('url')
            
        video_url = f"https://www.youtube.com/watch?v={item['id']}"
        duration_raw = item['contentDetails'].get('duration', '')
        duration_fmt = parse_duration(duration_raw)
        last_updated = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        video_data.append({
            'Video_ID': item['id'],
            'Video_URL': video_url,
            'Title': title,
            'English_Title': eng_title,
            'Published_At': pd.to_datetime(item['snippet']['publishedAt']).strftime('%Y-%m-%d'),
            'Video_Duration': duration_fmt,
            'Views': int(item['statistics'].get('viewCount', 0)),
            'Likes': int(item['statistics'].get('likeCount', 0)),
            'Comments': int(item['statistics'].get('commentCount', 0)),
            'Video_Type': video_type,
            'Season': season,
            'Lead_Vocals': vocals_str,
            'Spotify_Link': spotify_link,
            'Director': director,
            'Thumbnail_URL': thumbnail_url,
            'Genre': genre_str,
            'Last_Updated': last_updated,
            'Video_Details': description
        })

# 4. Save to your local directory
df = pd.DataFrame(video_data)
output_path = "coke_studio_bangla_raw.csv"

try:
    df.to_csv(output_path, index=False)
    print(f"Success! Dataset saved to: {output_path}")
except PermissionError:
    import time
    fallback_path = f"coke_studio_bangla_raw_{int(time.time())}.csv"
    df.to_csv(fallback_path, index=False)
    print(f"\n⚠️ PermissionError: '{output_path}' was open and locked.")
    print(f"Success! Dataset was safely saved instead to: {fallback_path}")