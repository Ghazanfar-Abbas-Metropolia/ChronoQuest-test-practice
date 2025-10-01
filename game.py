# ChronoQuest - runnable game
# Checklist before starting
# - Make sure mysql-connector-python is installed (pip install mysql-connector-python)
# - Make sure MariaDB is running
# - Database must be named ChronoQuest
# - Tables: Player, Game, Goal, Goal_Reached, Airport, Country

import random
import mysql.connector

# -----------------------
# DB CONNECTION
# -----------------------
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    database="ChronoQuest",
    user="your_username",      # Replace with your DB username
    password="your_password",  # Replace with your DB password
    auth_plugin="mysql_native_password",
    autocommit=True
)

# -----------------------
# HELPERS / DB UTILS
# -----------------------

def get_cursor(dict_cursor=True):
    if dict_cursor:
        return conn.cursor(dictionary=True)
    return conn.cursor()

def get_or_create_player(player_name):
    cur = get_cursor()
    cur.execute("SELECT player_id FROM Player WHERE name = %s", (player_name,))
    row = cur.fetchone()
    if row:
        return row['player_id']
    cur = get_cursor(False)
    cur.execute("INSERT INTO Player (name, email) VALUES (%s, %s)", (player_name, f"{player_name}@example.com"))
    return cur.lastrowid

# -----------------------
# GAME FUNCTIONS
# -----------------------

def get_airports(limit=30):
    sql = """SELECT ident, name, country
             FROM Airport
             ORDER BY RAND()
             LIMIT %s"""
    cur = get_cursor()
    cur.execute(sql, (limit,))
    return cur.fetchall()

def get_goals():
    cur = get_cursor()
    cur.execute("SELECT * FROM Goal")
    return cur.fetchall()

def create_game(player_id, start_airport, money, p_range):
    sql = """INSERT INTO Game
             (player_id, start_airport, current_airport, money, player_range, score, game_status)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cur = get_cursor(False)
    cur.execute(sql, (player_id, start_airport, start_airport, money, p_range, 0, 'active'))
    return cur.lastrowid

def get_airport_info(icao):
    cur = get_cursor()
    cur.execute("SELECT ident, name, country FROM Airport WHERE ident = %s", (icao,))
    return cur.fetchone()

def goal_already_reached(game_id, goal_id):
    cur = get_cursor()
    cur.execute("SELECT 1 FROM Goal_Reached WHERE game_id = %s AND goal_id = %s LIMIT 1", (game_id, goal_id))
    return cur.fetchone() is not None

def insert_goal_reached(game_id, goal_id):
    cur = get_cursor(False)
    cur.execute("INSERT INTO Goal_Reached (game_id, goal_id) VALUES (%s, %s)", (game_id, goal_id))

def update_game_score(game_id, points):
    cur = get_cursor(False)
    cur.execute("UPDATE Game SET score = score + %s WHERE game_id = %s", (points, game_id))

def update_location(game_id, icao, p_range, money):
    cur = get_cursor(False)
    cur.execute("""UPDATE Game
                   SET current_airport = %s,
                       player_range = %s,
                       money = %s
                   WHERE game_id = %s""", (icao, p_range, money, game_id))

def find_matching_goal_by_airport(airport):
    cur = get_cursor()
    cur.execute("""SELECT goal_id, name, target_text, points
                   FROM Goal
                   WHERE target_text LIKE CONCAT('%%', %s, '%%')
                      OR name LIKE CONCAT('%%', %s, '%%')
                   LIMIT 1""", (airport['name'], airport['ident']))
    return cur.fetchone()

# -----------------------
# GAME SETUP
# -----------------------

print("Welcome to ChronoQuest!")
player_name = input("Enter your player name: ").strip() or "TestPlayer"

player_id = get_or_create_player(player_name)

# Initial settings
money = 1000
player_range = 2000
score = 0
game_over = False
win = False
diamond_found = False   # Important: initialized here

# Select random airports
all_airports = get_airports(limit=30)
if len(all_airports) == 0:
    print("No airports found in the Airport table. Exiting.")
    raise SystemExit

start_airport = all_airports[0]['ident']
current_airport = start_airport

# Create game row in DB
game_id = create_game(player_id, start_airport, money, player_range)
print(f"\nYour journey begins at {start_airport} - {all_airports[0]['name']}")

# -----------------------
# MAIN GAME LOOP
# -----------------------
while not game_over:
    airport = get_airport_info(current_airport)
    print("\n=================================")
    print(f"You are at: {airport['name']} ({airport['ident']}) — Country: {airport['country']}")
    print(f"Money: ${money:.0f} | Range: {player_range:.0f} km | Score: {score}")
    print("=================================\n")

    # Check for goal at this airport
    matching_goal = find_matching_goal_by_airport(airport)
    if matching_goal and not goal_already_reached(game_id, matching_goal['goal_id']):
        print(f"Quest available: {matching_goal['name']} ({matching_goal['points']} pts)")
        choice = input("Do you want to complete it? (Y/N): ").strip().upper()
        if choice == 'Y':
            if matching_goal['points'] > 0:
                reward = matching_goal['points']
                money += reward
                score += matching_goal['points']
                insert_goal_reached(game_id, matching_goal['goal_id'])
                update_game_score(game_id, matching_goal['points'])
                print(f"Completed '{matching_goal['name']}' → +${reward}, +{matching_goal['points']} pts")
            elif matching_goal['points'] == 0:
                insert_goal_reached(game_id, matching_goal['goal_id'])
                print("You found the Chrono Diamond! Return to the start to win.")
                diamond_found = True
            else:
                money = 0
                insert_goal_reached(game_id, matching_goal['goal_id'])
                print("You were robbed and lost all money.")

    # Refuel option
    if money > 0:
        fuel_input = input("Buy fuel? 1$ = 2 km. Enter dollars or press Enter: ").strip()
        if fuel_input:
            try:
                dollars = int(fuel_input)
                if dollars <= money and dollars >= 0:
                    money -= dollars
                    player_range += dollars * 2
                    print(f"Bought {dollars}$ fuel → +{dollars*2} km. Range = {player_range}, Money = {money}")
                else:
                    print("Invalid amount.")
            except ValueError:
                print("Not a number.")

    # Show available airports
    print("\nAirports available to fly:")
    for ap in all_airports:
        print(f"  - {ap['ident']}: {ap['name']} ({ap['country']})")

    dest = input("Enter destination ICAO (or 'quit'): ").strip().upper()
    if dest.lower() == "quit":
        game_over = True
        break

    dest_record = next((a for a in all_airports if a['ident'] == dest), None)
    if not dest_record:
        print("Invalid choice.")
        continue

    travel_cost = 200
    if player_range < travel_cost:
        print("Not enough range.")
        game_over = True
        break

    player_range -= travel_cost
    current_airport = dest
    update_location(game_id, current_airport, player_range, money)
    print(f"Flew to {dest}. Range left: {player_range} km")

    # Win conditions
    cur = get_cursor()
    cur.execute("SELECT COUNT(*) AS total FROM Goal")
    total_goals = cur.fetchone()['total'] or 0
    cur.execute("SELECT COUNT(*) AS done FROM Goal_Reached WHERE game_id = %s", (game_id,))
    done_goals = cur.fetchone()['done'] or 0

    if total_goals > 0 and done_goals == total_goals and current_airport == start_airport:
        print("All quests complete & back to start. You win!")
        win = True
        game_over = True
        break

    if diamond_found and current_airport == start_airport:
        print("Returned to start with the Chrono Diamond. You win!")
        win = True
        game_over = True
        break

    if score >= 1000:
        print("You reached 1000+ score. You win!")
        win = True
        game_over = True
        break

# -----------------------
# GAME OVER
# -----------------------
print("\n=== GAME OVER ===")
print("Result:", "WIN" if win else "LOSE")
print(f"Final Money: ${money:.0f}")
print(f"Final Range: {player_range:.0f} km")
print(f"Final Score: {score}")

# Close
conn.close()
