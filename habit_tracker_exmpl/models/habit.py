# ==========================
# Import necessary built-in modules
# ==========================


# datetime is a module that allows us to work with dates and times.
# We use it to store when a habit is created and when it is completed.
from datetime import datetime, timedelta


# typing is used to improve code clarity and enable static type checking.
# 'List' lets us define the expected type of lists (e.g., list of datetime values).
from typing import List




# ==========================
# Definition of the Habit class
# ==========================


class Habit:
    """
    The Habit class represents a single habit that a user wants to track.


    This class encapsulates both the data (such as name, creation date, completion log)
    and the behavior (like checking off a habit or calculating streaks) related to a habit.


    This is a practical example of Object-Oriented Programming (OOP) principles,
    where we bundle related data and logic into a reusable object.
    """


    def __init__(self, name: str, periodicity: str):
        """
        The constructor method is called when we create a new Habit object.


        :param name: A string that names the habit (e.g., 'Drink water').
        :param periodicity: How often the habit should be completed, either 'daily' or 'weekly'.
        """
        # Store the habit name provided by the user
        self.name = name


        # Convert the periodicity input to lowercase to standardize the format (e.g., 'Daily' → 'daily')
        self.periodicity = periodicity.lower()


        # Save the current date and time when the habit was created
        # This is useful for tracking progress and validating check-offs
        self.created_date = datetime.now()


        # Initialize an empty list to store timestamps of when the habit was marked as completed
        # This list will grow over time as the user checks off the habit
        self.completion_log: List[datetime] = []


    def check_off(self, date: datetime = None):
        """
        Marks the habit as completed for a specific date.


        :param date: An optional datetime object. If the user doesn't provide one, we use the current date/time.
        """
        # If the caller did not specify a date, use the current date and time
        if date is None:
            date = datetime.now()


        # Add the completion time to the log
        # This lets us track how often and when the user completed this habit
        self.completion_log.append(date)


    def get_streak(self) -> int:
        """
        Calculates how many consecutive periods (days or weeks) the user has completed the habit.


        :return: An integer representing the streak length (e.g., 5 consecutive days)
        """
        # If the completion log is empty, the user has no streak
        if not self.completion_log:
            return 0


        # Sort the completion dates from newest to oldest
        # This ensures we evaluate the streak starting from the most recent date
        log = sorted(self.completion_log, reverse=True)


        # Initialize the streak counter
        streak = 0


        # Start checking from the most recent completion
        current_period = log[0]


        # Define what counts as one period depending on the habit's periodicity
        # If the habit is daily, each period is 1 day. If weekly, each period is 7 days.
        step = timedelta(days=1) if self.periodicity == 'daily' else timedelta(weeks=1)


        # Loop over all logged completion dates
        for entry in log:
            # Check if this completion happened within the current "streak window"
            if current_period - entry <= step:
                # If yes, this continues the streak
                streak += 1


                # Move the window back to the current completion
                current_period = entry
            else:
                # If the gap is too large, the streak was broken
                break


        # Return the total count of consecutive periods with a valid completion
        return streak


    def was_broken(self) -> bool:
        """
        Checks whether the habit was ever broken by the user.


        A break means the user skipped completing the habit for a whole period.


        :return: True if the habit was broken at any point, otherwise False.
        """
        # If the user never completed the habit, it’s considered broken
        if not self.completion_log:
            return True


        # Sort the log in chronological order (earliest to latest)
        log = sorted(self.completion_log)


        # Define the expected frequency between completions
        step = timedelta(days=1) if self.periodicity == 'daily' else timedelta(weeks=1)


        # Begin from the time the habit was created
        current_expected = self.created_date


        # Go through each recorded check-off
        for entry in log:
            # If the time between the expected and actual completion is longer than allowed...
            if entry - current_expected > step:
                # ...it means a period was skipped, and the habit was broken
                return True


            # Update the expected time to this completion date (for the next iteration)
            current_expected = entry


        # If no break was found in the entire log, the habit was consistently followed
        return False