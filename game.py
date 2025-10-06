# ============================================
# ChronoQuest - Time Traveling Adventure Game
# ============================================

import random
import mysql.connector
import sys

# -----------------------
# DB CONNECTION
# -----------------------
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    database="ChronoQuest",
    user="your_username",      # replace
    password="your_password",  # replace
    auth_plugin="mysql_native_password",
    autocommit=True
)

def get_cursor(dict_cursor=True):
    return conn.cursor(dictionary=True) if dict_cursor else conn.cursor()

# -----------------------
# UTILS
# -----------------------
def safe_input(prompt: str):
    """Input wrapper that allows quitting at any prompt."""
    user_input = input(prompt).strip()
    if user_input.lower() == "quit":
        print("🛑 Exiting ChronoQuest... Goodbye, traveler!")
        sys.exit(0)
    return user_input

# -----------------------
# PLAYER SETUP
# -----------------------
def create_player():
    name = safe_input("Enter your name (or type quit to exit): ")
    email = f"{name.lower()}@chronoquest.com"

    cur = get_cursor()
    cur.execute("INSERT INTO Player (name, email) VALUES (%s, %s)", (name, email))
    return cur.lastrowid

# -----------------------
# GAME SETUP
# -----------------------
def start_game(player_id):
    cur = get_cursor()
    cur.execute("SELECT icao_code, name, country FROM Airport")
    airports = cur.fetchall()

    print("\nAvailable Starting Airports:")
    for ap in airports:
        print(f"{ap['icao_code']} - {ap['name']} ({ap['country']})")

    start_airport = safe_input("\nChoose your starting airport (ICAO): ").upper()

    # validate
    cur.execute("SELECT * FROM Airport WHERE icao_code = %s", (start_airport,))
    if not cur.fetchone():
        print("❌ Invalid airport. Starting aborted.")
        sys.exit(0)

    cur.execute(
        """INSERT INTO Game (player_id, start_airport, current_airport, money, player_range, score, game_status)
           VALUES (%s, %s, %s, 1000.00, 5000, 0, 'active')""",
        (player_id, start_airport, start_airport)
    )
    return cur.lastrowid

# -----------------------
# GAME FUNCTIONS
# -----------------------
def show_status(game_id):
    cur = get_cursor()
    cur.execute("SELECT * FROM Game WHERE game_id = %s", (game_id,))
    g = cur.fetchone()
    print(f"\n📊 Status:")
    print(f"Current Airport: {g['current_airport']}")
    print(f"Money: ${g['money']}")
    print(f"Range: {g['player_range']} km")
    print(f"Score: {g['score']}")
    print(f"Game Status: {g['game_status']}")

def fly_to_airport(game_id, destination):
    cur = get_cursor()

    # find game
    cur.execute("SELECT * FROM Game WHERE game_id = %s", (game_id,))
    game = cur.fetchone()

    # find destination
    cur.execute("SELECT * FROM Airport WHERE icao_code = %s", (destination,))
    dest = cur.fetchone()
    if not dest:
        print("❌ Airport not found.")
        return

    # simulate travel
    year = random.randint(1400, 2500)
    print(f"\n✈️ Flying to {dest['icao_code']} ({dest['name']}, {dest['country']}) in the year {year}...")

    # basic fuel/money deductions
    money_cost = random.randint(100, 400)
    range_cost = random.randint(500, 1500)

    new_money = game['money'] - money_cost
    new_range = game['player_range'] - range_cost

    if new_money < 0 or new_range < 0:
        print("💀 You ran out of money or fuel! Game over.")
        cur.execute("UPDATE Game SET game_status='lost' WHERE game_id=%s", (game_id,))
        sys.exit(0)

    # possible time-travel events
    bonus = 0
    if year < 1900 and random.random() < 0.25:
        print("⚔️ Turbulent past! Bandits stole half your money!")
        new_money //= 2
    elif 1900 <= year <= 1950 and random.random() < 0.20:
        print("🔥 Engine trouble in early aviation! You lose extra range.")
        new_range -= 1000
    elif year > 2025 and random.random() < 0.20:
        print("🚀 Future technology boosts your range!")
        new_range += 2000
        bonus += 100

    # rare chrono diamond
    if year in (2000, 2222) and random.random() < 0.01:
        print("💎 You discovered the legendary Chrono Diamond!")
        bonus += 1000
        new_money += 5000

    # update game state
    cur.execute("""UPDATE Game 
                   SET current_airport=%s, money=%s, player_range=%s, score=score+%s 
                   WHERE game_id=%s""",
                (dest['icao_code'], new_money, new_range, bonus, game_id))

    print(f"Arrived at {dest['icao_code']} with ${new_money}, {new_range} km range, +{bonus} score.")

# -----------------------
# MAIN LOOP
# -----------------------
def main():
    print("🌍 Welcome to ChronoQuest! Type 'quit' at any time to exit.")
    player_id = create_player()
    game_id = start_game(player_id)

    while True:
        print("\n--- ChronoQuest Menu ---")
        print("1. Fly to a new airport")
        print("2. Check status")
        print("3. Quit")

        choice = safe_input("Choose an option: ")

        if choice == "1":
            icao = safe_input("Enter ICAO code of destination: ").upper()
            fly_to_airport(game_id, icao)
        elif choice == "2":
            show_status(game_id)
        elif choice == "3":
            print("🛑 Exiting ChronoQuest. See you next time!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
