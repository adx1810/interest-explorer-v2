# Interest Explorer — Version 2

A real local Flask web app with 15 questions, a professional responsive layout, an interest breakdown, six-sentence personalized summary, potential career directions, and four practical experiments. There is a **Not sure yet** option for every question.

## Run on Windows

1. Extract the ZIP, then open the `interest_explorer_v2` folder (the folder that contains `app.py`).
2. Click the File Explorer address bar, type `cmd`, then press Enter.
3. Run `py -m pip install -r requirements.txt` (first time only).
4. Run `py app.py`.
5. Open `http://127.0.0.1:5000/` in your browser.
6. Leave Command Prompt open while using the website. Press Ctrl+C in Command Prompt to stop the server.

If the old site is already running on port 5000, press **Ctrl+C** in its Command Prompt first. You **do not need to delete your old project**: the new ZIP extracts to a separate folder.

## How it works

- Python (`app.py`) holds all 15 questions, scores answers, and builds the results.
- HTML templates (`templates/`) control the pages.
- CSS (`static/style.css`) controls appearance.
- Flask serves the pages from your laptop.
- Answers are not stored on disk or in a database. They are submitted to the local Flask process when you click results.
- The scores are counts of answer selections, **not** scientifically validated measures of skills, personality, or job fit. Close results with caution, especially if many answers are "not sure" or scores tie.
- Development mode (`debug=True`) is suitable only for local use; do not expose the development server publicly.

## Edit the questions

Open `app.py` in Python IDLE or VS Code and find `QUESTIONS`. Each question has five choices corresponding to five category keys. Save changes and rerun or refresh while Flask's local development reload is active.

## Troubleshooting

- `requirements.txt` not found: Command Prompt is in the wrong folder. Use `dir` and verify that `app.py` and `requirements.txt` are listed.
- Address won't open: type `http://127.0.0.1:5000/` in the browser **address bar**, not into a search result.
- Address already in use: stop the previous Flask process with `Ctrl+C` and run `py app.py` again.
