# Habit Tracker (DLMDSPWP01)

This is a Python-based habit tracking application designed as part of the DLMDSPWP01 course assignment. It uses Object-Oriented Programming (OOP) and Functional Programming (FP) principles.

## Features

- Create and manage daily/weekly habits
- Check off habits as completed
- Track streaks and breaks
- Analyze habits using functional methods
- Persist data using SQLite
- CLI interface (no GUI)

## Requirements

- Python 3.7 or later

## How to Run (GitHub Codespaces)

1. Open the Codespace or clone the repo.
2. Run the main program:

```bash
python3 main.py
```

## Folder Structure

```
habit_tracker_IU/
├── main.py                  # CLI interface
├── models/                  # Habit class (OOP)
├── managers/                # (Future) Habit manager module
├── analytics/               # Functional analytics
├── db/                      # Database handling (SQLite)
├── data/                    # (Optional) Predefined fixture SQL or JSON
├── tests/                   # Unit tests
├── utils/                   # Helper functions (optional)
```

## Preloaded Habits

You can optionally add habits manually or use test fixtures in the future.

## Testing

Add test files inside the `tests/` folder. Example framework: `pytest`.

## License

For educational use only.