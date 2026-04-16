import csv
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score a Song dataclass against a UserProfile."""
        score = 0.0
        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 3.0
            reasons.append("genre match (+3.0)")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 2.0
            reasons.append("mood match (+2.0)")

        energy_diff = abs(song.energy - user.target_energy)
        energy_score = round((1 - energy_diff) * 2.0, 2)
        score += energy_score
        reasons.append(f"energy similarity (+{energy_score})")

        if user.likes_acoustic and song.acousticness >= 0.7:
            score += 1.5
            reasons.append("acoustic preference (+1.5)")

        if song.danceability >= 0.7:
            score += 1.0
            reasons.append("high danceability (+1.0)")

        if song.valence >= 0.7:
            score += 0.5
            reasons.append("positive valence (+0.5)")

        return (round(score, 2), reasons)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs sorted by score descending for the given user."""
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        score, reasons = self._score(user, song)
        return f"Score: {score:.2f} — " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries with proper types."""
    songs = []
    # Resolve path relative to project root (one level up from src/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, csv_path)
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences, returning (score, reasons)."""
    score = 0.0
    reasons = []

    # Genre match: +3.0 points for exact match
    if song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += 3.0
        reasons.append("genre match (+3.0)")

    # Mood match: +2.0 points for exact match
    if song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += 2.0
        reasons.append("mood match (+2.0)")

    # Energy similarity: up to +2.0 points based on closeness (1 - |difference|)
    if "energy" in user_prefs:
        energy_diff = abs(song["energy"] - user_prefs["energy"])
        energy_score = round((1 - energy_diff) * 2.0, 2)
        score += energy_score
        reasons.append(f"energy similarity (+{energy_score})")

    # Danceability bonus: +1.0 if danceability >= 0.7
    if song["danceability"] >= 0.7:
        score += 1.0
        reasons.append("high danceability (+1.0)")

    # Valence bonus: +0.5 if valence >= 0.7 (positive/uplifting feel)
    if song["valence"] >= 0.7:
        score += 0.5
        reasons.append("positive valence (+0.5)")

    return (round(score, 2), reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, sort by score descending, and return the top k results."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    # sorted() returns a new list, leaving the original unchanged
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
