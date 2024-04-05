DB_INSERT_TABLE_ARTICLES = ("""
        INSERT INTO articles(title, author, source_link,  body) 
        VALUES (%s, %s, %s, %s)
        RETURNING id;
""")

DB_INSERT_TABLE_USERS = ("""
        INSERT INTO users (username, password) 
        VALUES (%s, %s) 
        RETURNING user_id;
""")

DB_SELECT_TABLE_USERS = """
        SELECT * FROM users WHERE username = %s AND confirmed = true;
"""

DB_SELECT_TABLE_USERS_BY_ID_CONFIRMED = """
        UPDATE users SET confirmed = true WHERE user_id = %s
"""