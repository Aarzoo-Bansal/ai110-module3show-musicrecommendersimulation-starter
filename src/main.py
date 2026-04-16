"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  Music Recommender — Top 5 for You")
    print(f"  Profile: {user_prefs['genre']} / {user_prefs['mood']} / energy={user_prefs['energy']}")
    print("=" * 50)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"\n  #{i}  {song['title']} by {song['artist']}")
        print(f"      Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"      Score: {score:.2f}")
        print(f"      Reasons: {explanation}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
