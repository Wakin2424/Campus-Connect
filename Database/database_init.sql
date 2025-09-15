CREATE TABLE course (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(50) UNIQUE,
    description TEXT
);

CREATE TABLE career (
    career_id SERIAL PRIMARY KEY,
    career_name VARCHAR(150) NOT NULL,
    description TEXT
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    contact VARCHAR(50),
    course_id INT REFERENCES course(course_id),
    career_id INT REFERENCES career(career_id),
    year_of_study INT,
    graduation_level VARCHAR(50),
    verified BOOLEAN DEFAULT FALSE,  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE qa (
    qa_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES "Auth_customuser"(id) ON DELETE CASCADE,
    course_id INT REFERENCES course(course_id) ON DELETE SET NULL,
    question TEXT NOT NULL,
    description TEXT,                     
    answers JSONB DEFAULT '[]',           
    views INT DEFAULT 0,                  
    likes INT DEFAULT 0,                  
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notes (
    note_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES "Auth_customuser"(id) ON DELETE CASCADE,
    course_id INT REFERENCES course(course_id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    file_url TEXT NOT NULL,
    file_size BIGINT,                  
    views INT DEFAULT 0,                
    rating DECIMAL(3,2) DEFAULT 0.0,  
    likes INT DEFAULT 0,                
    subjects TEXT[],                    
    pages INT,                         
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE market (
    market_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES "Auth_customuser"(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) NOT NULL UNIQUE,
    description TEXT,
    price DECIMAL(10,2),
    status BOOLEAN DEFAULT TRUE,
    amount INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE study_groups (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(150) NOT NULL,
    description TEXT,
    created_by INT REFERENCES "Auth_customuser"(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE study_group_members (
    group_id INT REFERENCES study_groups(group_id) ON DELETE CASCADE,
    user_id INT REFERENCES "Auth_customuser"(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES "Auth_customuser"(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
