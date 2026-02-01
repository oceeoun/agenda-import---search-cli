#!/usr/bin/env python3

### I. Import Agenda

## Input: agenda.xls
## Output: 
#   Imported xxx sessions, xxx subsessions, xxx speakers, xxx mappings into interview_test.db
#   Error: file not found OR missing args/bad file OR parse fail OR ...

import sys, os, xlrd
from db import open_tables, close_tables
from db_table import db_table

HEADER_ROW = 14 # (for now)
DATA_START_ROW = 15 # (for now)

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
    
    try:
        agenda_items, speakers, agenda_item_to_speaker = open_tables()
        book = xlrd.open_workbook(agenda_path)
        sh = book.sheet_by_index(0)
        speaker_cache = {}

        for i in range(DATA_START_ROW, sh.nrows):
            # fill agenda_items table
            row = [str(x).replace("'", "''").strip() for x in sh.row_values(i)]
            agenda_item_id = agenda_items.insert({
                "row_index": i,
                "date": row[0],
                "time_start": row[1],
                "time_end": row[2],
                "session_type": row[3],
                "parent_id": "",
                "title": row[4],
                "location": row[5],
                "description": row[6]
            })

            # fill speakers table and agenda_item_to_speaker table
            for speaker in row[7].split(";"):
                name = speaker.strip()
                if not name:
                    continue
                    
                if name in speaker_cache:
                    speaker_id = speaker_cache[name]
                else:
                    speaker_id = speakers.insert({"speaker_name": name})
                    speaker_cache[name] = speaker_id
                
                agenda_item_to_speaker.insert({
                    "agenda_item_id": str(agenda_item_id),
                    "speaker_id": str(speaker_id)
                })
                
        print(f"Imported {len(agenda_items.select())} agenda items ({len(speakers.select())} total speakers) into interview_test.db")
        return 0
    
    finally:
        if agenda_items and speakers and agenda_item_to_speaker:
            close_tables(agenda_items, speakers, agenda_item_to_speaker)

if __name__ == "__main__":
    main()