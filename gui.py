import pickle
import streamlit as st
import matplotlib.pyplot as plt

# Disable the PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)

# with open("best_particle_random.pkl", "rb") as f:
#     best_solution_random = pickle.load(f)

with open("best_particle_level_based.pkl", "rb") as f:
    best_solution_level_based = pickle.load(f)

with open("constants.pkl", "rb") as f:
    constants_dict = pickle.load(f)

# Retrieve constants from the dictionary
TIMESLOTS = constants_dict["TIMESLOTS"]
DAYS = constants_dict["DAYS"]
POPULAR_COURSE_COMBINATIONS = constants_dict["POPULAR_COURSE_COMBINATIONS"]

# Define your functions here

# Function to display courses by level
def display_courses_by_level(level):
    if level < 1 or level > len(POPULAR_COURSE_COMBINATIONS):
        print("Invalid level. Please choose a valid student level between 1 and", len(POPULAR_COURSE_COMBINATIONS))
        return []
    courses = POPULAR_COURSE_COMBINATIONS[level - 1]
    print("Courses available for Level", level, ":")
    for course_id in courses:
        print("Course ID:", course_id)
    return courses


# Function to display timetable for selected courses
def display_timetable_for_selected_courses(best, selected_courses):
    # Filter the schedule for selected courses
    filtered_schedule = {day: {timeslot: [] for timeslot in TIMESLOTS} for day in DAYS}
    for course_id, lecturer_id, room_id, timeslot_id in best:
        if course_id in selected_courses:
            day_index = timeslot_id // len(TIMESLOTS)
            time_index = timeslot_id % len(TIMESLOTS)
            day = DAYS[day_index]
            time = TIMESLOTS[time_index]
            entry = f"C{course_id} L{lecturer_id} R{room_id}"
            filtered_schedule[day][time].append(entry)

    # Create and display the timetable with matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))  # Adjust size as needed
    table_data = [[filtered_schedule[day][time] for time in TIMESLOTS] for day in DAYS]
    table = ax.table(cellText=table_data, colLabels=TIMESLOTS, rowLabels=DAYS, cellLoc='center', loc='center', colColours=['#ffe5e5']*len(TIMESLOTS))
    ax.set_title("Timetable for Selected Courses")
    ax.axis('tight')
    ax.axis('off')
    table.auto_set_font_size(False)
    table.set_fontsize(8)  # Adjust font size for better readability
    table.scale(1, 1.5)  # Adjust table scale for spacing
    plt.close()  # Close the figure to avoid displaying it in Streamlit
    return fig


# Streamlit app
def main():
    st.title("University Timetable Scheduler")

    # Allow user to select a level
    level = st.sidebar.number_input("Enter your student level (1-4):", min_value=1, max_value=4)

    # Display courses for selected level in the sidebar
    available_courses = display_courses_by_level(level)
    if available_courses:
        st.sidebar.write(f"**Courses available for Level {level}:**")
        for course_id in available_courses:
            st.sidebar.write(f"- Course ID: {course_id}")

    # Allow user to select courses from the available ones
    selected_course_ids = st.sidebar.text_input("Enter the course IDs you want to include in your timetable, separated by commas:")

    if selected_course_ids:
        selected_course_ids = [int(id.strip()) for id in selected_course_ids.split(',') if int(id.strip()) in available_courses]

        # Display timetable for the selected courses
        if selected_course_ids:
            st.pyplot(display_timetable_for_selected_courses(best_solution_level_based, selected_course_ids))


if __name__ == "__main__":
    main()
