create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL
        );
        """

create_urls_table = """
        CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        original_url TEXT,
        short_url TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """

add_user = """
        INSERT INTO users (username) VALUES (?);
        """

add_url = """
        INSERT INTO urls (user_id, original_url, short_url) VALUES (?, ?, ?);
        """
get_users = """
        SELECT username FROM users;
        """

get_user_id_by_username = """
        SELECT id FROM users WHERE username = ?;
        """

get_original_url_by_short_url = """
        SELECT original_url FROM urls JOIN users ON urls.user_id = users.id 
        WHERE short_url = ? AND users.username = ?;
        """

get_urls_by_user_name = """
        SELECT original_url, short_url FROM urls JOIN users ON urls.user_id = users.id 
        WHERE users.username = ?;
        """

delete_url_by_short_url = """
        DELETE FROM urls WHERE short_url = ? AND 
        user_id = (SELECT id FROM users WHERE username = ?);
        """

delete_user_by_username = """
        DELETE FROM users WHERE username = ?;
        """
