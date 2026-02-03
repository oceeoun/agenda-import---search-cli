### Initialize tables
from db_table import db_table

def open_tables():
    agenda_items = db_table("agenda_items", {
        "id": "integer PRIMARY KEY",
        "date": "text NOT NULL",
        "time_start": "text NOT NULL",
        "time_end": "text NOT NULL",
        "session_type": "text NOT NULL", # session or subsession
        "parent_id": "integer",
        "title": "text NOT NULL",
        "location": "text",
        "description": "text"
    })

    # skip duplicate sessions
    agenda_items.db_conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS agenda_item
        ON agenda_items(date, time_start, time_end, session_type, parent_id, title, location, description)
    """)

    # (for now) skip duplicate subsessions even if they have a different parent_id
    agenda_items.db_conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS agenda_sub_item
        ON agenda_items(date, time_start, time_end, session_type, title, location, description)
        WHERE session_type = 'Sub'
    """)

    agenda_items.db_conn.commit()

    speakers = db_table("speakers", {
        "id": "integer PRIMARY KEY",
        "speaker_name": "text NOT NULL UNIQUE"
    })

    agenda_item_to_speaker = db_table("agenda_item_to_speaker", {
        "agenda_item_id": "integer NOT NULL",
        "speaker_id": "integer NOT NULL"
    })

    return agenda_items, speakers, agenda_item_to_speaker

def close_tables(*tables):
    for t in tables:
        t.close()