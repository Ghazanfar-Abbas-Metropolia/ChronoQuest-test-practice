# ChronoQuest

## Story

You are a daring **time-traveling adventurer**, seeking the legendary **Chrono Diamond**, a jewel said to shine brighter than the stars themselves.

Your journey begins at your **starting airport**, where the display board greets you:

> “Welcome to KJFK! You have **$1000** and **5000 km of range** left.”

With money and fuel in hand, you take your first flight. Some airports hide **lootboxes**—offering extra money, score, or range. Others conceal **bandits**, ready to rob you of your treasures.

Your quest takes you across **USA, Finland, Sweden, Japan, Germany, and Norway**. Each airport may hold a **goal**—complete it for rewards and points.
Some goals are easy, others are rare. If luck is on your side, you may stumble upon the **Chrono Diamond** itself.

But beware: to truly win, you must **return to your starting airport**, diamond in hand, with your money and victories intact.

Can you outsmart fate, survive the journey, and etch your name into history?

---

## Database

This game uses a **MariaDB/MySQL database** called `ChronoQuest`.
Follow these steps to set it up:

1. **Create the database:**

   ```sql
   CREATE DATABASE ChronoQuest;
   USE ChronoQuest;
   ```

2. **Run the provided schema (chronoquest.sql):**

   ```bash
   mysql -u root -p ChronoQuest < chronoquest.sql
   ```

   This will create the following tables:

   * `Player` → stores player profiles
   * `Game` → active game sessions
   * `Airport` → airports with ICAO codes, coordinates, and countries
   * `Goal` → missions/goals tied to airports
   * `Goal_Reached` → logs of completed goals

3. **Verify the tables:**

   ```sql
   SHOW TABLES;
   ```

   You should see:

   ```
   +----------------+
   | Tables_in_ChronoQuest |
   +----------------+
   | Airport        |
   | Game           |
   | Goal           |
   | Goal_Reached   |
   | Player         |
   +----------------+
   ```

---

## Example Goals & Airports

* **USA** → JFK (KJFK), LAX (KLAX)
* **Finland** → Helsinki (EFHK)
* **Sweden** → Arlanda (ESSA)
* **Japan** → Tokyo Haneda (RJTT), Narita (RJAA)
* **Germany** → Frankfurt (EDDF), Munich (EDDM)
* **Norway** → Oslo (ENGM), Bergen (ENBR)

Example goals include:

* ✈️ *Transatlantic Flight – USA* (+$500, 30% chance)
* 🏔️ *Nordic Explorer – Finland* (+$400, 25% chance)
* 🎌 *Samurai Journey – Japan* (+$600, 15% chance)
* 💎 *Chrono Diamond – The Ultimate Goal* (rare)

---

## Game Setup

1. Install dependencies:

   ```bash
   pip install mysql-connector-python
   ```

2. Run the game:

   ```bash
   python game.py
   ```

3. Sample playthrough:

   ```
   🎮 New game started for Alice at KJFK
   📊 Status: Airport=KJFK, Money=$1000.00, Score=0
   ✅ Flew from KJFK to KLAX
   🎯 Goal achieved: Pacific Hop - USA (+$450.00, +100 score)
   📊 Status: Airport=KLAX, Money=$1450.00, Score=100
   ```

---

## Next Steps

* Add **time travel mechanics** (jump between years with random risks).
* Introduce **fuel purchase system**.
* Expand airport list with more countries.
* Add **win/loss conditions** (score threshold, money bankruptcy).
