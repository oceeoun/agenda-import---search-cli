"""
Database Schema Initialization and Helpers (for interview_test.db)

Defines tables and indexes used by the agenda import pipeline.
Provides open_tables(), close_tables(), and count_rows().
"""

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

    # skip duplicate mappings
    agenda_item_to_speaker.db_conn.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS mapping
        ON agenda_item_to_speaker(agenda_item_id, speaker_id)
    """)

    agenda_item_to_speaker.db_conn.commit()

    return agenda_items, speakers, agenda_item_to_speaker

def close_tables(*tables):
    for t in tables:
        t.close()

# return the number of rows in a database table
def count_rows(table):
    return table.db_conn.execute(f"SELECT COUNT(*) FROM {table.name}").fetchone()[0]