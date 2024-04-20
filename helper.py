from flask import redirect, render_template, session
from functools import wraps
from datetime import datetime
import sqlite3



def apology(apology):
    return render_template('apology.html', apology = apology )

def getinfo(*args):
    property_list = []
    if len(args) == 2:
        db = sqlite3.connect('flashcard.db')
        cursor = db.cursor()

        # Sử dụng cú pháp f-string để tạo câu truy vấn
        query = f"SELECT {args[0]} FROM {args[1]}"
        rows = cursor.execute(query)
        
        for row in rows:
            property_list.append(row[0])
    elif len(args) == 4:
        db = sqlite3.connect('flashcard.db')
        cursor = db.cursor()

        # Use parameterized query to prevent SQL injection
        query = f"SELECT {args[0]} FROM {args[1]} WHERE {args[2]} = ?"
        rows = cursor.execute(query, (args[3],))  # Pass the parameter as a tuple
    
        for row in rows:
            property_list.append(row[0])

        # Close the cursor and commit the transaction
        db.commit()
        cursor.close()
        db.close()
    
    return property_list


def insertinfo(table, **kwargs):
    db = sqlite3.connect('flashcard.db')
    cursor = db.cursor()

    columns = ",".join(kwargs.keys())
    question_marks = ', '.join(['?' for _ in range(len(kwargs))])
    
    query = f"INSERT INTO {table} ({columns}) VALUES ({question_marks})"
    values = list(kwargs.values())  # Convert dictionary values to a list

    cursor.execute(query, values)

    db.commit()
    db.close()


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def delete_row(table_name, column, value):
    # Connect to the SQLite database
    conn = sqlite3.connect("flashcard.db")

    # Create a cursor
    cursor = conn.cursor()

    # Build the DELETE query
    delete_query = f"DELETE FROM {table_name} WHERE {column} = '{value}'"

    # Execute the DELETE query
    cursor.execute(delete_query)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()

def getinfov2(column, table, **kwargs):
    db = sqlite3.connect('flashcard.db')
    cursor = db.cursor()
    # Construct the SQL query
    query = f"SELECT {column} FROM {table}"

    # Check if there are any additional conditions
    if kwargs:
        conditions = " AND ".join(f"{key} = ?" for key in kwargs.keys())
        query += f" WHERE {conditions}"

    # Execute the query
    results =  cursor.execute(query, tuple(kwargs.values()))
    haha = []
    for result in results:
        haha.append(result[0])
    return haha


def replacetinfo(table, **kwargs):
    db = sqlite3.connect('flashcard.db')
    cursor = db.cursor()

    columns = ",".join(kwargs.keys())
    question_marks = ', '.join(['?' for _ in range(len(kwargs))])
    
    query = f"REPLACE INTO {table} ({columns}) VALUES ({question_marks})"
    values = list(kwargs.values())  # Convert dictionary values to a list

    cursor.execute(query, values)

    db.commit()
    db.close()


def create_trigger_for_all_cards():
    db = sqlite3.connect('flashcard.db')
    cursor = db.cursor()

    trigger_query = """
        CREATE TRIGGER IF NOT EXISTS update_card_count_daily AFTER INSERT ON cards
        BEGIN
            UPDATE cards
            SET count = CASE WHEN count - 1 < 0 THEN 0 ELSE count - 1 END,
            last_update_time = datetime('now')
            WHERE strftime('%s', 'now') - strftime('%s', last_update_time) >= 86400;
        END;
    """

    cursor.execute(trigger_query)
    db.commit()
    db.close()


def updatecount():
    now = datetime.now()
    user_id = session["user_id"][0]
    deck_ids = getinfov2("id", "decks", user_id = user_id)
    if len(deck_ids) == 0:
        return
    card_ids = []
    for deck_id in deck_ids:
        card_ids.extend(getinfov2("id", "cards", deck_id = deck_id))
    for card_id in card_ids:
        front = getinfov2("front", "cards", id = card_id)[0]
        back = getinfov2("back", "cards", id = card_id)[0]
        time_str = getinfov2("last_update_time","cards", id = card_id)[0]
        time_format = "%Y-%m-%d %H:%M:%S.%f"
        oldtime = datetime.strptime(time_str, time_format)
        box_id = getinfov2("box_id", "cards",id = card_id)[0]
        deck_id = getinfov2("deck_id", "cards", id = card_id)[0]
        count = getinfov2("count", "cards", id = card_id)[0]
        distance = now - oldtime
        new_count = 0
        if count > 0:
            if distance.seconds >= count:
                new_count = 0
            else:
                new_count = count - distance.seconds
    
            
        replacetinfo("cards", id = card_id, count = new_count, front = front, back = back, box_id = box_id, deck_id = deck_id, last_update_time = datetime.now())