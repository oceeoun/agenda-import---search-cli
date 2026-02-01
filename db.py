### Initialize tables
from db_table import db_table

def open_tables():
    agenda_items = db_table("agenda_items", {
        "id": "integer PRIMARY KEY",
        "row_index": "integer NOT NULL UNIQUE", # unique per agenda file import (reset DB to re-import)
        "date": "text NOT NULL",
        "time_start": "text NOT NULL",
        "time_end": "text NOT NULL",
        "session_type": "text NOT NULL", # session or subsession
        "parent_id": "integer",
        "title": "text NOT NULL",
        "location": "text",
        "description": "text"
    })

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