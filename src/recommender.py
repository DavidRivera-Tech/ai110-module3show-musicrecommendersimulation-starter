import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

def _profile_to_prefs(user: UserProfile) -> Dict:
    """Converts a UserProfile into the dict format score_song expects."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the k songs that best match the user, highest score first."""
        user_prefs = _profile_to_prefs(user)
        ranked = sorted(
            self.songs,
            key=lambda song: score_song(user_prefs, asdict(song))[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns the scoring reasons for a song as one semicolon-separated string."""
        _, reasons = score_song(_profile_to_prefs(user), asdict(song))
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts with numeric fields converted."""
    int_fields = ("id", "popularity", "release_decade")
    float_fields = (
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
        "instrumentalness",
        "speechiness",
        "liveness",
    )

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            song = dict(row)
            for field in int_fields:
                song[field] = int(row[field])
            for field in float_fields:
                song[field] = float(row[field])
            song["mood_tags"] = row["mood_tags"].split("|")
            songs.append(song)

    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against user preferences and returns (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    if "genre" in user_prefs and song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append("genre match (+2.00)")

    if "mood" in user_prefs and song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.00)")

    if "energy" in user_prefs:
        target = user_prefs["energy"]
        points = 1.5 * max(0.0, 1 - abs(song["energy"] - target))
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs target {target:.2f} (+{points:.2f})")

    if "likes_acoustic" in user_prefs:
        if user_prefs["likes_acoustic"]:
            points = 0.5 * song["acousticness"]
            reasons.append(f"acousticness {song['acousticness']:.2f}, likes acoustic (+{points:.2f})")
        else:
            points = 0.5 * (1 - song["acousticness"])
            reasons.append(f"acousticness {song['acousticness']:.2f}, prefers non-acoustic (+{points:.2f})")
        score += points

    if "tempo_bpm" in user_prefs:
        target = user_prefs["tempo_bpm"]
        points = 0.5 * max(0.0, 1 - abs(song["tempo_bpm"] - target) / 60)
        score += points
        reasons.append(f"tempo {song['tempo_bpm']:.0f} BPM vs target {target:.0f} (+{points:.2f})")

    if "valence" in user_prefs:
        target = user_prefs["valence"]
        points = 0.5 * max(0.0, 1 - abs(song["valence"] - target))
        score += points
        reasons.append(f"valence {song['valence']:.2f} vs target {target:.2f} (+{points:.2f})")

    if "popularity" in user_prefs:
        target = user_prefs["popularity"]
        points = 0.5 * max(0.0, 1 - abs(song["popularity"] - target) / 100)
        score += points
        reasons.append(f"popularity {song['popularity']} vs target {target:.0f} (+{points:.2f})")

    if "decade" in user_prefs and song["release_decade"] == user_prefs["decade"]:
        score += 0.5
        reasons.append(f"decade match, {song['release_decade']}s (+0.50)")

    if "mood_tags" in user_prefs:
        wanted = user_prefs["mood_tags"]
        if isinstance(wanted, str):
            wanted = wanted.split("|")
        shared = [tag for tag in wanted if tag in song["mood_tags"]][:3]
        points = 0.25 * len(shared)
        score += points
        if shared:
            reasons.append(f"shared mood tags {', '.join(shared)} (+{points:.2f})")

    if "instrumental" in user_prefs:
        if user_prefs["instrumental"]:
            points = 0.5 * song["instrumentalness"]
            reasons.append(f"instrumentalness {song['instrumentalness']:.2f}, wants instrumental (+{points:.2f})")
        else:
            points = 0.5 * (1 - song["instrumentalness"])
            reasons.append(f"instrumentalness {song['instrumentalness']:.2f}, wants vocals (+{points:.2f})")
        score += points

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts highest first, and returns the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
