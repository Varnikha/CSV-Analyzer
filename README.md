
# 🔎 Insightly — CSV Data Analyzer

> A simple, generic web app to upload any CSV file and instantly explore its structure, statistics, and trends — no coding required.

Built with **Python + Streamlit + pandas**.

---

## ✨ Features

- **Universal CSV Upload** — works with any CSV file, automatically detects numeric and text columns
- **Key Metrics Dashboard** — total rows, most common category, average of a chosen numeric column
- **Search & Filter** — search across every column at once, and download the filtered results
- **Summary Statistics** — automatic mean, min, max, and percentiles for all numeric columns
- **Group & Analyze** — group data by any category column, with count/average/sum and a chart (bar, line, or area)
- **Data Reliability Indicator** — shows how many records contributed to each calculated average, so you know how trustworthy each number is
- **Missing Data Report** — see exactly which columns have missing values, and how many

---

## 🖥️ Tech Stack

| Layer | Technology |
|---|---|
| App framework | [Streamlit](https://streamlit.io) |
| Data processing | [pandas](https://pandas.pydata.org) |
| Numerical computing | [NumPy](https://numpy.org) (used internally by pandas) |
| Language | Python 3 |

---

## 📂 Project Structure

```
Insightly/
├── app.py                   # Main Streamlit app
├── requirements.txt         # Python dependencies
├── .streamlit/
│   └── config.toml          # Theme/branding configuration
└── README.md
```

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/CSV-Analyzer.git
cd CSV-Analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the app
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## 🌐 Live Demo

🔗 [Insightly on Streamlit Cloud](https://csv-analyzer-sgfzr7mzrkukdy6ux5mdk8.streamlit.app)

---

## 📊 How It Works

1. **Upload** any CSV file through the drag-and-drop uploader
2. Insightly automatically detects which columns are **numeric** and which are **text/category**
3. Explore your data across four tabs:
   - **Home & Search** — key metrics, search, and export
   - **Summary Stats** — statistical overview of numeric columns
   - **Group & Analyze** — grouped breakdowns with charts
   - **Missing Data** — data quality check

---

## 🛠️ Possible Improvements

- Support for Excel (`.xlsx`) file uploads
- Export charts as image files
- User-uploaded custom themes

---
👩‍💻 Author

Built as a hands-on learning project to understand data analysis with pandas and building interactive web apps with Streamlit.
