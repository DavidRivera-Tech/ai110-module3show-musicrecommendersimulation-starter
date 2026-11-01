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

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
