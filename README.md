
# Atmosphere Mood Studio

A real-time, emotion-adaptive PyQt6 desktop workspace using hybrid NLP (NLTK VADER + Lexical Rules) and custom vector animations.

---

## Key Features

* **Hybrid NLP Emotion Engine:** Combines NLTK VADER sentiment polarity analysis with regular expression lexical overrides to accurately distinguish complex emotion states (Joy, Calm, Sadness, Anger, Focus).
* **Dynamic Vector Animations:** Custom `QPainter` facial rendering (`EmotionFaceWidget`) featuring real-time feature morphing (eyebrows, eyes, mouth curves) driven by 450ms cubic easing curves.
* **Adaptive Glassmorphism Theme System:** Live stylesheet injection updating window linear gradients, card surface colors, focus highlights, and dynamic contextual guidance messages.
* **Direct Emoji & Pill Overrides:** Dedicated override handling for explicit emojis (`😊`, `🌿`, `😭`, `🤬`, `🚀`) and quick-select mood pills.
* **Sentiment Intensity Meter:** Visual progress bar tracking polarity score values in real time.

---

## Architecture Overview


┌────────────────────────────────────────────────────────┐
│                       USER INPUT                       │
│        Typed Text  •  Direct Emojis  •  Mood Pills      │
└───────────────────────────┬────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────┐
│                HYBRID EMOTION ENGINE                   │
│   • Direct Emoji Overrides                             │
│   • NLTK VADER Polarity Scoring (-1.0 to +1.0)         │
│   • Lexical Indicators (Sad vs. Angry vs. Focus)       │
└───────────────────────────┬────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────┐
│             THEME & ANIMATION CONTROLLER               │
│   • QPainter Vector Morphing (450ms Easing Curves)     │
│   • Dynamic Palette & Style Sheet Generator            │
└───────────────────────────┬────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────┐
│                    ADAPTIVE UI OUTPUT                  │
│   Vector Face  •  Background Gradient  •  Message Bar  │
└───────────────────────────┴────────────────────────────┘


---

## Tech Stack

* **Language:** Python 3.x
* **GUI Framework:** PyQt6
* **NLP & Analytics:** NLTK (VADER Sentiment) & Regular Expressions (`re`)
* **Vector Graphics:** Custom `QPainter` & `QPainterPath` primitives

---

## Prerequisites & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/atmosphere-mood-studio.git](https://github.com/YOUR_USERNAME/atmosphere-mood-studio.git)
   cd atmosphere-mood-studio



2. **Install dependencies:**
Option A: Install via requirements file (Recommended)
```bash
pip install -r requirements.txt

```


Option B: Install packages individually
```bash
pip install pyqt6 nltk

```


3. **Download NLTK VADER Lexicon:**
Run the following snippet in Python:
```python
import nltk
nltk.download('vader_lexicon')

```



---

## Running the Application

Execute the main script to start the desktop workspace:

```bash
python app.py

```

---

