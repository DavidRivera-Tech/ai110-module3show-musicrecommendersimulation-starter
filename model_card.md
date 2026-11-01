# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Think of the recommender as a judge who gives every song in the catalog a score out of 5 for how well it fits one listener, then hands back the highest-scoring songs.

**What it knows about each song.** The catalog describes every song with a genre (such as pop or lofi), a mood (such as happy or chill), an energy level from calm to intense, and how acoustic it sounds, meaning how much it relies on real instruments instead of electronic sound. Catalog entries also carry other details like tempo and popularity, but the judge does not use those yet.

**What it knows about the listener.** The listener tells the system four things: a favorite genre, a favorite mood, how energetic they want their music to be, and whether they like acoustic sound. If the listener leaves one of these out, that part is simply skipped.

**How the points add up.** Each song starts at zero and earns points like this:

- **Genre:** +2 points if the song's genre is exactly the listener's favorite. This is the biggest reward, because genre is the best sign of long-term taste.
- **Mood:** +1 point if the song's mood is exactly the listener's favorite mood.
- **Energy:** up to 1.5 points, based on how *close* the song's energy is to what the listener wants. A perfect match earns the full 1.5, and the further away the song is, the fewer points it gets. A very energetic song is not rewarded just for being energetic, and a calm song is not rewarded just for being calm. Only closeness to the listener's target counts.
- **Acoustic sound:** up to 0.5 points. Listeners who like acoustic music give more points to songs that sound acoustic, and listeners who don't give more points to songs that sound electronic.

The most a song can earn is 5 points. Along with each score, the system writes a short list of reasons, such as "genre match" or "energy close to target", so you can see why a song ranked where it did.

**How songs are ranked.** The judge scores every song in the catalog, lines them up from highest score to lowest, and returns the top few, five by default.

**What changed from the starter logic.** The starter version could not actually recommend anything. It could not read the song catalog, it did not score songs, and its "recommendations" were just the first few songs in the file, in the same order for everyone, with a placeholder where the explanation should be. This version reads the catalog (now expanded from 10 to 22 songs), scores each song against the listener's preferences using the point rules above, ranks the songs by score, and explains each result in plain words.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

**Main weakness: genre dominance on a thin catalog.** A genre match is worth +2.00, which is more than the most energy closeness can ever add (1.50). On top of that, 14 of the 17 genres in the 22-song catalog have exactly one song. So for most listeners the genre bonus goes to a single song, and after that song every other slot is decided by energy alone.

The "Edge Case: Classical but High Energy" profile (energy 0.9) shows both problems. Its #1 result is Nocturne in Blue Hour (score 2.86), a song with energy 0.15. It earned +2.00 for genre, only +0.38 for energy, and +0.48 for acousticness. The songs that actually fit the requested energy came after it: Storm Runner (energy 0.91, +1.48 for energy) scored 1.53, and Gym Hero scored 1.48. No energy mismatch can overcome the genre bonus, so the system recommended the opposite of what the listener asked for. "Deep Intense Rock" shows the thin-catalog side: Storm Runner is the only rock song and scores 4.93, but slots 2 to 5 score 2.96, 1.95, 1.91 and 1.83, so the rest of the list is just "whatever is near energy 0.92". The result is a filter bubble in miniature: the system rewards whatever label the listener typed in and does little to find music that sounds like what they want.

**Case-sensitive exact string matching.** Genre and mood are compared as exact strings, so "Pop" does not equal "pop". In the "Capitalized Input" profile (genre=Pop, mood=Happy, energy=0.8), Sunrise City fell from 4.88 to 1.47 because it lost both the +2.00 genre and +1.00 mood bonuses. The list became a pure energy ranking: Sunrise City (1.47) is tied with Concrete Crown, a hip-hop song (1.47), and Rooftop Lights is next at 1.44. The same thing happens when a genre simply is not in the catalog: for "k-pop" the top score is only 2.48. Nothing warns the user that their input matched nothing. Related to this, "indie pop" gets no credit for "pop" even though a pop fan would likely enjoy it.

**Missing and sparse moods.** The catalog has no "sad" mood, so a listener who types "sad" gets no mood points from any song. The closest options are "melancholic" and "wistful", and each appears on only one song. In total, 9 of the 15 moods appear on just one song. Mood matching is also all-or-nothing: for "Chill Lofi", Focus Flow (mood "focused") scores 3.81 against 4.75 for Midnight Coding (mood "chill") and loses the full +1.00 even though the two songs are nearly identical in sound.

**No input validation.** The energy rule assumes a target between 0 and 1, but nothing checks it. When I tried a target of 2.0, all 22 songs received negative energy points, and the lowest total score was -1.28 (Nocturne in Blue Hour). The results still sorted and printed as if nothing was wrong, with Sunrise City on top at 2.73. A typo like 8 instead of 0.8 would quietly produce nonsense rankings.

**Artist repetition.** Nothing stops one artist from filling the list. In "High-Energy Pop", Neon Echo holds #1 (Sunrise City, 4.88) and #3 (Afterglow Avenue, 3.72). In the "Genre Not in Catalog" profile, three of the five results are Neon Echo songs: Sunrise City, Night Drive Loop and Afterglow Avenue. A real listener would see the same artist repeated rather than a varied list.

**Who this unintentionally favors.** The system works best for listeners whose favorite genre has several songs, like pop (3), lofi (3) or jazz (2), and whose typing matches the catalog exactly. "Chill Lofi" gets a coherent list because three lofi songs share the genre bonus. Listeners of genres with one song, listeners who use different spellings or moods, and listeners whose tastes cross genres get weaker, less varied results.

**Features it does not consider.** Tempo, valence, danceability, instrumentalness, speechiness, liveness, popularity, release decade and mood tags are in the data but not used in the score, so two songs that feel very different can score the same.

*Numbers come from `profile_output.txt`, except the energy 2.0 test, which I ran separately.*

---

## 7. Evaluation  

I checked the recommender by running six listener profiles through the full 22-song catalog and reading the top 5 and the reasons behind each score. Three profiles are ordinary listeners and three are edge cases built to break the logic.

### Profiles tested and what I looked for

| # | Profile | What I looked for |
|---|---|---|
| 1 | High-Energy Pop (pop, happy, 0.8, not acoustic) | A baseline where every rule can fire. Does the song matching genre, mood and energy rank first? |
| 2 | Chill Lofi (lofi, chill, 0.35, likes acoustic) | The opposite end of the taste range. Does a calm, acoustic listener get a completely different list from the pop listener? |
| 3 | Deep Intense Rock (rock, intense, 0.92, not acoustic) | A genre with only one song. What fills the list after that song? |
| 4 | Edge Case: Classical but High Energy (classical, melancholic, 0.9, likes acoustic) | Conflicting preferences. Which wins, the genre or the requested energy? |
| 5 | Edge Case: Genre Not in Catalog (k-pop, happy, 0.75) | What happens when no song can earn genre points? |
| 6 | Edge Case: Capitalized Input (Pop, Happy, 0.8) | Does a capitalization difference change the results? |

### Full output for each profile

**1. High-Energy Pop**

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

**2. Chill Lofi**

```
PROFILE: Chill Lofi
===================
Preferences: genre=lofi, mood=chill, energy=0.35, likes_acoustic=True

1. Library Rain by Paper Lanterns  (score: 4.93)
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.35 vs target 0.35 (+1.50)
     - acousticness 0.86, likes acoustic (+0.43)

2. Midnight Coding by LoRoom  (score: 4.75)
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.42 vs target 0.35 (+1.40)
     - acousticness 0.71, likes acoustic (+0.35)

3. Focus Flow by LoRoom  (score: 3.81)
     - genre match (+2.00)
     - energy 0.40 vs target 0.35 (+1.42)
     - acousticness 0.78, likes acoustic (+0.39)

4. Spacewalk Thoughts by Orbit Bloom  (score: 2.85)
     - mood match (+1.00)
     - energy 0.28 vs target 0.35 (+1.40)
     - acousticness 0.92, likes acoustic (+0.46)

5. Willow Road by Maple & Pine  (score: 1.93)
     - energy 0.33 vs target 0.35 (+1.47)
     - acousticness 0.91, likes acoustic (+0.46)
```

**3. Deep Intense Rock**

```
PROFILE: Deep Intense Rock
==========================
Preferences: genre=rock, mood=intense, energy=0.92, likes_acoustic=False

1. Storm Runner by Voltline  (score: 4.93)
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.91 vs target 0.92 (+1.48)
     - acousticness 0.10, prefers non-acoustic (+0.45)

2. Gym Hero by Max Pulse  (score: 2.96)
     - mood match (+1.00)
     - energy 0.93 vs target 0.92 (+1.48)
     - acousticness 0.05, prefers non-acoustic (+0.47)

3. Pulse Theory by Atlas Drift  (score: 1.95)
     - energy 0.94 vs target 0.92 (+1.47)
     - acousticness 0.04, prefers non-acoustic (+0.48)

4. Iron Cathedral by Black Meridian  (score: 1.91)
     - energy 0.97 vs target 0.92 (+1.43)
     - acousticness 0.03, prefers non-acoustic (+0.48)

5. Fuego en la Calle by Los Soleros  (score: 1.83)
     - energy 0.86 vs target 0.92 (+1.41)
     - acousticness 0.15, prefers non-acoustic (+0.42)
```

**4. Edge Case: Classical but High Energy**

```
PROFILE: Edge Case: Classical but High Energy
=============================================
Preferences: genre=classical, mood=melancholic, energy=0.9, likes_acoustic=True

1. Nocturne in Blue Hour by Elena Vasquez  (score: 2.86)
     - genre match (+2.00)
     - energy 0.15 vs target 0.90 (+0.38)
     - acousticness 0.97, likes acoustic (+0.48)

2. Crossroads Lament by Delta Jack  (score: 2.17)
     - mood match (+1.00)
     - energy 0.46 vs target 0.90 (+0.84)
     - acousticness 0.66, likes acoustic (+0.33)

3. Storm Runner by Voltline  (score: 1.53)
     - energy 0.91 vs target 0.90 (+1.48)
     - acousticness 0.10, likes acoustic (+0.05)

4. Fuego en la Calle by Los Soleros  (score: 1.51)
     - energy 0.86 vs target 0.90 (+1.44)
     - acousticness 0.15, likes acoustic (+0.07)

5. Gym Hero by Max Pulse  (score: 1.48)
     - energy 0.93 vs target 0.90 (+1.46)
     - acousticness 0.05, likes acoustic (+0.03)
```

**5. Edge Case: Genre Not in Catalog**

```
PROFILE: Edge Case: Genre Not in Catalog
========================================
Preferences: genre=k-pop, mood=happy, energy=0.75

1. Rooftop Lights by Indigo Parade  (score: 2.48)
     - mood match (+1.00)
     - energy 0.76 vs target 0.75 (+1.48)

2. Sunrise City by Neon Echo  (score: 2.40)
     - mood match (+1.00)
     - energy 0.82 vs target 0.75 (+1.40)

3. Night Drive Loop by Neon Echo  (score: 1.50)
     - energy 0.75 vs target 0.75 (+1.50)

4. Concrete Crown by Kid Meridian  (score: 1.46)
     - energy 0.78 vs target 0.75 (+1.46)

5. Afterglow Avenue by Neon Echo  (score: 1.40)
     - energy 0.68 vs target 0.75 (+1.40)
```

**6. Edge Case: Capitalized Input**

```
PROFILE: Edge Case: Capitalized Input
=====================================
Preferences: genre=Pop, mood=Happy, energy=0.8

1. Sunrise City by Neon Echo  (score: 1.47)
     - energy 0.82 vs target 0.80 (+1.47)

2. Concrete Crown by Kid Meridian  (score: 1.47)
     - energy 0.78 vs target 0.80 (+1.47)

3. Rooftop Lights by Indigo Parade  (score: 1.44)
     - energy 0.76 vs target 0.80 (+1.44)

4. Night Drive Loop by Neon Echo  (score: 1.42)
     - energy 0.75 vs target 0.80 (+1.42)

5. Fuego en la Calle by Los Soleros  (score: 1.41)
     - energy 0.86 vs target 0.80 (+1.41)
```

### Why four specific songs ranked where they did

- **Sunrise City, #1 for High-Energy Pop (4.88).** It is the only song that earns both the genre and mood bonuses: +2.00 for pop, +1.00 for happy, +1.47 because its energy (0.82) is only 0.02 from the 0.8 target, and +0.41 for being mostly non-acoustic (0.18). 2.00 + 1.00 + 1.47 + 0.41 = 4.88.
- **Storm Runner, #1 for Deep Intense Rock (4.93).** It is the only rock song and also the only song that is both rock and intense: +2.00 genre, +1.00 mood, +1.48 for energy (0.91 against 0.92), and +0.45 for low acousticness (0.10). 2.00 + 1.00 + 1.48 + 0.45 = 4.93.
- **Gym Hero, #2 for Deep Intense Rock (2.96).** It is not rock, so it gets no genre points. It gets +1.00 because it is the only other "intense" song, +1.48 for energy (0.93 against 0.92), and +0.47 for low acousticness (0.05). The listed pieces add to 2.95; the exact total is 2.96 because each piece is rounded for display. It trails Storm Runner by 1.97, which is almost entirely the missing +2.00 genre bonus. It beats the next song, Pulse Theory (1.95), by about one point, the value of the mood match.
- **Nocturne in Blue Hour, #1 for Classical but High Energy (2.86).** It is the only classical song, so it earns +2.00 for genre. Its energy is 0.15 against a 0.9 target, so it gets only +0.38, and it gets +0.48 for being very acoustic (0.97) for a listener who likes acoustic music. 2.00 + 0.38 + 0.48 = 2.86. Songs that actually fit the requested energy scored lower (Storm Runner 1.53) because they had no genre or mood match to add to their energy points.

### Comparing profiles side by side

- **Pop vs. Lofi: no overlap.** The two top-5 lists share no songs. This makes sense: pop wants energy 0.8 and non-acoustic sound, lofi wants energy 0.35 and acoustic sound, and the genre bonus goes to different songs. It's the clearest sign the system is responding to the listener.
- **Pop vs. Rock: one song in common (Gym Hero).** Both listeners want high-energy, non-acoustic music (0.8 against 0.92), so the leftover high-energy songs overlap, but the genre-matched songs (Sunrise City and Afterglow Avenue for pop, Storm Runner for rock) differ. Gym Hero is #2 on both lists because it matches pop's genre and rock's mood.
- **Lofi vs. Rock: no overlap.** Calm and acoustic against intense and electronic: every song on one list is the wrong fit for the other, as it should be.
- **Rock vs. Classical: three songs in common (Storm Runner, Fuego en la Calle, Gym Hero).** The classical listener asked for energy 0.9, close to rock's 0.92, so slots 3 to 5 are the same high-energy songs. The only results tied to the listener's genre or mood are Nocturne in Blue Hour (#1, genre) and Crossroads Lament (#2, mood). It makes sense mathematically, but it means the classical listener mostly got rock-style songs.
- **Pop vs. Capitalized Input: same listener, much worse results.** Writing "Pop" and "Happy" instead of "pop" and "happy" dropped Sunrise City from 4.88 to 1.47 and removed Gym Hero and Afterglow Avenue from the top 5. The capitalized list is now only an energy ranking, led by a tie between Sunrise City and Concrete Crown (hip-hop) at 1.47. The system treats "Pop" and "pop" as different words, so the change is explainable, though not desirable.
- **Pop vs. k-pop: similar songs, different order.** Four of the five songs repeat (Sunrise City, Afterglow Avenue, Rooftop Lights, Concrete Crown). Without any genre bonus, Rooftop Lights jumps to #1 (2.48) because it matches the mood and its energy (0.76) is almost exactly on the 0.75 target, and Gym Hero drops out because its energy (0.93) is now further from the target. This comparison is not perfectly clean, because the k-pop profile also lowers the target energy to 0.75 and leaves out the acoustic preference.

### Why Gym Hero shows up in three lists

Gym Hero appears in the High-Energy Pop list (#2), the Deep Intense Rock list (#2) and the Classical but High Energy list (#5). That looks odd for a song that is only one genre, but the explanation is simple. Think of the scoring as handing out bonuses: the genre bonus and the mood bonus each go only to a few songs, but **energy is the only rule that gives points to every song in the catalog**. After the few genre and mood winners are placed, the rest of the list is decided by which songs are closest to the listener's energy, and Gym Hero has very high energy (0.93) and almost no acoustic sound. For the rock listener (+1.48) and the classical listener (+1.46) its energy is nearly perfect, so it climbs the list even though it matches neither genre. For the pop listener it earns a good but smaller energy score (+1.30), since the target is 0.8, and it stays high there because it is also a pop song.

### What surprised me

What got me was the classical profile. I asked for energy 0.9 and the #1 song was Nocturne in Blue Hour, which has energy 0.15. It won only because it's the one classical song, and a genre match is worth +2.00. I figured the energy score would at least stop a song that far off from winning, and it didn't. The "Pop" vs "pop" test bugged me too: one capital letter took Sunrise City from 4.88 to 1.47, and nothing warned me. Gym Hero showing up in three lists was the one I couldn't explain until I saw that energy is the only rule that gives every song points.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
