CREATE DATABASE IF NOT EXISTS fitness_club
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE fitness_club;


CREATE TABLE clients (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    gender ENUM('male', 'female') NOT NULL,
    birth_date DATE NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE trainers (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE,
    gender ENUM('male', 'female') NOT NULL,
    birth_date DATE NULL,
    specialization VARCHAR(255) NOT NULL DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE services (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    service_type ENUM('group', 'individual') NOT NULL,
    default_duration_minutes INT UNSIGNED NOT NULL,
    default_capacity INT UNSIGNED NOT NULL DEFAULT 1,
    price DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_services_duration
        CHECK (default_duration_minutes > 0),

    CONSTRAINT chk_services_capacity
        CHECK (default_capacity > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE membership_plans (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL,
    duration_days INT UNSIGNED NOT NULL,
    visit_limit INT UNSIGNED NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_membership_plans_duration
        CHECK (duration_days > 0),

    CONSTRAINT chk_membership_plans_visit_limit
        CHECK (visit_limit IS NULL OR visit_limit > 0)
) ENGINE=InnoDB;


CREATE TABLE client_memberships (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    client_id BIGINT UNSIGNED NOT NULL,
    membership_plan_id BIGINT UNSIGNED NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    remaining_visits INT UNSIGNED NULL,
    status ENUM('active', 'expired', 'frozen', 'used_up') NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_client_memberships_client
        FOREIGN KEY (client_id) REFERENCES clients(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_client_memberships_plan
        FOREIGN KEY (membership_plan_id) REFERENCES membership_plans(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_client_memberships_dates
        CHECK (end_date >= start_date)
) ENGINE=InnoDB;


CREATE TABLE trainer_work_slots (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    trainer_id BIGINT UNSIGNED NOT NULL,
    start_datetime DATETIME NOT NULL,
    end_datetime DATETIME NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    comment VARCHAR(255) NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_trainer_work_slots_trainer
        FOREIGN KEY (trainer_id) REFERENCES trainers(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT chk_trainer_work_slots_time
        CHECK (end_datetime > start_datetime)
) ENGINE=InnoDB;


CREATE TABLE sessions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    service_id BIGINT UNSIGNED NOT NULL,
    trainer_id BIGINT UNSIGNED NOT NULL,
    start_datetime DATETIME NOT NULL,
    end_datetime DATETIME NOT NULL,
    capacity INT UNSIGNED NOT NULL DEFAULT 1,
    price DECIMAL(10,2) NOT NULL,
    status ENUM('planned', 'completed', 'canceled') NOT NULL DEFAULT 'planned',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_sessions_service
        FOREIGN KEY (service_id) REFERENCES services(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_sessions_trainer
        FOREIGN KEY (trainer_id) REFERENCES trainers(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT chk_sessions_time
        CHECK (end_datetime > start_datetime),

    CONSTRAINT chk_sessions_capacity
        CHECK (capacity > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE bookings (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    client_id BIGINT UNSIGNED NOT NULL,
    session_id BIGINT UNSIGNED NOT NULL,
    status ENUM('booked', 'visited', 'canceled', 'missed') NOT NULL DEFAULT 'booked',
    price_final DECIMAL(10,2) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_bookings_client
        FOREIGN KEY (client_id) REFERENCES clients(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_bookings_session
        FOREIGN KEY (session_id) REFERENCES sessions(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT uq_bookings_client_session
        UNIQUE (client_id, session_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE one_time_visits (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    client_id BIGINT UNSIGNED NOT NULL,
    visit_date DATE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    status ENUM('paid', 'visited', 'canceled') NOT NULL DEFAULT 'paid',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_one_time_visits_client
        FOREIGN KEY (client_id) REFERENCES clients(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE INDEX idx_clients_last_first ON clients(last_name, first_name);

CREATE INDEX idx_trainers_last_first ON trainers(last_name, first_name);

CREATE INDEX idx_sessions_service_id ON sessions(service_id);
CREATE INDEX idx_sessions_trainer_id ON sessions(trainer_id);
CREATE INDEX idx_sessions_start_datetime ON sessions(start_datetime);
CREATE INDEX idx_sessions_trainer_time ON sessions(trainer_id, start_datetime, end_datetime);

CREATE INDEX idx_bookings_client_id ON bookings(client_id);
CREATE INDEX idx_bookings_session_id ON bookings(session_id);

CREATE INDEX idx_client_memberships_client_id ON client_memberships(client_id);
CREATE INDEX idx_client_memberships_plan_id ON client_memberships(membership_plan_id);

CREATE INDEX idx_trainer_work_slots_trainer_id ON trainer_work_slots(trainer_id);
CREATE INDEX idx_trainer_work_slots_start_datetime ON trainer_work_slots(start_datetime);
CREATE INDEX idx_trainer_work_slots_trainer_time ON trainer_work_slots(trainer_id, start_datetime, end_datetime);

CREATE INDEX idx_one_time_visits_client_id ON one_time_visits(client_id);
CREATE INDEX idx_one_time_visits_visit_date ON one_time_visits(visit_date);