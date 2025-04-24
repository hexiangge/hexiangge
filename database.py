def create_bet_history_table():
    conn = connect_db()
    cursor = conn.cursor()
    create_bet_history_table = """
    CREATE TABLE IF NOT EXISTS bet_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        openid VARCHAR(255),
        bet_type VARCHAR(50),
        bet_content VARCHAR(255),
        winning_numbers VARCHAR(255),
        is_win BOOLEAN,
        score_change INT,
        FOREIGN KEY (openid) REFERENCES users(openid)
    )
    """
    try:
        cursor.execute(create_bet_history_table)
        conn.commit()
    except pymysql.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()
        conn.close()
