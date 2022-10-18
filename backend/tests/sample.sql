INSERT INTO app_db.appuser (username, first_name, last_name, email, created_at, updated_at, is_active)
VALUES
    ('bmoore', 'Brian', 'Moore', 'BrianFMoore@dayrep.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('thyatt', 'Tammy', 'Hyatt', 'TammyDHyatt@rhyta.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('ghills', 'George', 'Hills', 'GeorgeSHills@dayrep.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('aryan', 'Annette', 'Ryan', 'AnnetteJRyan@teleworm.us', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('jwhobrey', 'James', 'Whobrey', 'JamesJWhobrey@armyspy.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('mwoodmansee', 'Mathew', 'Woodmansee', 'MathewKWoodmansee@rhyta.com', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('mtaylor', 'Michael', 'Taylor', 'MichaelJTaylor@teleworm.us', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE);
  
INSERT INTO app_db.client (name, is_active, created_at, updated_at)
VALUES
    ('dyvenia', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('google', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('neuralink', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_db.team (lead_user_id, name, short_name, is_active, created_at, updated_at)
VALUES
    (1, 'Seniors', 'Snrs', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 'Mid-levels', 'Mids', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (3, 'Juniors', 'Jnrs', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (4, 'Agile', 'agile', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_db.sponsor (client_id, name, short_name, is_active, created_at, updated_at)
VALUES
    (1, 'Alessio Civitillo', 'Alessio', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 'Sundar Pichai', 'Sundar', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (3, 'Elon Musk', 'Elon', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_db.epic (short_name, name, team_id, sponsor_id, start_date, is_active, created_at, updated_at)
VALUES
    ('App', 'Mobile app', 1, 2, CURRENT_TIMESTAMP, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Pay', 'Payment gateway', 2, 1, CURRENT_TIMESTAMP, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_db.epicarea (epic_id, name, is_active, created_at, updated_at)
VALUES
    (1, 'Login page', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (1, 'Design', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (1, 'Night mode', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    (2, 'Crypto', TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO app_db.role (short_name, name, created_at, updated_at, is_active)
VALUES
    ('Data Eng', 'Data Engineer', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('Analyst', 'Data Analyst', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('Scientist', 'Data Scientist', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('Scrum Master', 'SM', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('Team Member', 'TM', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('Epic Owner', 'EO', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    ('Feature Owner', 'FO', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE);

INSERT INTO app_db.rate (user_id, client_id, valid_from, valid_to, amount, created_at, updated_at, is_active)
VALUES
    (1, 1, '2022-01-01', '2022-02-01', 300, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (1, 2, '2022-02-01', '2022-03-01', 600, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (1, 3, '2022-03-01', '2022-04-01', 400, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (2, 1, '2022-02-01', '2022-03-01', 250, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (2, 2, '2022-01-01', '2022-02-01', 550, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (2, 3, '2022-02-01', '2022-03-01', 350, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (3, 1, '2022-03-01', '2022-04-01', 200, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (3, 2, '2022-03-01', '2022-04-01', 500, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (3, 3, '2022-01-01', '2022-02-01', 300, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE);

INSERT INTO app_db.timelog (user_id, start_time, end_time, epic_id, count_hours, count_days, month, year, epic_area_id, created_at, updated_at, is_locked)
VALUES
    (1, '2022-06-03 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (2, '2022-06-03 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (3, '2022-06-03 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (4, '2022-06-03 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (5, '2022-06-03 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (6, '2022-06-03 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (7, '2022-06-03 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (1, '2022-06-04 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (2, '2022-06-04 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (3, '2022-06-04 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (4, '2022-06-04 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (5, '2022-06-04 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (6, '2022-06-04 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (7, '2022-06-04 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (1, '2022-06-05 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (2, '2022-06-05 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (3, '2022-06-05 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (4, '2022-06-05 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (5, '2022-06-05 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (6, '2022-06-05 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (7, '2022-06-05 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (1, '2022-06-06 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (2, '2022-06-06 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (3, '2022-06-06 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (4, '2022-06-06 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (5, '2022-06-06 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (6, '2022-06-06 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (7, '2022-06-06 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (1, '2022-06-07 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (2, '2022-06-07 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (3, '2022-06-07 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (4, '2022-06-07 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (5, '2022-06-07 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (6, '2022-06-07 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE),
    (7, '2022-06-07 08:30:00.000000', '2022-06-03 13:45:00.000000', 1, 5.25, 0.66, 6, 2022, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, TRUE);
    
INSERT INTO app_db.forecast (user_id, epic_id, days, month, year, created_at, updated_at, is_locked)
VALUES
    (1, 1, 5.0, 4, 2022, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (2, 1, 5.0, 4, 2022, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (3, 1, 5.0, 4, 2022, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
    
INSERT INTO app_db.capacity (user_id, year, month, days, created_at, updated_at, is_locked)
VALUES
    (1, 2022, 1, 18, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (2, 2022, 2, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (3, 2022, 2, 12, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (5, 2022, 1, 13, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

INSERT INTO app_db.demand (team_id, epic_id, year, month, days, created_at, updated_at, is_locked)
VALUES
    (1, 1, 2022, 1, 18, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (2, 2, 2022, 2, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (3, 2, 2022, 2, 12, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE),
    (2, 1, 2022, 1, 13, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);