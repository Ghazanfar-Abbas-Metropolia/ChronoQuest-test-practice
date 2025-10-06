-- ===========================================
-- ChronoQuest Database
-- ===========================================

DROP DATABASE IF EXISTS ChronoQuest;
CREATE DATABASE ChronoQuest;
USE ChronoQuest;

-- ---------------------
-- PLAYER
-- ---------------------
CREATE TABLE Player (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE
);

-- ---------------------
-- GAME
-- ---------------------
CREATE TABLE Game (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    start_airport VARCHAR(10) NOT NULL,     -- ICAO
    current_airport VARCHAR(10) NOT NULL,   -- ICAO
    money DECIMAL(10,2) NOT NULL DEFAULT 1000.00,
    player_range FLOAT NOT NULL DEFAULT 5000,
    score INT NOT NULL DEFAULT 0,
    game_status ENUM('active','won','lost') NOT NULL DEFAULT 'active',
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
);

-- ---------------------
-- AIRPORT
-- ---------------------
CREATE TABLE Airport (
    airport_id INT AUTO_INCREMENT PRIMARY KEY,
    icao_code VARCHAR(10) NOT NULL UNIQUE,   -- ICAO (e.g., KJFK, EFHK)
    name VARCHAR(150) NOT NULL,
    country VARCHAR(100) NOT NULL,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL
);

-- ---------------------
-- GOAL
-- ---------------------
CREATE TABLE Goal (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    money_value DECIMAL(10,2) NOT NULL,
    probability DECIMAL(5,2) NOT NULL, -- e.g., 0.25 = 25%
    game_id INT NOT NULL,
    airport_id INT NOT NULL,
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (airport_id) REFERENCES Airport(airport_id)
);

-- ---------------------
-- GOAL_REACHED
-- ---------------------
CREATE TABLE Goal_Reached (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    goal_id INT NOT NULL,
    airport_id INT NOT NULL,
    reached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (goal_id) REFERENCES Goal(goal_id),
    FOREIGN KEY (airport_id) REFERENCES Airport(airport_id)
);

-- ===========================================
-- INSERT SAMPLE DATA
-- ===========================================

-- 1. Player
INSERT INTO Player (name, email) VALUES 
('Test Player', 'test@example.com');

-- 2. Game (this will be game_id = 1)
INSERT INTO Game (player_id, start_airport, current_airport, money, player_range, score, game_status)
VALUES (1, 'KJFK', 'KJFK', 1000.00, 5000, 0, 'active');

-- 3. Airports
INSERT INTO Airport (icao_code, name, country, longitude, latitude) VALUES
-- USA
('KJFK', 'John F. Kennedy International Airport', 'USA', -73.7781, 40.6413),
('KLAX', 'Los Angeles International Airport', 'USA', -118.4085, 33.9416),
-- Finland
('EFHK', 'Helsinki Vantaa Airport', 'Finland', 24.9633, 60.3172),
-- Sweden
('ESSA', 'Stockholm Arlanda Airport', 'Sweden', 17.9186, 59.6519),
-- Japan
('RJTT', 'Tokyo Haneda Airport', 'Japan', 139.7798, 35.5494),
('RJAA', 'Tokyo Narita Airport', 'Japan', 140.3929, 35.7653),
-- Germany
('EDDF', 'Frankfurt am Main Airport', 'Germany', 8.5706, 50.0333),
('EDDM', 'Munich International Airport', 'Germany', 11.7861, 48.3538),
-- Norway
('ENGM', 'Oslo Gardermoen Airport', 'Norway', 11.1004, 60.2028),
('ENBR', 'Bergen Flesland Airport', 'Norway', 5.2181, 60.2934);

-- 4. Goals (linked to game_id = 1 and airport_id values in order of insert)
INSERT INTO Goal (name, money_value, probability, game_id, airport_id) VALUES
('Transatlantic Flight - USA', 500.00, 0.30, 1, 1),   -- KJFK
('Pacific Hop - USA', 450.00, 0.25, 1, 2),            -- KLAX
('Nordic Explorer - Finland', 400.00, 0.25, 1, 3),    -- EFHK
('Scandinavian Skies - Sweden', 350.00, 0.20, 1, 4),  -- ESSA
('Samurai Journey - Japan', 600.00, 0.15, 1, 5),      -- RJTT
('Rising Sun Quest - Japan', 500.00, 0.15, 1, 6),     -- RJAA
('Tech Hub Germany', 450.00, 0.18, 1, 7),             -- EDDF
('Bavarian Legacy - Germany', 420.00, 0.18, 1, 8),    -- EDDM
('Viking Spirit - Norway', 300.00, 0.22, 1, 9),       -- ENGM
('Fjord Adventure - Norway', 280.00, 0.22, 1, 10);    -- ENBR
