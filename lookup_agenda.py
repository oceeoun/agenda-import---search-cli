#!/usr/bin/env python3

"""
II. Lookup Agenda

Usage: ./lookup_agenda.py column value
Finds and prints sessions/subsessions matching the lookup condition (case-insensitive; skips duplicates).
- column must be one of: date, time_start, time_end, title, location, description, speaker
- non-speaker lookup mtaches by exact equality of the value
- speaker lookup matches a single speaker_name to agenda items containing that speaker
- if a session matches, all of its subsessions are also printed
"""

import sys, sqlite3
from db import open_tables, close_tables

ALLOWED_COLUMNS = ["date", "time_start", "time_end", "title", "location", "description", "speaker"]

def main():
    # require exactly two args
    argv = sys.argv[1:]
    if len(argv) != 2:
        print("Error: expected exactly two arguments (column and value).")
        return 2
    
    # require valid column names (case-sensitive)
    column = argv[0]
    if column not in ALLOWED_COLUMNS:
        print(f"Error: invalid column '{column}'. Must be one of: {ALLOWED_COLUMNS}")
        return 2
    
    agenda_items = speakers = agenda_item_to_speaker = None
    try:
        try:
            agenda_items, speakers, agenda_item_to_speaker = open_tables()
        except Exception as e:
            print(f"Error: failed to open database ({e}).")
            return 2
        try:
            value = argv[1]
            matches_session_ids = set()
        
            if column != "speaker":
                # match non-speaker items, case-insensitive and skips duplicates
                db = agenda_items
                id = "id"
            else:
                # match speaker items, case-insensitive and skips duplicates
                speaker_id = speakers.select(["id"], { "speaker_name":value })
                if not speaker_id:
                    print(f"No matches found for speaker '{value}'.")
                    return 0
            
                db = agenda_item_to_speaker
                id = "agenda_item_id"
                column = "speaker_id"
                value = speaker_id[0]["id"]
        
            for session in db.select([id], { column:value }):
                matches_session_ids.add(session[id])
                # also store matching session's subsessions
                for subsession in agenda_items.select(["id"], { "parent_id":session[id] }):
                    matches_session_ids.add(subsession["id"])
            
            # output for no matches
            if not matches_session_ids:
                print(f"No matches found for {column} '{value}'.")
                return 0
        
            # formatted output 
            print("-" * 20)
            ids = sorted(matches_session_ids)
            for i in range(len(ids)):
                rows = agenda_items.select(["date", "time_start", "time_end", "title", "location", "description", "session_type"], { "id":ids[i] })
                if not rows:
                    continue
                row = rows[0]
                date, time_start, time_end, title, location, description, session_type = row["date"], row["time_start"], row["time_end"], row["title"], row["location"], row["description"], row["session_type"]
                #speaker_list = "IMPLEMENT DISSSS"
            
                print(f"Match #{i+1} | {date} | {time_start} - {time_end} | {session_type}")
                print(f"Title: {title}")
                print(f"Location: {location}")
                print(f"Description: {description}")
                #print(f"Speakers: {speaker_list}")
                print("-" * 20)

            return 0
        except sqlite3.Error as e:
            print(f"Error: database query failed ({e}).")
            return 2
    finally:
        if agenda_items and speakers and agenda_item_to_speaker:
            close_tables(agenda_items, speakers, agenda_item_to_speaker)
    
if __name__ == "__main__":
    sys.exit(main())