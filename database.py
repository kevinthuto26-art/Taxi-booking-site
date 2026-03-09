import sqlite3


def init_db():
    conn = sqlite3.connect("rides.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS rides (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pickup TEXT,
        destination TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_ride(pickup, destination):
    conn = sqlite3.connect("rides.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO rides (pickup, destination, status) VALUES (?, ?, ?)",
        (pickup, destination, "waiting")
    )

    conn.commit()
    conn.close()


def get_waiting_rides():
    conn = sqlite3.connect("rides.db")
    c = conn.cursor()

    c.execute("SELECT * FROM rides WHERE status='waiting'")
    rides = c.fetchall()

    conn.close()
    return rides


def get_all_rides():
    conn = sqlite3.connect("rides.db")
    c = conn.cursor()

    c.execute("SELECT * FROM rides ORDER BY id DESC")
    rides = c.fetchall()

    conn.close()
    return rides


def accept_ride(ride_id):
    conn = sqlite3.connect("rides.db")
    c = conn.cursor()

    c.execute(
        "UPDATE rides SET status='accepted' WHERE id=?",
        (ride_id,)
    )

    conn.commit()
    conn.close()
    
    
def get_latest_ride():
    conn = sqlite3.connect("rides.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM rides ORDER BY id DESC LIMIT 1"
    )

    ride = cursor.fetchone()

    conn.close()

    return ride