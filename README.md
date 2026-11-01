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

### Algorithm Recipe

Each song gets a score from 0 to 5.0 by adding up these rules:

| Rule | Points |
|---|---|
| Genre match | **+2.0** if `song.genre == favorite_genre`, otherwise 0 |
| Mood match | **+1.0** if `song.mood == favorite_mood`, otherwise 0 |
| Energy closeness | **1.5 × (1 − \|song energy − target energy\|)** |
| Acoustic preference | If `likes_acoustic`: **+0.5 × acousticness**. Otherwise: **+0.5 × (1 − acousticness)** |

Numeric features reward **closeness, not higher or lower values**. A song with energy 0.80 earns full energy points for a user targeting 0.80, and a song at 0.95 earns fewer, even though it is "more energetic." Likewise, a user who dislikes acoustic music earns points from songs with *low* acousticness, not from songs with high or low values in general.

**Data flow:**

```
INPUT                    PROCESS                               OUTPUT
-----                    -------                               ------
User preferences   -->   Load every song from songs.csv  -->   Sort songs by score
(genre, mood,            For each song:                        (highest first)
 target energy,            apply the scoring rules             Return the top k
 likes acoustic)           to get one score                    recommendations
```

### Expected Biases

- **Genre can dominate.** At +2.0 it is the largest single reward, so a song in the favorite genre can outrank a song that is a near-perfect mood and energy match but in a different genre. Great matches outside the user's genre get pushed down the list.
- **Thin genres give weak results.** Most genres in the catalog have only one song, and only pop, lofi, and jazz have more than one. A user whose favorite genre is, say, metal gets one genre bonus to hand out. After that song, the rest of the list is ranked only by mood, energy, and acousticness.
- **Exact string matching is brittle.** `indie pop` does not match `pop`, and a mood like `focused` does not match `chill`, even though a listener might enjoy both. Close matches get zero credit.
- **Features outside the rules are ignored.** Valence, tempo, danceability, and the other new columns do not affect the score, so two songs that feel very different can score the same.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

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

This is the first of the six profiles that `python -m src.main` runs (High-Energy Pop: pop / happy / energy 0.8 / not acoustic):

```
PROFILE: High-Energy Pop
========================
Preferences: genre=pop, mood=happy, energy=0.8, likes_acoustic=False

1. Sunrise City by Neon Echo  (score: 4.88)
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.82 vs target 0.80 (+1.47)
     - acousticness 0.18, prefers non-acoustic (+0.41)

2. Gym Hero by Max Pulse  (score: 3.78)
     - genre match (+2.00)
     - energy 0.93 vs target 0.80 (+1.30)
     - acousticness 0.05, prefers non-acoustic (+0.47)

3. Afterglow Avenue by Neon Echo  (score: 3.72)
     - genre match (+2.00)
     - energy 0.68 vs target 0.80 (+1.32)
     - acousticness 0.20, prefers non-acoustic (+0.40)

4. Rooftop Lights by Indigo Parade  (score: 2.77)
     - mood match (+1.00)
     - energy 0.76 vs target 0.80 (+1.44)
     - acousticness 0.35, prefers non-acoustic (+0.33)

5. Concrete Crown by Kid Meridian  (score: 1.91)
     - energy 0.78 vs target 0.80 (+1.47)
     - acousticness 0.12, prefers non-acoustic (+0.44)
```

The results match what a pop/happy listener would expect: Sunrise City (4.88) is #1 because it is the only song to earn both the genre and mood bonuses (and its energy is almost on target), and the other two pop songs, Gym Hero (3.78) and Afterglow Avenue (3.72), come next. Rooftop Lights (2.77) got no genre points because "indie pop" does not exactly match "pop", which is the string-matching bias predicted in Expected Biases. With the +2.00 genre bonus it would have scored 4.77 and ranked #2, so a near-perfect match for this listener is pushed down to fourth. See [model_card.md](model_card.md) section 7 for the output of the other five profiles.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Weight shift: genre 2.0 → 1.0 and energy 1.5 → 3.0

**What I changed.** I halved the genre bonus and doubled the energy closeness weight, which raises the maximum possible score from 5.0 to 5.5 (1.0 + 1.0 + 3.0 + 0.5). I ran all six profiles, then restored the original weights.

**High-Energy Pop (pop, happy, energy 0.8, not acoustic)**

| Rank | Before (genre 2.0, energy 1.5) | Score | After (genre 1.0, energy 3.0) | Score |
|---|---|---|---|---|
| 1 | Sunrise City | 4.88 | Sunrise City | 5.35 |
| 2 | Gym Hero | 3.78 | Rooftop Lights | 4.21 |
| 3 | Afterglow Avenue | 3.72 | Gym Hero | 4.08 |
| 4 | Rooftop Lights | 2.77 | Afterglow Avenue | 4.04 |
| 5 | Concrete Crown | 1.91 | Concrete Crown | 3.38 |

**Edge Case: Classical but High Energy (classical, melancholic, energy 0.9, likes acoustic)**

| Rank | Before (genre 2.0, energy 1.5) | Score | After (genre 1.0, energy 3.0) | Score |
|---|---|---|---|---|
| 1 | Nocturne in Blue Hour | 2.86 | Storm Runner | 3.02 |
| 2 | Crossroads Lament | 2.17 | Crossroads Lament | 3.01 |
| 3 | Storm Runner | 1.53 | Fuego en la Calle | 2.96 |
| 4 | Fuego en la Calle | 1.51 | Gym Hero | 2.94 |
| 5 | Gym Hero | 1.48 | Pulse Theory | 2.90 |

**More accurate, or just different?** Mostly different, with one clear improvement. For the classical profile, the old #1 was Nocturne in Blue Hour, a 0.15-energy song for a listener who asked for 0.9, and it dropped out of the top 5 entirely. For the pop profile, the happy indie pop song Rooftop Lights moved ahead of two actual pop songs, which is defensible but not obviously better.

**Trade-off.** Doubling the energy weight fixed the classical problem, but it made the system behave more like a plain energy sort. In the classical results, the scores are bunched between 2.90 and 3.02, so tiny energy differences decide the order, and the one classical song is gone. A listener who truly wants classical music would now be poorly served.

**Weights reverted.** I restored genre 2.0 and energy 1.5 after the experiment, and `git diff src/recommender.py` showed no changes. All the other results in this README and the model card use the original weights.

---

## Limitations and Risks

- **Genre dominates a tiny catalog.** The +2.00 genre bonus is larger than the most energy closeness can add (1.50), and 14 of the 17 genres have only one song. A 0.15-energy classical song ranked #1 (2.86) for a listener who wanted energy 0.9.
- **Exact, case-sensitive matching.** "Pop" does not match "pop". The Capitalized Input profile dropped Sunrise City from 4.88 to 1.47 with no warning.
- **Sparse moods.** There is no "sad" mood, and 9 of the 15 moods appear on just one song.
- **No input validation.** An energy target of 2.0 gives all 22 songs negative energy points.
- **Artist repetition.** Neon Echo holds #1 and #3 in the High-Energy Pop results, because nothing limits one artist.

See the [model card](model_card.md) (sections 6 and 7) for more detail and the full numbers.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



