# Story

You are a time-traveler, known only as the “Chrono Explorer.”
Your mission is to journey across airports scattered around the world to complete legendary **Quests of Time**. Each airport you land at brings new opportunities — treasure, challenges, or danger.

When you arrive at an airport, the board flashes:
**“Welcome to [Airport Name]! You have [Money]$ and [Range] km of travel power left.”**

To survive and progress, you must carefully manage your **money** (to refuel or recover) and your **range** (to travel). At each airport you may encounter:

* A **quest** (like reaching a legendary city or surviving long flights).
* A **reward** (money or points).
* Or a **challenge** (losing resources, facing fuel shortages, or even robbers).

Complete enough quests, and you’ll unlock the ultimate secret: the **Chrono Diamond**, hidden in the depths of time.
But beware — only careful travelers can finish their journey without running out of money or range.

Your story is written in the database as you play — every airport you reach, every quest you complete, and every victory or loss is stored for history.

---

# Database

This game uses the **airport** and **country** tables from the `flight_game` database.

### 1. Create a new database

```sql
CREATE DATABASE chronoquest;
USE chronoquest;
```

### 2. Import airports and countries

Take the data from `flight_game_reordered_full.sql` and keep **airport** and **country** tables.

---

### 3. Create the following tables

```sql
CREATE TABLE Player (
    player_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    join_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Game (
    game_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT NOT NULL,
    start_airport VARCHAR(40) NOT NULL,
    current_airport VARCHAR(40) NOT NULL,
    money FLOAT NOT NULL DEFAULT 1000,
    player_range DECIMAL(8,2) NOT NULL DEFAULT 500,
    score INT NOT NULL DEFAULT 0,
    game_status ENUM('active','won','lost') NOT NULL DEFAULT 'active',
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (start_airport) REFERENCES Airport(ident),
    FOREIGN KEY (current_airport) REFERENCES Airport(ident)
);

CREATE TABLE Goal (
    goal_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    target_text VARCHAR(255) NOT NULL,
    points INT NOT NULL
);

CREATE TABLE Goal_Reached (
    id INT PRIMARY KEY AUTO_INCREMENT,
    game_id INT NOT NULL,
    goal_id INT NOT NULL,
    reached_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (goal_id) REFERENCES Goal(goal_id)
);
```

---

### 4. Insert sample player

```sql
INSERT INTO Player (name, email)
VALUES ('TestPlayer', 'testplayer@example.com');
```

---

### 5. Insert sample goals (quests)

```sql
INSERT INTO Goal (goal_id, name, target_text, points)
VALUES
(7, 'Fly to Helsinki', 'Reach Helsinki Vantaa Airport from your starting location', 100),
(8, 'Fly to Los Angeles', 'Land at Los Angeles International Airport', 200),
(9, 'Visit Germany airports', 'Visit Frankfurt, Munich, and Berlin airports in order', 300),
(10,'Earn 1000 points','Accumulate 1000 points',100),
(11,'Long distance flight','Fly 1000 km in one game',150),
(12,'Fuel challenge','Complete 5 flights without refueling',50);
```

---

### 6. Insert a sample game

```sql
INSERT INTO Game (player_id, start_airport, current_airport, money, player_range, score, game_status)
VALUES (1, '00A', '00A', 1000, 500, 0, 'active');
```

---

### 7. Simulate progress

Mark a quest completed (example: Los Angeles):

```sql
INSERT INTO Goal_Reached (game_id, goal_id)
VALUES (1, 8);

UPDATE Game g
JOIN Goal gr ON gr.goal_id = 8
SET g.score = g.score + gr.points
WHERE g.game_id = 1;
```

---

### 8. Verify setup

```sql
SHOW TABLES;
```

Expected:

```
+----------------+
| Tables_in_chronoquest |
+----------------+
| airport        |
| country        |
| player         |
| game           |
| goal           |
| goal_reached   |
+----------------+
```
