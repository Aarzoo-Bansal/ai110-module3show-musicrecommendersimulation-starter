"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 55)
    print(f"  [{profile_name}]")
    print(f"  Prefs: genre={user_prefs.get('genre','any')} | mood={user_prefs.get('mood','any')} | energy={user_prefs.get('energy','N/A')}")
    print("=" * 55)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n  #{i}  {song['title']} by {song['artist']}")
        print(f"      Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"      Score: {score:.2f}")
        print(f"      Reasons: {explanation}")

    print("\n" + "-" * 55)


def main() -> None:
    songs = load_songs("data/songs.csv")

    # --- Standard profiles ---
    profiles = {
        "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
        "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.95},

        # --- Adversarial / edge-case profiles ---
        "Conflicting: High Energy + Sad Mood": {"genre": "r&b", "mood": "relaxed", "energy": 0.95},
        "Genre Not In Catalog": {"genre": "k-pop", "mood": "happy", "energy": 0.7},
        "Zero Energy Listener": {"genre": "classical", "mood": "relaxed", "energy": 0.0},
    }

    for name, prefs in profiles.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
