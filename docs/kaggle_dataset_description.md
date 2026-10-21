# Kaggle dataset description (copy-paste into Kaggle)

**Subtitle (max 80 chars):**
Daily YouTube metrics & metadata for every Coke Studio Bangla video

**Tags:** music, youtube, bangladesh, entertainment, data visualization, time series

**License:** CC BY-NC-SA 4.0

---

## About Dataset

This dataset tracks **every video on the Coke Studio Bangla YouTube channel** and is **updated daily** from the YouTube Data API v3. Each row is one video, with engagement metrics (views, likes, comments) plus enriched metadata: video type, season, genre, lead vocalists, director and Spotify link.

**🔴 Live dashboard:** https://sarandnath.shinyapps.io/coke-studio-bangla-day10-v2/
**💻 Source code:** https://github.com/saranDnath/coke-studio-bangla-dataset

### Columns

| Column | Description |
|---|---|
| Video_ID | YouTube video ID |
| Video_URL | Link to the video |
| Title | Original title (Bangla / English) |
| English_Title | Title machine-translated to English |
| Published_At | Upload date (YYYY-MM-DD) |
| Video_Duration | Length (mm:ss or hh:mm:ss) |
| Views / Likes / Comments | Engagement counts at collection time |
| Video_Type | Official Music Video, Shorts, Reels, Behind the Scenes, Celebration / Milestone, Live Event, Promo / Teaser, Uncategorized |
| Season | Season number detected from title/description, else "Uncategorized" |
| Genre | Comma-separated genres for official music videos (e.g. "Folk, Fusion"); "Not Applicable" for other types |
| Lead_Vocals | Lead singers parsed from the description credits (backing vocals excluded) |
| Director | Music-video director parsed from the credits |
| Spotify_Link | Spotify link if listed in the description |
| Thumbnail_URL | Highest-resolution thumbnail available |
| Last_Updated | Timestamp when the row was collected |
| Video_Details | Full video description |

### How the labels are created

- **Video_Type:** rule-based, in priority order: `#Shorts` → `#Reels` → Behind the Magic / BTS → milestone titles ("million views") → Live → Teaser / Promo → clips ≤ 90 s (Shorts) → videos with vocal credits or a Spotify link (Official Music Video).
- **Genre:** whole-word keyword matching on the song's story paragraphs only (credits are ignored). Videos with no genre keyword default to *Fusion*.
- These labels are heuristic. Please open a discussion if you find a misclassified video.

### Source & disclaimer

Data is collected from the public YouTube Data API v3. All music, videos and trademarks belong to Coke Studio Bangla and their respective owners. This is an independent analytics project and is not affiliated with The Coca-Cola Company.
