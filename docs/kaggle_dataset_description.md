### Context
Coke Studio Bangla has revolutionized the music scene in Bangladesh by blending traditional folk, classical, and modern genres. This dataset provides a comprehensive, constantly updating look at the performance of every video on their official YouTube channel. 

**Note:** This dataset is dynamic. It is powered by a scheduled Kaggle Notebook that hits the YouTube Data API v3 and updates the metrics automatically every day. You can view, copy, and learn from the dataset here: https://www.kaggle.com/code/sarandebnath/coke-studio-bangla-youtube-analytics 

### Acknowledgements
Data is sourced directly from the official **Coke Studio Bangla YouTube Channel** via the public Google YouTube Data API v3. 

### Inspiration
This dataset is perfect for:
1.  **Exploratory Data Analysis (EDA):** Which seasons or artists generate the highest engagement rates? 
2.  **Time-Series Analysis:** Tracking the longevity of a song's popularity.
3.  **Data Visualization:** Building beautiful dashboards to track the musical footprint of the show.

**Disclaimer:** All image and branding rights belong to Coke Studio Bangla and The Coca-Cola Company. This dataset is for educational purposes only.

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

