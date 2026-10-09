# GameMatch AI — Gaming Profile Matching & Recommendation System

## Overview
GameMatch AI is a Python application designed to estimate compatibility between gamers using profile information and gaming preferences. It combines text similarity with a feedback-learning component to support profile matching.

## Features
- **Profile matching:** Compares textual profile information using TF-IDF and cosine similarity.
- **Compatibility scoring:** Combines matching signals into a compatibility score.
- **Feedback learning:** Includes a Logistic Regression-based component intended to incorporate feedback into matching.
- **Interactive interface:** Uses Streamlit.

> Before publishing, confirm that each feature described here matches the implementation in this repository.

## Technologies
- Python
- scikit-learn
- Streamlit
- pandas
- NumPy

## Project Files
The repository contains Python modules for matching, feedback learning, data generation, configuration, utilities, and performance analysis, along with data and saved model/artifact files.

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/ajaynarasimha-stud/game-match-ai.git
cd game-match-ai
```

### 2. Create a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
If the repository contains `requirements.txt`, run:
```bash
pip install -r requirements.txt
```

If it does not, inspect the imports in the source files and install the required packages.

### 4. Run the application
If the Streamlit entry-point file is `app.py`, run:
```bash
streamlit run app.py
```
If the entry point has another filename, use that filename instead. Confirm the correct entry point from the source files before running.

## How It Works
1. Profile information is prepared for matching.
2. TF-IDF converts textual information into numerical features.
3. Cosine similarity compares profile representations.
4. Matching signals are combined to calculate compatibility scores.
5. The feedback-learning component uses Logistic Regression according to the implementation and available data.

## Reproducibility Notes
- Confirm that the saved model is compatible with the installed scikit-learn version.
- Ensure CSV files contain no private or sensitive information.
- Document how saved model and output files were generated.
- Add screenshots or a demo link if available.

## Limitations
Matching quality depends on the profile data, scoring design, and available feedback. This project is a learning and demonstration application, not a validated production recommendation system.

## Author
Ajay Narasimha Vijay
