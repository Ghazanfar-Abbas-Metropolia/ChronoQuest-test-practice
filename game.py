import mysql.connector
import random

# ==============================
# Database Connection
# ==============================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="ChronoQuest"
    )

# ==============================
# Game Logic
# ==============================
class ChronoQuest:
    def __init__(self, player_name, player_email):
        self.conn = get_connection()
        self.cursor = self.conn.cursor(dictionary=True)

        # Ensure player exists
        self.cursor.execute("SELECT * FROM Player WHERE email = %s", (player_email,))
        player = self.cursor.fetchone()
        if not player:
            self.cursor.execute(
                "INSERT INTO Player (name, email) VALUES (%s, %s)",
                (player_name, player_email)
            )
            self.conn.commit()
            self.player_id = self.cursor.lastrowid
        else:
            self.player_id = player["player_id"]

        # Start new game
        self.start_airport = "KJFK"  # Default start (JFK USA)
        self.cursor.execute("""
            INSERT INTO Game (player_id, start_airport, current_airport, money, player_range, score)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (self.player_id, self.start_airport, self.start_airport, 1000.0, 5000, 0))
        self.conn.commit()
        self.game_id = self.cursor.lastrowid

        print(f"🎮 New game started for {player_name} at {self.start_airport}")

    # --------------------------
    # Get airport by ICAO
    # --------------------------
    def get_airport(self, icao_code):
        self.cursor.execute("SELECT * FROM Airport WHERE icao_code = %s", (icao_code,))
        return self.cursor.fetchone()

    # --------------------------
    # Fly to a new airport
    # --------------------------
    def fly_to_airport(self, icao_code):
        # Current position
        self.cursor.execute("SELECT * FROM Game WHERE game_id = %s", (self.game_id,))
        game = self.cursor.fetchone()
        current_airport = self.get_airport(game["current_airport"])
        target_airport = self.get_airport(icao_code)

        if not target_airport:
            print("❌ Airport not found.")
            return

        # (Simplified) Check distance using flat Euclidean approximation
        dist = ((current_airport["longitude"] - target_airport["longitude"])**2 +
                (current_airport["latitude"] - target_airport["latitude"])**2) ** 0.5

        if dist > game["player_range"]:
            print("✈️ Too far! You can’t reach this airport.")
            return

        # Update position
        self.cursor.execute("""
            UPDATE Game SET current_airport = %s WHERE game_id = %s
        """, (icao_code, self.game_id))
        self.conn.commit()

        print(f"✅ Flew from {current_airport['icao_code']} to {target_airport['icao_code']}")

        # Check if there's a goal at this airport
        self.check_goal(target_airport["airport_id"])

    # --------------------------
    # Check and apply goal rewards
    # --------------------------
    def check_goal(self, airport_id):
        self.cursor.execute("""
            SELECT * FROM Goal
            WHERE airport_id = %s AND game_id = %s
        """, (airport_id, self.game_id))
        goals = self.cursor.fetchall()

        for goal in goals:
            if random.random() < float(goal["probability"]):
                # Reward player
                self.cursor.execute("""
                    UPDATE Game
                    SET money = money + %s, score = score + 100
                    WHERE game_id = %s
                """, (goal["money_value"], self.game_id))
                self.conn.commit()

                # Record achievement
                self.cursor.execute("""
                    INSERT INTO Goal_Reached (game_id, goal_id, airport_id)
                    VALUES (%s, %s, %s)
                """, (self.game_id, goal["goal_id"], airport_id))
                self.conn.commit()

                print(f"🎯 Goal achieved: {goal['name']} (+${goal['money_value']}, +100 score)")

    # --------------------------
    # Show player status
    # --------------------------
    def show_status(self):
        self.cursor.execute("SELECT * FROM Game WHERE game_id = %s", (self.game_id,))
        game = self.cursor.fetchone()
        print(f"📊 Status: Airport={game['current_airport']}, Money=${game['money']}, Score={game['score']}")

# ==============================
# Example Gameplay
# ==============================
if __name__ == "__main__":
    game = ChronoQuest("Alice", "alice@example.com")
    game.show_status()
    game.fly_to_airport("KLAX")   # Fly to Los Angeles
    game.show_status()
    game.fly_to_airport("EDDF")   # Fly to Frankfurt
    game.show_status()
