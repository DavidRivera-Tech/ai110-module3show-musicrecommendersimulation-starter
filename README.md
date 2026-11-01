# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### How real-world recommenders work

Platforms like Spotify and YouTube predict what you'll enjoy next by combining two approaches. **Collaborative filtering** ignores what a song sounds like and looks at behavior across millions of users: if people who saved the same songs as you also love a track you haven't heard, it becomes a good bet for you. **Content-based filtering** looks at the attributes of the songs themselves (genre, mood, tempo, energy) and recommends songs similar to the ones you already like. Collaborative filtering finds surprising matches but fails on brand-new songs and users (the "cold start" problem), while content-based filtering works from day one and is easy to explain but can trap you in a bubble. Real systems blend both, using signals such as likes, skips, listening time, repeat plays, playlist adds, and song attributes like genre, mood, and tempo. Implicit signals like skips and listening time matter most because there is far more of them than explicit likes.

### Three separate pieces of this system

- **Input data (song features):** the catalog in `data/songs.csv`. Each song is described by its attributes and never changes based on who is listening.
- **User preferences (taste profile):** a small `UserProfile` describing what one listener wants right now: favorite genre, favorite mood, a target energy level, and whether they like acoustic sound.
- **Ranking and selection (scoring rule + ranking rule):**
  - The **scoring rule** judges one song against one user and returns a single number. For numeric features it rewards *closeness* to the user's target (for example `1 - abs(song_energy - target_energy)`), not simply higher or lower values.
  - The **ranking rule** takes every song's score, sorts the whole list, and returns the top results. It works at the list level, which is where later improvements like a diversity penalty (so one artist can't fill the top five) will go.

### What this simplified version prioritizes

This recommender is **content-based only**, since there is a song catalog and a taste profile but no crowd of other users. It prioritizes:

1. **Genre match:** the strongest signal of long-term taste, so it is worth the most points.
2. **Energy closeness:** rewards songs near the user's target energy, not just louder or quieter ones.
3. **Mood match:** what the listener wants to feel right now.

### Features used

**`Song` object** (every column in `data/songs.csv`):

- `id`
- `title`
- `artist`
- `genre`
- `mood`
- `energy` (0-1)
- `tempo_bpm`
- `valence` (0-1)
- `danceability` (0-1)
- `acousticness` (0-1)
- `popularity` (0-100)
- `release_decade`
- `mood_tags` (pipe-separated, e.g. `euphoric|uplifting`)
- `instrumentalness` (0-1)
- `speechiness` (0-1)
- `liveness` (0-1)

**`UserProfile` object:**

- `favorite_genre`
- `favorite_mood`
- `target_energy`
- `likes_acoustic`

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



