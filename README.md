# SuperRR Selector Season 2 — Streamlit Dashboard

## Run locally
1. Install Python 3.10+.
2. Open Terminal in this folder.
3. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Start:
   ```bash
   streamlit run app.py
   ```

## Deploy to Streamlit Community Cloud
1. Create a **new private or public GitHub repository** for the dashboard code.
2. Upload `app.py`, `requirements.txt`, and the `data/` folder.
3. Do not upload the original raw SuperRR data pack. This project includes only derived Top 10 and methodology summary CSVs from the final workbook.
4. Go to https://share.streamlit.io/ and sign in with GitHub.
5. Choose **Create app**, select your repository, branch, and `app.py`, then deploy.
6. When deployment finishes, copy the app URL and paste it into Unstop's optional dashboard link field.

## Included pages
- Overview
- Batting leaderboard
- Bowling leaderboard
- Sensitivity analysis (20%, 25%, 30%)
- Methodology and limitations

## Notes
- The 25% cutoff is the primary model.
- The pressure index is an innings-context proxy, not a direct measure of match leverage or win probability.
- Scores are relative model scores, not probabilities.
