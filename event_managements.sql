CREATE TABLE customer (
    Customer_id INT PRIMARY KEY,
    First_name VARCHAR(50) NOT NULL,
    Last_name VARCHAR(50) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Email VARCHAR(100) NOT NULL
);
CREATE TABLE Decoration (
    Decor_id INT PRIMARY KEY,            -- Primary Key
    Decor_style VARCHAR(50) NOT NULL,    -- Decoration style (e.g., modern, classic)
    Decor_cost DECIMAL(10, 2) NOT NULL   -- Cost of the decoration
);
CREATE TABLE Venue (
    Venue_id INT PRIMARY KEY,                -- Primary Key, cannot be NULL
    Facilities VARCHAR(255),                -- Facilities can have NULL values
    location VARCHAR(100),                  -- Location can have NULL values
    Capacity INT                         -- Capacity can have NULL values              
);
CREATE TABLE Supervisor (
    Employee_id INT PRIMARY KEY,
    Manager_id INT,
    -- Other employee attributes can be added here
    FOREIGN KEY (Manager_id) REFERENCES Employee(Employee_id)
);
CREATE TABLE catering (
    category_id INT PRIMARY KEY,     -- Primary key to uniquely identify each category
    menu_type VARCHAR(255)           -- Type of menu (e.g., vegetarian, non-vegetarian, vegan)
);
CREATE TABLE menu (
    menu_item VARCHAR(255) PRIMARY KEY,  -- Name of the menu item with primary key constraint
    menu_cost DECIMAL(10, 2)             -- Cost of the menu item
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
CREATE TABLE entertainment (
    entertainment_id INT PRIMARY KEY,         -- Unique identifier for each entertainment entry
    cost DECIMAL(10, 2)                        -- Cost associated with the entertainment event
);
CREATE TABLE event (
    event_id INT PRIMARY KEY,                        -- Unique identifier for each event
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

