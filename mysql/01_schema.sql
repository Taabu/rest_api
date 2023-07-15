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
    actual_start DATETIME NOT NULL,
    FOREIGN KEY (sport) REFERENCES sports(id) ON DELETE CASCADE
);

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
