Вот перевод на английский, структура и пояснения оставлены без изменений кода:

# Perfume Bot MVP

Bot for searching perfumes and their popular clones with savings calculation.

## 📂 Project Structure

```
perfume-bot/
│
├── data/
│   └── perfumes.db
│
├── bot.py                  # only Telegram launch and handlers
├── database.py             # SQLite operations (already provided)
├── search.py               # parsing and search logic (brand/name, fuzzy)
├── formatter.py            # assembling nicely formatted text responses
├── followup.py             # "Hooray! 🎉..." logic (sent once)
├── utils.py                # text normalization, transliteration
│
├── requirements.txt
├── .env
└── README.md
```

---

## 🗄️ Database Structure (SQLite)

The database consists of two main tables:

### 1. `OriginalPerfume` Table

Stores information about original perfumes.

| Column      | Data Type | Description             |
| ----------- | --------- | ----------------------- |
| `id`        | TEXT      | Unique id (Primary Key) |
| `brand`     | TEXT      | Original brand          |
| `name`      | TEXT      | Original name           |
| `price_eur` | REAL      | Original price in euros |
| `url`       | TEXT      | Link to original page   |

### 2. `CopyPerfume` Table

Stores information about perfume clones linked to originals.

| Column         | Data Type | Description 
| -------------- | --------- | ----
| `id`           | TEXT      | Unique id (Primary Key)   
| `original_id`  | TEXT      | Reference to `id` in `OriginalPerfume` (Foreign Key)  
| `brand`        | TEXT      | Clone brand 
| `name`         | TEXT      | Clone name                
| `price_eur`    | REAL      | Clone price in euros 
| `url`          | TEXT      | Link to clone 
| `notes`        | TEXT      | Notes about the scent 
| `saved_amount` | REAL      | Savings in %: `(orig_price_eur - dupe_price_eur) / orig_price_eur * 100` |

```
BOT_TOKEN="YOUR_TOKEN_HERE"
python database.py

pip install -r requirements.txt
python bot.py
```
