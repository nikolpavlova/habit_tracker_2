# ==========================
# Import built-in modules
# ==========================


# sqlite3 allows us to interact with a local SQLite database file
import sqlite3


# datetime is used to handle and format timestamps
from datetime import datetime


# Typing allows us to annotate return types and function signatures
from typing import List


# We import the Habit class so we can instantiate Habit objects from DB rows
from models.habit import Habit




# ==========================
# DATABASE HELPER CLASS
# ==========================


class DatabaseHandler:
    """
    This class manages all interaction with the SQLite database.
    It handles table creation, inserting and retrieving habits, and storing completion logs.
    """


    def __init__(self, db_name: str = "habit_tracker.db"):
        """
        Constructor: Connects to the database and ensures tables exist.
        :param db_name: Name of the SQLite file to use or create.
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()  # Ensure required tables exist


    def create_tables(self):
        """
        Creates the 'habits' and 'completions' tables if they do not already exist.
        """
        # Create 'habits' table to store basic habit metadata
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                created_date TEXT NOT NULL
            )
        """)


        # Create 'completions' table to store when habits are checked off
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_date TEXT NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits(id)
            )
        """)


        # Apply the changes to the database
        self.connection.commit()


    def add_habit(self, habit: Habit):
        """
        Inserts a new habit into the 'habits' table.
        :param habit: Habit object to save
        """
        self.cursor.execute(
            "INSERT INTO habits (name, periodicity, created_date) VALUES (?, ?, ?)",
            (habit.name, habit.periodicity, habit.created_date.isoformat())
        )
        self.connection.commit()


    def get_all_habits(self) -> List[Habit]:
        """
        Loads all habits from the database and reconstructs Habit objects (including their logs).
        :return: A list of Habit objects
        """
        # Step 1: Fetch habit metadata
        self.cursor.execute("SELECT id, name, periodicity, created_date FROM habits")
        habit_rows = self.cursor.fetchall()


        habits = []


        for row in habit_rows:
            habit_id, name, periodicity, created_str = row


            # Step 2: Reconstruct Habit object
            habit = Habit(name=name, periodicity=periodicity)
            habit.created_date = datetime.fromisoformat(created_str)


            # Step 3: Fetch completion timestamps for this habit
            self.cursor.execute(
                "SELECT completed_date FROM completions WHERE habit_id = ?", (habit_id,)
            )
            completions = self.cursor.fetchall()


            # Step 4: Convert completion timestamps to datetime objects and load into the habit
            for (completed_date,) in completions:
                habit.completion_log.append(datetime.fromisoformat(completed_date))


            # Step 5: Add to the list of habits
            habits.append(habit)


        return habits


    def add_completion(self, habit_name: str, completed_date: datetime = None):
        """
        Records a new check-off for the specified habit.
        :param habit_name: The name of the habit being checked off
        :param completed_date: Optional datetime; defaults to now
        """
        if completed_date is None:
            completed_date = datetime.now()


        # First, find the habit ID by name
        self.cursor.execute(
            "SELECT id FROM habits WHERE name = ?", (habit_name,)
        )
        result = self.cursor.fetchone()


        if result:
            habit_id = result[0]


            # Record the check-off with a timestamp
            self.cursor.execute(
                "INSERT INTO completions (habit_id, completed_date) VALUES (?, ?)",
                (habit_id, completed_date.isoformat())
            )
            self.connection.commit()


    def close(self):
        """
        Closes the database connection to release resources.
        """
        self.connection.close()
