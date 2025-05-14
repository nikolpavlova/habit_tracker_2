# ==========================
# Import required modules and classes
# ==========================


from models.habit import Habit                        # To create Habit objects
from db.db_handler import DatabaseHandler             # For saving/loading/check-offs
from analytics.analytics_module import *              # Analytics functions
from datetime import datetime                         # To manage timestamps




# ==========================
# Display the main menu
# ==========================


def show_menu():
    """
    Displays the main menu with numbered choices for user interaction.
    """
    print("\n=== Habit Tracker Menu ===")
    print("1. Create a new habit")
    print("2. View all habits")
    print("3. Check off a habit")
    print("4. View habits by periodicity")
    print("5. View longest overall streak")
    print("6. View longest streak for a specific habit")
    print("7. Exit")




# ==========================
# Main program loop
# ==========================


def main():
    """
    Main loop that runs the Habit Tracker CLI.
    This connects all the subsystems and interacts with the user.
    """
    # Create the database handler to load/save data
    db = DatabaseHandler()


    while True:
        # Show the main menu
        show_menu()


        # Get the user's choice
        choice = input("Select an option (1-7): ")


        if choice == "1":
            # Create a new habit
            name = input("Enter a name for the habit: ")
            period = input("Enter periodicity ('daily' or 'weekly'): ").lower()


            if period not in ["daily", "weekly"]:
                print("Invalid periodicity. Must be 'daily' or 'weekly'.")
                continue


            new_habit = Habit(name=name, periodicity=period)
            db.add_habit(new_habit)
            print(f"Habit '{name}' created successfully.")


        elif choice == "2":
            # View all habits
            habits = db.get_all_habits()


            if not habits:
                print("No habits found.")
            else:
                print("\nTracked Habits:")
                for habit in habits:
                    print(f"- {habit.name} ({habit.periodicity})")


        elif choice == "3":
            # Check off a habit
            habit_name = input("Enter the name of the habit to check off: ")
            db.add_completion(habit_name)
            print(f"Habit '{habit_name}' checked off successfully.")


        elif choice == "4":
            # View habits by periodicity
            period = input("Enter periodicity ('daily' or 'weekly'): ").lower()
            habits = db.get_all_habits()
            filtered = get_habits_by_periodicity(habits, period)


            if not filtered:
                print(f"No {period} habits found.")
            else:
                print(f"\n{period.capitalize()} Habits:")
                for habit in filtered:
                    print(f"- {habit.name}")


        elif choice == "5":
            # View longest overall streak
            habits = db.get_all_habits()
            longest = get_longest_streak_all(habits)
            print(f"Longest streak across all habits: {longest} periods")


        elif choice == "6":
            # View longest streak for a single habit
            name = input("Enter the name of the habit: ")
            habits = db.get_all_habits()
            match = next((h for h in habits if h.name == name), None)


            if match:
                streak = get_longest_streak_for_habit(match)
                print(f"Longest streak for '{name}': {streak} periods")
            else:
                print(f"No habit named '{name}' found.")


        elif choice == "7":
            # Exit the application
            db.close()
            print("Goodbye!")
            break


        else:
            print("Invalid option. Please choose a number between 1 and 7.")




# ==========================
# Entry point check
# ==========================


if __name__ == "__main__":
    main()  # Start the app only when run directly
