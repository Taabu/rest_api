USE sports_db; 

-- sports
INSERT INTO sports (name, slug, active) 
VALUES 
('Football', 'football', TRUE), 
('Basketball', 'basketball', TRUE), 
('Tennis', 'tennis', TRUE); 

-- events
INSERT INTO events (name, slug, active, type, sport, status, scheduled_start) 
VALUES 
('Premier League', 'premier-league', TRUE, 'preplay', 1, 'Pending', '2023-07-17T00:00:00'), 
('FA Cup', 'fa-cup', TRUE, 'preplay', 1, 'Pending', '2023-07-17T01:00:00'), 
('Champions League', 'champions-league', TRUE, 'preplay', 1, 'Pending', '2023-07-17T02:00:00'), 
('NBA Finals', 'nba-finals', TRUE, 'preplay', 2, 'Pending', '2023-07-17T03:00:00'), 
('NBA Playoffs', 'nba-playoffs', TRUE, 'preplay', 2, 'Pending', '2023-07-17T04:00:00'), 
('NBA All-Stars', 'nba-all-stars', TRUE, 'preplay', 2, 'Pending', '2023-07-17T05:00:00'), 
('Wimbledon', 'wimbledon', TRUE, 'preplay', 3, 'Pending', '2023-07-17T06:00:00'), 
('French Open', 'french-open', TRUE, 'preplay', 3, 'Pending', '2023-07-17T08:00:00'), 
('US Open', 'us-open', TRUE, 'preplay', 3, 'Pending', '2023-07-17T09:00:00');


-- selections
INSERT INTO selections (name, event, price, active, outcome) 
VALUES 
('Team A', 1, 1.50, TRUE, 'Unsettled'), 
('Team B', 1, 2.50, TRUE, 'Unsettled'), 
('Draw', 1, 3.00, TRUE, 'Unsettled'), 
('Team C', 2, 1.50, TRUE, 'Unsettled'), 
('Team D', 2, 2.50, TRUE, 'Unsettled'), 
('Draw', 2, 3.00, TRUE, 'Unsettled'), 
('Team E', 3, 1.50, TRUE, 'Unsettled'), 
('Team F', 3, 2.50, TRUE, 'Unsettled'), 
('Draw', 3, 3.00, TRUE, 'Unsettled'), 
('Team G', 4, 1.50, TRUE, 'Unsettled'), 
('Team H', 4, 2.50, TRUE, 'Unsettled'), 
('Draw', 4, 3.00, TRUE, 'Unsettled'), 
('Team I', 5, 1.50, TRUE, 'Unsettled'), 
('Team J', 5, 2.50, TRUE, 'Unsettled'), 
('Draw', 5, 3.00, TRUE, 'Unsettled'), 
('Team K', 6, 1.50, TRUE, 'Unsettled'), 
('Team L', 6, 2.50, TRUE, 'Unsettled'), 
('Draw', 6, 3.00, TRUE, 'Unsettled'), 
('Player M', 7, 1.50, TRUE, 'Unsettled'), 
('Player N', 7, 2.50, TRUE, 'Unsettled'), 
('Draw', 7, 3.00, TRUE, 'Unsettled'), 
('Player O', 8, 1.50, TRUE, 'Unsettled'), 
('Player P', 8, 2.50, TRUE, 'Unsettled'), 
('Draw', 8, 3.00, TRUE, 'Unsettled'), 
('Player Q', 9, 1.50, TRUE, 'Unsettled'), 
('Player R', 9, 2.50, TRUE, 'Unsettled'), 
('Draw', 9, 3.00, TRUE, 'Unsettled'); 
