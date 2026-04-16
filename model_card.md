# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This recommender suggests 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is a classroom simulation designed for exploring how content-based recommendation systems work. It is not intended for real production use or real users.

---

## 3. How the Model Works

The system takes a user's taste profile (favorite genre, preferred mood, and target energy level) and compares it against every song in the catalog. Each song gets a numeric score based on how well it matches the user:

- If the song's genre matches the user's favorite, it gets the biggest point boost (genre is treated as the strongest signal).
- If the mood matches, it gets additional points.
- The closer the song's energy level is to what the user wants, the more points it earns — this is a sliding scale, not all-or-nothing.
- Songs that are highly danceable or have a positive/uplifting feel get small bonus points.

After scoring every song, the system sorts them from highest to lowest score and shows the top 5 along with a plain-language explanation of why each song scored the way it did.

---

## 4. Data

The catalog (`data/songs.csv`) contains **18 songs** across 12 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, electronic, classical, country, metal, reggae, hip-hop, and folk. Moods include happy, chill, intense, relaxed, moody, and focused.

Most genres have only 1 song in the catalog. Pop and lofi have 2 each, which gives them slightly more representation. The dataset was curated by hand for classroom purposes and does not reflect the distribution of real-world music catalogs. Genres like Latin, Afrobeat, and K-pop are entirely absent.

---

## 5. Strengths

- **Transparent scoring:** Every recommendation comes with a list of reasons, so users can see exactly why a song was chosen. There is no "black box."
- **Works well for clear-cut profiles:** When a user's preferences align with a single genre and mood (e.g., "chill lofi" or "intense rock"), the top results feel intuitively correct.
- **Energy sensitivity:** The continuous energy score rewards close matches rather than treating energy as a binary (high/low), which produces more nuanced rankings.
- **Edge cases degrade gracefully:** When a user asks for a genre not in the catalog (e.g., "k-pop"), the system still returns reasonable results by falling back on mood and energy matches instead of returning nothing.

---

## 6. Limitations and Bias

The system over-prioritizes genre because genre match is worth 3.0 points out of a maximum of 8.5 — roughly 35% of the total score from a single binary check. This means a pop song with a completely wrong mood and energy will often outscore a non-pop song that perfectly matches the user's mood and energy. In the "Conflicting: High Energy + Relaxed Mood" experiment, the only R&B song (Late Night Bars) ranked #1 despite having energy=0.55 while the user wanted energy=0.95, purely because of the 3.0-point genre bonus.

The danceability and valence bonuses are awarded based on fixed thresholds (>=0.7), not user preference. This means the system has a built-in bias toward upbeat, danceable songs. A user who prefers slow, melancholic music will still see danceable songs get bonus points they should not receive.

The catalog has only 18 songs and most genres have just 1 representative. This makes it impossible to differentiate within a genre — if you like rock, you always get Storm Runner, regardless of whether you want classic rock, punk, or grunge. The system cannot capture the diversity that exists within any single genre.

The system also treats all users as having exactly one favorite genre and one favorite mood. Real listeners have complex, multi-dimensional taste that changes by context (studying vs. working out vs. relaxing).

---

## 7. Evaluation

### Profiles Tested

Six user profiles were tested, including three standard profiles and three adversarial/edge-case profiles:

| Profile | Genre | Mood | Energy | Purpose |
|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.8 | Baseline "golden path" |
| Chill Lofi | lofi | chill | 0.4 | Low-energy, relaxed user |
| Deep Intense Rock | rock | intense | 0.95 | High-energy, aggressive user |
| Conflicting Prefs | r&b | relaxed | 0.95 | High energy contradicts relaxed mood |
| Genre Not In Catalog | k-pop | happy | 0.7 | Tests graceful degradation |
| Zero Energy Listener | classical | relaxed | 0.0 | Extreme low-energy edge case |

### What Surprised Me

- **"Gym Hero" appears in 4 out of 6 top-5 lists.** It ranks highly for almost every profile because it has high energy (0.93), high danceability (0.88), and high valence (0.77). The danceability and valence bonuses give it a persistent advantage regardless of the user's actual taste. This is a form of popularity bias — certain songs with "universally high" audio features dominate recommendations.
- **The "Conflicting Prefs" profile exposed a real tension.** The user wanted R&B + relaxed mood + high energy, but there are no relaxed high-energy R&B songs in the catalog. The system handled this by splitting the difference — the genre match pulled Late Night Bars to #1 even though its energy was far from the target. This shows how the system prioritizes genre over energy when they conflict.
- **The "k-pop" profile still got good results.** Even with zero genre matches possible, the system fell back on mood and energy, returning happy songs with matching energy. This is a strength of having multiple scoring dimensions rather than relying on genre alone.

### Weight Experiment

I ran an experiment where genre weight was halved (3.0 to 1.5) and energy weight was doubled (2.0 to 4.0). Key finding: for the "Deep Intense Rock" profile, Storm Runner (rock) dropped from #1 to #2, and Gym Hero (pop) jumped to #1 because its energy (0.93) was closer to the target (0.95) than Storm Runner's (0.91). This showed that the system is sensitive to weight choices — doubling energy made the system genre-blind in cases where energy differences were small, which may not match user expectations. The original weights were restored as they better reflected the intuition that genre identity matters more than small energy differences.

---

## 8. Future Work

- **Multi-genre and multi-mood profiles:** Allow users to specify multiple genres and moods with different weights, reflecting how real taste works.
- **Diversity penalty:** Add a penalty for recommending multiple songs by the same artist or in the same genre, so the top 5 is not a genre echo chamber.
- **User-adjustable weights:** Let the user set how much they care about genre vs. mood vs. energy, rather than hardcoding the weights.
- **Larger catalog:** 18 songs is too small to evaluate a recommender meaningfully. A catalog of 200+ songs would allow testing whether the algorithm scales.
- **Contextual profiles:** Support multiple profiles per user (e.g., "gym playlist" vs. "study playlist") to handle the fact that taste changes by situation.

---

## 9. Personal Reflection

Building this system showed me that recommendation is fundamentally a design problem, not just a math problem. The weights I chose (genre=3.0, mood=2.0, energy=2.0) encode my assumptions about what matters most to a listener — and those assumptions directly shape who gets good recommendations and who does not. When I doubled the energy weight, a pop song beat a rock song for a rock fan, which felt wrong even though the math was valid.

I was surprised by how much a tiny catalog limits the system. With only 1 song per genre in most cases, the recommender cannot distinguish between different types of rock fans or different types of jazz listeners. It reinforced why real platforms like Spotify need millions of tracks — not just for variety, but because the algorithm needs enough candidates to find genuinely good matches.

The most important takeaway is that "transparent" does not mean "fair." My system shows exactly why each song was recommended, but the fixed danceability and valence bonuses quietly favor upbeat music for everyone, including users who did not ask for it. Transparency in scoring does not automatically prevent bias — it just makes the bias visible, which is a necessary first step.
