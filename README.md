# Agenda Import & Search CLI 📂

##### a personal productivity tool for importing, processing, and organizing agenda data for use in other tools

## overview
this tool is a small Python/SQLite pipeline for importing agenda data from an Excel `.xls` file into a local SQLite database, then querying the imported data from the command line.

it supports:
- importing sessions and subsessions from an agenda spreadsheet
- deduplicating agenda items, people, and item-person mappings
- case-insensitive lookup by common agenda fields (including people)
- printing formatted CLI results for matching agenda entries

## tech stack
- Python
- SQLite (`sqlite3`)
- `xlrd` (for `.xls` files)
