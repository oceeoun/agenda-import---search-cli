#!/usr/bin/env python3

"""
II. Lookup Agenda


"""

import sys
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
        
        value = argv[1]
        matches_session_ids = list()
        matches_sub_ids = list()
        
        if column != "speaker":
            for session in agenda_items.select(["id"], { column:value }):
                matches_session_ids.append(session["id"])
                for subsession in agenda_items.select(["id"], { "parent_id":session["id"]}):
                    matches_session_ids.append(subsession["id"])
            print(matches_session_ids)

        else:
            speaker_id = None
        
        # formatted output 
        print("-" * 20)
        for id in matches_session_ids:
            row = agenda_items.select(["date", "time_start", "time_end", "title", "location", "description", "session_type"], { "id":id })[0]
            date, time_start, time_end, title, location, description, session_type = row["date"], row["time_start"], row["time_end"], row["title"], row["location"], row["description"], row["session_type"]
            #speaker_list = "IMPLEMENT DISSSS"
            
            print(f"{date} | {time_start} - {time_end} | {session_type}")
            print(f"Title: {title}")
            print(f"Location: {location}")
            print(f"Description: {description}")
            #print(f"Speakers: {speaker_list}")
            print("-" * 20)

        return 0
    finally:
        if agenda_items and speakers and agenda_item_to_speaker:
            close_tables(agenda_items, speakers, agenda_item_to_speaker)

    # non-speakers
    # search in lowercase and store matching session ids (agenda_items)
    # search in lowercase and store matching subsessions ids (agenda_items)
    # search + store subsession ids of matching session ids (agenda_items["parent_id"])
    # store all stored ids into a set (deduplicate)

    # speakers
    # search in lowercase and store matching session ids (agenda_item_to_speaker)
    # search + store subsession ids of matching session ids (agenda_items["parent_id"])
    # store all stored ids into a set (deduplicate)

    # result
    # store each id's info (row) into a list -> return that list!

    # --- Please note: ---
    # * Your program should look for both sessions and subsessions
    # * For all matched session, you should return all its corresponding subsessions
    # * We do not expect any specific output format as long as the results are distinguishable and all the information about that session is correct.
    # * We are looking for an exact match for date, time_start, time_end, title, location and description.
    # * For speaker, we will only pass one name at a time. We will expect all sessions where we can find this speaker, even though he may not be the only speaker.
    
if __name__ == "__main__":
    sys.exit(main())