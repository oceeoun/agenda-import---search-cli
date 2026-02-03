#!/usr/bin/env python3

"""
I. Import Agenda (into interview_test.db)

Usage: ./import_agenda.py agenda.xls
Reads sheet 0 starting at Excel row 16.
Inserts rows into agenda_items, speakers, and agenda_item_to_speaker (skipping duplicates).
Prints a summary and exits zero on success, non-zero on error.
"""

import sys, os, xlrd, sqlite3
from db import open_tables, close_tables, count_rows
from db_table import db_table

HEADER_ROW = 14
DATA_START_ROW = 15

def main():
    argv = sys.argv[1:]

    # require exactly one arg (for now)
    if len(argv) != 1:
        print("Error: expected exactly one argument.")
        return 2
    
    # check file exists
    agenda_path = argv[0]
    if not os.path.isfile(agenda_path):
        print(f"Error: file '{agenda_path}' not found.")
        return 2
    
    agenda_items = speakers = agenda_item_to_speaker = None
    imported_items = imported_speakers = 0
    
    try:
        agenda_items, speakers, agenda_item_to_speaker = open_tables()

        try:
            book = xlrd.open_workbook(agenda_path)
            sh = book.sheet_by_index(0)
        except Exception as e:
            print(f"Error: failed to open '{agenda_path}' ({e})")
            return 2

        # trackers
        speaker_cache = {}
        curr_parent_id = None
        duplicate_agenda_items = duplicate_speakers = 0

        for i in range(DATA_START_ROW, sh.nrows):
            # fill agenda_items table
            row = [str(x).replace("'","''").strip() for x in sh.row_values(i)]

            # record parent_id if applicable
            session_type = row[3].strip()
            parent_id = curr_parent_id if session_type == "Sub" else None

            # insert agenda item, skipping duplicates
            try:
                agenda_item_id = agenda_items.insert({
                    "date": row[0],
                    "time_start": row[1],
                    "time_end": row[2],
                    "session_type": session_type,
                    "parent_id": parent_id,
                    "title": row[4],
                    "location": row[5],
                    "description": row[6]
                })

                # update parent_id
                if session_type != "Sub":
                    curr_parent_id = agenda_item_id
                
                imported_items += 1
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    duplicate_agenda_items += 1
                    continue # (for now) skip mapping speakers
                raise
            
            # fill speakers table and agenda_item_to_speaker table
            s = [name.strip() for name in row[7].split(";")]
            for name in s:
                if not name:
                    continue
                    
                # skip duplicates in speakers
                if name not in speaker_cache:
                    try:
                        speaker_id = speakers.insert({"speaker_name": name})
                        speaker_cache[name] = speaker_id
                        imported_speakers += 1
                    except sqlite3.IntegrityError as e:
                        if "UNIQUE constraint failed" in str(e):
                            duplicate_speakers += 1
                            speaker_cache[name] = speakers.select(["id"], { "speaker_name": name })[0]["id"]
                        else:
                            raise

                speaker_id = speaker_cache[name]
                
                # skip duplicates in agenda_item_to_speaker mappings
                try:
                    agenda_item_to_speaker.insert({
                        "agenda_item_id": agenda_item_id,
                        "speaker_id": speaker_id
                    })
                except sqlite3.IntegrityError as e:
                    if "UNIQUE constraint failed" in str(e):
                        continue
                    raise

        # summary output
        total_items = count_rows(agenda_items)
        total_speakers = count_rows(speakers)
        print(f"Imported {imported_items} new items and skipped {duplicate_agenda_items} duplicates ({total_items} total).")
        print(f"Imported {imported_speakers} new speakers and skipped {duplicate_speakers} duplicates ({total_speakers} total).")
        return 0
    
    finally:
        if agenda_items and speakers and agenda_item_to_speaker:
            close_tables(agenda_items, speakers, agenda_item_to_speaker)

if __name__ == "__main__":
    sys.exit(main())