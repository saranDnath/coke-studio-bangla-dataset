# 🎵 Coke Studio Bangla — YouTube Dataset Builder

An automated Python pipeline that fetches, enriches, and structures a comprehensive dataset of all **Coke Studio Bangla** YouTube videos using the YouTube Data API v3.

---

## 📦 Dataset on Kaggle (Recommended — No Setup Required!)

I maintain a **live, auto-updating version** of this dataset on Kaggle. If you just want to analyse the data without running the code yourself, you can download it instantly:

```python
import kagglehub

# Download latest version
path = kagglehub.dataset_download("sarandebnath/coke-studio-bangla-youtube-metric-daily-update")

print("Path to dataset files:", path)
```

> The Kaggle dataset is refreshed regularly so it always contains the most up-to-date metrics like views, likes, and comments.

---

## 📁 Project Structure

```
coke_studio_bangla/
├── coke_studio_bangla_dataset.py   # Main pipeline script
├── requirements.txt                # Python dependencies
├── .env                            # Your API key (NOT pushed to GitHub)
├── .gitignore                      # Protects .env and generated files
└── README.md                       # This file
```

---

## 🏗️ What the Dataset Contains

Each row represents one YouTube video from the Coke Studio Bangla channel with the following columns:

| Column             | Description                                                                                                                                                         |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Video_ID`       | Unique YouTube video identifier                                                                                                                                     |
| `Video_URL`      | Direct link to the YouTube video                                                                                                                                    |
| `Title`          | Original video title (Bengali / English)                                                                                                                            |
| `English_Title`  | Auto-translated English title                                                                                                                                       |
| `Published_At`   | Date the video was published (`YYYY-MM-DD`)                                                                                                                       |
| `Video_Duration` | Duration in `MM:SS` or `HH:MM:SS` format                                                                                                                        |
| `Views`          | Total view count                                                                                                                                                    |
| `Likes`          | Total like count                                                                                                                                                    |
| `Comments`       | Total comment count                                                                                                                                                 |
| `Video_Type`     | Category:`Official Music Video`, `Reels`, `Shorts`, `Behind the Scenes`, `Celebration / Milestone`, `Live Event`, `Promo / Teaser`, `Uncategorized` |
| `Season`         | Season number:`Season 1`, `Season 2`, `Season 3`, or `Uncategorized`                                                                                        |
| `Lead_Vocals`    | Lead vocalist(s) extracted from the description                                                                                                                     |
| `Spotify_Link`   | Official Spotify streaming link (if available)                                                                                                                      |
| `Director`       | Music video director (if available)                                                                                                                                 |
| `Genre`          | Detected genres from description (e.g.`Folk, Qawwali, R&B / Soul`). Only assigned for Official Music Videos                                                       |
| `Thumbnail_URL`  | Highest resolution thumbnail URL (for dashboards)                                                                                                                   |
| `Last_Updated`   | Timestamp when the data row was last fetched                                                                                                                        |
| `Video_Details`  | Full raw YouTube video description                                                                                                                                  |

---

## ⚙️ Running the Script Yourself

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/coke-studio-bangla.git
cd coke-studio-bangla
```

### Step 2: Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### Step 3: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Set up your API Key

Create a `.env` file in the project root:

```
YOUTUBE_API_KEY=your_youtube_api_key_here
```

> Get a free YouTube Data API v3 key from the [Google Cloud Console](https://console.cloud.google.com/).

### Step 5: Run the pipeline

```powershell
python coke_studio_bangla_dataset.py
```

This will fetch all videos, enrich them, and save the output as `coke_studio_bangla_raw.csv`.

---

## 🔍 Key Features

- **Full Pagination**: Fetches all videos from the channel, not just the first 50.
- **Smart Categorization**: Uses regex-based priority logic to classify `Video_Type` and `Season` from titles, descriptions, and hashtags.
- **Vocals Extraction**: Parses both colon (`:`) and dash (`-`) formats used across different seasons of CSB.
- **Genre Detection**: Identifies music genres (Folk, Rock, Qawwali, Fusion, Latin, etc.) from video descriptions — only for Official Music Videos.
- **High-Res Thumbnails**: Fetches the best available thumbnail URL (`maxres` → `high` → `standard`) for visual dashboards.
- **Secure by Design**: API key is loaded from a `.env` file and never hardcoded — safe to push to GitHub.
- **Auto Timestamp**: Each row records when it was last fetched via `Last_Updated`.

---

## 🔑 Requirements

- Python 3.8+
- YouTube Data API v3 Key
- See `requirements.txt` for all Python packages

---

## 📄 License

This project is open source. The data is sourced from the public YouTube API and belongs to Coke Studio Bangla / Coca-Cola.
