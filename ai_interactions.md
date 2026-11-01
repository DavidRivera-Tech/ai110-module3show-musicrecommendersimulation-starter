# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude in VS Code to score six extra song attributes (tempo, valence, popularity, decade, mood tags, instrumentalness) without changing any existing result. The job had several steps: change the scoring function, fix a bug in the energy rule, add a seventh test profile, and prove the first six profiles still came out the same.

**Prompts used:**

**S1** (extra attributes and a seventh profile):

> In src/recommender.py, extend score_song so these new song attributes add points ONLY when the user_prefs dict includes the matching key (so existing profiles score exactly the same):
>
> "tempo_bpm": up to +0.5 for closeness (full at 0 BPM difference, 0 at 60+ BPM apart)
> "valence": up to +0.5 for closeness
> "popularity": up to +0.5 for closeness (on a 0-100 scale)
> "decade": +0.5 if release_decade matches (it's stored as an int like 2020)
> "mood_tags": +0.25 per shared tag, max 3 tags
> "instrumental": True/False preference, up to +0.5 using instrumentalness
>
> Each one adds a reason string. Clamp energy closeness at 0 so it can't go negative. Then add a 7th profile to main.py called "Extended: Late-Night Focus" that uses several of these keys, and confirm the first 6 profiles' output is unchanged by comparing against profile_output.txt.

**What did the agent generate or change?**

- `src/recommender.py`: six new rules in `score_song`, each guarded by `if key in user_prefs`, each adding a reason string such as `tempo 80 BPM vs target 78 (+0.48)`. Energy closeness now uses `max(0.0, ...)`.
- `src/main.py`: a seventh profile, "Extended: Late-Night Focus" (lofi, focused, energy 0.4, likes acoustic, tempo 78, valence 0.55, instrumental, mood tags `focused` and `calm`, decade 2020). Focus Flow came out first at 7.30.
- It ran `python -m src.main` and `pytest` to check its own work.

**What did you verify or fix manually?**

- **Profiles 1–6 unchanged.** I had Claude compare the new output against `profile_output.txt`. The first six profiles matched exactly. I repeated the same check after the Strategy refactor and again after adding `--diversity` and `--table`, and the default output still matched each time.
- **The max-score mismatch (7.75 vs 8.25).** Claude told me the new maximum score was 7.75. I added it up myself and got 8.25: 5.0 for the four core rules, 2.5 for the five +0.5 rules, and 0.75 for mood tags. Claude agreed it had made an arithmetic slip. Before writing 8.25 into the docs I had it check again. A made-up "perfect" song with every key set scored exactly 8.25, and the same song with only the four core keys scored 5.0. The README and model card now say 5.0 for the core rules and 8.25 with every optional key.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

The Strategy pattern, combined with a weights table. Each ranking mode (balanced, genre-boost, mood-first, energy-focused) is a small class that holds only a name, a one-line description, and a dict of weights.

**How did AI help you brainstorm or implement it?**

**S2a** (brainstorming the options):

> I want multiple ranking modes (e.g. balanced, genre-heavy, mood-first, energy-focused) that a user can switch in main.py. Looking at recommender.py, what design patterns could keep this modular without copying score_song for each mode? Compare 2–3 options and recommend one.

Claude compared three options. Option A was a weights table passed into `score_song`. Option B was rules as small functions, with a mode as a list of (rule, weight). Option C was one class per mode. It recommended A, because my four modes differ only in how much each rule is worth, and said B would make sense later if the rules grew different shapes.

**My decision.** I didn't pick just one. I chose to combine A and C: use Strategy classes that only hold a weights table. That keeps `score_song` as one function while giving every mode a name and a description that `--list-modes` can print.

**S2b** (building it):

> Build the ranking modes as a Strategy pattern combined with your Option A: a base ScoringStrategy class with a name, a one-line description, and a weights dict (balanced = exactly today's weights). Subclasses override only the weights they change:
>
> "genre-boost": genre 4.0, mood 0.5, energy 1.0
> "mood-first": mood 3.0, genre 1.0
> "energy-focused": energy 4.0, genre 0.5, mood 0.5
>
> Add a STRATEGIES registry dict and get_strategy(name) that raises ValueError for unknown names. score_song and recommend_songs take mode="balanced" by default, and reason strings show the weighted points (e.g. "genre match (+4.00)"). The Recommender class keeps "balanced" so the tests don't change. In main.py, add argparse flags: --mode (choices from STRATEGIES, default balanced) and --list-modes (prints each mode's name and description). Skip normalization. Confirm the default output still matches profile_output.txt for profiles 1–6.

Claude wrote the classes, the registry, and the `--mode` and `--list-modes` flags. Its first attempt never ran because of a shell quoting error, so it moved the edit scripts into files and re-ran them. After that, everything applied cleanly.

**How does the pattern appear in your final code?**

- `ScoringStrategy` in `src/recommender.py` is the base class. Its weights are exactly the original ones, so `balanced` behaves as before.
- `GenreBoostStrategy`, `MoodFirstStrategy`, and `EnergyFocusedStrategy` override only the weights they change.
- `STRATEGIES` is the registry, and `get_strategy(name)` raises `ValueError` for an unknown mode.
- `score_song(..., mode="balanced")` and `recommend_songs(..., mode="balanced")` look up the weights, and the reason strings show the weighted points.
- `src/main.py` has `--mode` and `--list-modes`.
- `tests/test_recommender.py` has a test for each mode's #1 result and one for the unknown-mode error.

**What I verified.**

- **Same output in default mode.** The default output matched `profile_output.txt` for profiles 1–6, as in the first task.
- **"Three #1 songs, not four."** When I asked Claude to save the mode comparison table for the README, I described it as showing four different #1 songs. The table for Classical but High Energy actually shows three: balanced and genre-boost both give Nocturne in Blue Hour, mood-first gives Crossroads Lament, and energy-focused gives Storm Runner. Claude caught it, and the README says three.
