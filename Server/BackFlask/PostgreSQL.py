DB_INIT_TABLE_THEME = ("""
        CREATE TABLE IF NOT EXISTS themes (
        theme_id SERIAL PRIMARY KEY,
        theme_name VARCHAR(255) UNIQUE NOT NULL
    );
        INSERT INTO themes (theme_id ,theme_name) VALUES 
        (1, 'tech'), 
        (2, 'crypto'), 
        (3, 'privacy'), 
        (4, 'security') ON CONFLICT (theme_name) DO NOTHING;;
""")

DB_CREATE_TABLE_ARTICLES = ("""
        CREATE TABLE IF NOT EXISTS articles (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        title VARCHAR(255) NOT NULL,
        publication_date DATE,
        author VARCHAR(255) NOT NULL,
        theme_id INTEGER,
        source_link VARCHAR(255) UNIQUE NOT NULL,
        image_link VARCHAR(255),
        body TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT now(),
        FOREIGN KEY (theme_id) REFERENCES themes(theme_id) ON DELETE CASCADE
    );
""")

DB_CREATE_TABLE_ANNOTATIONS = ("""
        CREATE TABLE IF NOT EXISTS annotations (
        id BIGSERIAL PRIMARY KEY,
        article_id UUID UNIQUE NOT NULL, -- Связь с таблицей "articles"
        annotation TEXT NOT NULL,
        FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
    );
""")

DB_CREATE_TABLES_INDEX = ("""
        CREATE INDEX IF NOT EXISTS idx_source_link ON articles (source_link);
""")

DB_INSERT_TABLE_ARTICLES = ("""
        INSERT INTO articles(title, author, source_link,  body, image_link) 
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
""")

DB_CREATE_TABLE_USERS = ("""
        CREATE TABLE IF NOT EXISTS users (
        user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        user_verify BOOL DEFAULT False
);
""")

DB_INSERT_TABLE_USERS = ("""
        INSERT INTO users (username, password) 
        VALUES (%s, %s) 
        RETURNING user_id;
""")

DB_SELECT_TABLE_USERS = """
        SELECT * FROM users WHERE username = %s AND password = %s AND user_verify = true;
"""
