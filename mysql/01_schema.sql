-- sports table
CREATE TABLE IF NOT EXISTS sports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL
);

-- events table
CREATE TABLE IF NOT EXISTS events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL,
    type VARCHAR(255) NOT NULL,
    sport INT NOT NULL,
    status VARCHAR(255) NOT NULL,
    scheduled_start DATETIME NOT NULL,
    actual_start DATETIME,
    FOREIGN KEY (sport) REFERENCES sports(id) ON DELETE CASCADE
);

-- events table indexes
CREATE INDEX idx_events_active ON events (active);
CREATE INDEX idx_events_sport ON events (sport);
CREATE INDEX idx_events_scheduled_start ON events (scheduled_start);
CREATE INDEX idx_events_sport_active ON events (sport, active);

-- selections table
CREATE TABLE IF NOT EXISTS selections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    event INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    active BOOLEAN NOT NULL,
    outcome VARCHAR(255) NOT NULL,
    FOREIGN KEY (event) REFERENCES events(id) ON DELETE CASCADE
);

-- selections table indexes
CREATE INDEX idx_selections_event ON selections (event);
CREATE INDEX idx_selections_active ON selections (active);
