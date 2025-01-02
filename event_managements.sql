CREATE TABLE customer (
    Customer_id SERIAl PRIMARY KEY,
    First_name VARCHAR(50) NOT NULL,
    Last_name VARCHAR(50) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Email VARCHAR(100) NOT NULL
);
CREATE TABLE Decoration (
    Decor_id SERIAL PRIMARY KEY,            -- Primary Key
    Decor_style VARCHAR(50) NOT NULL,    -- Decoration style (e.g., modern, classic)
    Decor_cost DECIMAL(10, 2) NOT NULL   -- Cost of the decoration
);
CREATE TABLE Venue (
    Venue_id SERIAL PRIMARY KEY,                -- Primary Key, cannot be NULL
    Facilities VARCHAR(255),                -- Facilities can have NULL values
    location VARCHAR(100),                  -- Location can have NULL values
    Capacity INT                         -- Capacity can have NULL values              
);
CREATE TABLE Supervisor (
    Employee_id SERIAL PRIMARY KEY,
    Manager_id INT,
    -- Other employee attributes can be added here
    FOREIGN KEY (Manager_id) REFERENCES Supervisor(Employee_id)
);
CREATE TABLE catering (
    category_id SERIAL PRIMARY KEY,     -- Primary key to uniquely identify each category
    menu_type VARCHAR(255)           -- Type of menu (e.g., vegetarian, non-vegetarian, vegan)
);
CREATE TABLE menu (
    menu_item VARCHAR(255) PRIMARY KEY,  -- Name of the menu item with primary key constraint
    menu_cost DECIMAL(10, 2)             -- Cost of the menu item
);
CREATE TABLE entertainment (
    entertainment_id SERIAL PRIMARY KEY,         -- Unique identifier for each entertainment entry
    cost DECIMAL(10, 2)                        -- Cost associated with the entertainment event
);
CREATE TABLE dance (
    style VARCHAR(255) PRIMARY KEY,        -- Unique style of dance (used as primary key)
    group_size INT,                        -- Group size of dancers
    entertainment_id INT,                  -- Foreign key linking to the entertainment table
    FOREIGN KEY (entertainment_id) REFERENCES entertainment(entertainment_id)  -- Foreign key reference
);
CREATE TABLE music (
    genre VARCHAR(255) PRIMARY KEY,          -- Genre of music as the primary key (unique)
    number_of_performers INT,               -- Number of performers in the music group
    entertainment_id INT,                   -- Foreign key linking to the entertainment table
    FOREIGN KEY (entertainment_id) REFERENCES entertainment(entertainment_id)  -- Foreign key reference
);
CREATE TABLE comedy (
    comedy_name VARCHAR(255) PRIMARY KEY,     -- Unique name for the comedy genre
    humour_type VARCHAR(255),                 -- Type of humour (e.g., slapstick, dark humour, etc.)
    entertainment_id INT,                     -- Foreign key linking to the entertainment table
    FOREIGN KEY (entertainment_id) REFERENCES entertainment(entertainment_id)  -- Foreign key reference
);
CREATE TABLE event (
    event_id SERIAL PRIMARY KEY,                        -- Unique identifier for each event
    event_type VARCHAR(255),                          -- Type of event (e.g., Wedding, Conference, Party)
    event_date DATE,                                  -- Date of the event
    venue_id INT,                                     -- Foreign key linking to the venue table
    catering_id INT,                                  -- Foreign key linking to the catering table
    decor_id INT,                                     -- Foreign key linking to the decor table
    customer_id INT,                                  -- Foreign key linking to the customer table
    entertainment_id INT,                             -- Foreign key linking to the entertainment table
    FOREIGN KEY (venue_id) REFERENCES venue(venue_id),  -- Foreign key reference to venue
    FOREIGN KEY (catering_id) REFERENCES catering(category_id),  -- Foreign key reference to catering
    FOREIGN KEY (decor_id) REFERENCES decoration(decor_id),        -- Foreign key reference to decor
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),  -- Foreign key reference to customer
    FOREIGN KEY (entertainment_id) REFERENCES entertainment(entertainment_id)  -- Foreign key reference to entertainment
);

INSERT INTO customer (First_name, Last_name, Phone, Email)
VALUES
    ('John', 'Doe', '1234567890', 'john.doe@example.com'),
    ('Jane', 'Smith', '9876543210', 'jane.smith@example.com'),
    ('Alice', 'Johnson', '5551234567', 'alice.johnson@example.com'),
    ('Bob', 'Brown', '5559876543', 'bob.brown@example.com'),
    ('Charlie', 'Davis', '5552468100', 'charlie.davis@example.com');


INSERT INTO Decoration (Decor_style, Decor_cost)
VALUES
    ('Modern', 150.00),
    ('Classic', 200.00),
    ('Vintage', 180.00),
    ('Rustic', 220.00),
    ('Minimalistic', 170.00);

INSERT INTO Venue (Facilities, location, Capacity)
VALUES
    ('AC, Parking', 'Noma Convention', 200),
    ('AC, Stage', 'Grand Hall', 300),
    ('Parking', 'City Center', 150),
    ('AC, Outdoor', 'Beach Resort', 100),
    ('AC, Audio', 'Royal Palace', 250);

INSERT INTO Supervisor (Manager_id)
VALUES
    (NULL),
    (1),  -- Assuming Employee_id 1 is a manager
    (2),
    (1),
    (3);


INSERT INTO catering (menu_type)
VALUES
    ('Vegetarian'),
    ('Non-Vegetarian'),
    ('Vegan'),
    ('Gluten-Free'),
    ('Seafood');


INSERT INTO menu (menu_item, menu_cost)
VALUES
    ('Veg Sandwich', 10.00),
    ('Chicken Sandwich', 12.00),
    ('Vegan Salad', 8.00),
    ('Fish Fillet', 15.00),
    ('Fruit Platter', 6.00);


INSERT INTO dance (style, group_size, entertainment_id)
VALUES
    ('Hip Hop', 10, 1),
    ('Ballet', 5, 2),
    ('Salsa', 8, 3),
    ('Breakdance', 6, 4),
    ('Contemporary', 7, 5);

INSERT INTO music (genre, number_of_performers, entertainment_id)
VALUES
    ('Jazz', 5, 1),
    ('Rock', 4, 2),
    ('Classical', 6, 3),
    ('Pop', 3, 4),
    ('Blues', 4, 5);

INSERT INTO comedy (comedy_name, humour_type, entertainment_id)
VALUES
    ('Stand Up', 'Slapstick', 1),
    ('Sketch Comedy', 'Dark Humour', 2),
    ('Improv', 'Observational', 3),
    ('Parody', 'Surreal', 4),
    ('Roast Comedy', 'Satirical', 5);

INSERT INTO entertainment (cost)
VALUES
    (500.00),
    (300.00),
    (450.00),
    (600.00),
    (700.00);


INSERT INTO event (event_type, event_date, venue_id, catering_id, decor_id, customer_id, entertainment_id)
VALUES
    ('Birthday', '2025-01-15', 1, 1, 1, 1, 1),
    ('Wedding', '2025-02-20', 2, 2, 2, 2, 2),
    ('Conference', '2025-03-10', 3, 3, 3, 3, 3),
    ('Party', '2025-04-05', 4, 4, 4, 4, 4),
    ('Exhibition', '2025-05-18', 5, 5, 5, 5, 5);
