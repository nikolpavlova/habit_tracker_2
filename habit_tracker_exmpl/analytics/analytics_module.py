# ==========================
# This module contains analytical functions based on functional programming principles.
# Functional programming favors pure functions that don't modify input data and have no side effects.
# Each function here takes in habit objects or lists and returns results without altering state.
# ==========================


# Import the Habit class from the models directory
from models.habit import Habit


# We use typing to make the code easier to read and validate.
# List is used to indicate a list of Habit objects.
from typing import List




def get_all_habits(habits: List[Habit]) -> List[str]:
    """
    Returns a list of habit names from a list of Habit objects.


    :param habits: A list of Habit instances (objects)
    :return: A list of strings (habit names)
    """
    return [habit.name for habit in habits]  # Use list comprehension to extract names




def get_habits_by_periodicity(habits: List[Habit], period: str) -> List[Habit]:
    """
    Returns a list of Habit objects that match a given periodicity ('daily' or 'weekly').


    :param habits: A list of Habit instances
    :param period: A string indicating the desired periodicity
    :return: A filtered list of Habit objects
    """
    return [habit for habit in habits if habit.periodicity == period.lower()]




def get_longest_streak_all(habits: List[Habit]) -> int:
    """
    Computes the longest streak found among all habits.


    :param habits: A list of Habit instances
    :return: An integer representing the longest streak found
    """
    # Use a generator expression to compute streaks for all habits
    streaks = (habit.get_streak() for habit in habits)


    # Use the built-in max function to return the largest value from the streaks
    return max(streaks, default=0)  # default=0 handles empty habit lists




def get_longest_streak_for_habit(habit: Habit) -> int:
    """
    Returns the longest streak for a single habit.


    :param habit: A single Habit instance
    :return: Integer representing the habit's streak
    """
    return habit.get_streak()