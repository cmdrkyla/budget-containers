-- Not adding contraints for now --

-- TABLE activity --
DROP TABLE IF EXISTS activity;
CREATE TABLE IF NOT EXISTS activity(
    id INTEGER PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deactivated_at DATETIME NULL,
    modified_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    amount DECIMAL(8,2) NOT NULL,
    container_id INTEGER NOT NULL,
    description VARCHAR(50) NOT NULL DEFAULT "",
    paid_on DATE NOT NULL,
    period_id INTEGER NOT NULL
);
DROP INDEX IF EXISTS idx_user_id;
DROP INDEX IF EXISTS idx_container_id;
DROP INDEX IF EXISTS idx_period_id;
CREATE INDEX idx_user_id ON activity(user_id);
CREATE INDEX idx_container_id ON activity(container_id);
CREATE INDEX idx_period_id ON activity(period_id);


-- TABLE container --
DROP TABLE IF EXISTS container;
CREATE TABLE IF NOT EXISTS container(
    id INTEGER PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deactivated_at DATETIME NULL,
    modified_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL
);
DROP INDEX IF EXISTS idx_user_id; 
CREATE INDEX idx_user_id ON container(user_id); 


-- TABLE period --
DROP TABLE IF EXISTS period;
CREATE TABLE IF NOT EXISTS period(
    id INTEGER PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deactivated_at DATETIME NULL,
    modified_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    stop_date DATE NOT NULL
);
DROP INDEX IF EXISTS idx_user_id;
DROP INDEX IF EXISTS idx_dates;
CREATE INDEX idx_user_id ON period (user_id); 
CREATE INDEX idx_dates ON period(start_date, stop_date);


-- TABLE user --
DROP TABLE IF EXISTS user;
CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deactivated_at DATETIME NULL,
    modified_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email_address VARCHAR(100) NOT NULL,
    login_token CHAR(64) NULL,
    name_first VARCHAR(50) NOT NULL,
    name_last VARCHAR(50) NOT NULL,
    password_hash CHAR(96) NOT NULL
);
DROP INDEX IF EXISTS email_address;
DROP INDEX IF EXISTS idx_login_token;
DROP INDEX IF EXISTS idx_email_address;
CREATE INDEX idx_login_token ON user(login_token);
CREATE INDEX idx_email_address ON user(email_address);


-- Create default user --
INSERT INTO user(email_address, name_first, name_last, password_hash) 
VALUES(
    'eadiek@gmail.com', 'Kyla', 'Eadie',
    /* 12345 */
    'pbkdf2$sha256$150000$t2SfbLfZpq$b6096e2bb880bf507ea815a88271f08ba791321d1bdf4e72e3633437d60af3eb'
);