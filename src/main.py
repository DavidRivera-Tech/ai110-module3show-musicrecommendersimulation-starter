"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False,
    },
    "Edge Case: Classical but High Energy": {
        "genre": "classical", "mood": "melancholic", "energy": 0.9, "likes_acoustic": True,
    },
    "Edge Case: Genre Not in Catalog": {
        "genre": "k-pop", "mood": "happy", "energy": 0.75,
    },
    "Edge Case: Capitalized Input": {
        "genre": "Pop", "mood": "Happy", "energy": 0.8,
    },
    "Extended: Late-Night Focus": {
        "genre": "lofi", "mood": "focused", "energy": 0.4, "likes_acoustic": True,
        "tempo_bpm": 78, "valence": 0.55, "instrumental": True,
        "mood_tags": ["focused", "calm"], "decade": 2020,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
        header = f"PROFILE: {name}"
        print()
        print(header)
        print("=" * len(header))
        print(f"Preferences: {profile}")

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']} by {song['artist']}  (score: {score:.2f})")
            for reason in explanation.split("; "):
                print(f"     - {reason}")
        print()


if __name__ == "__main__":
    main()
