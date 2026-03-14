import mysql.connector
import random

# Function to connect to the database
def connect_to_database():
    """Connect to the MySQL database."""
    try:
        print("Connecting to the database...")
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="school_exam"
        )
        print("Database connection successful.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: Unable to connect to the database. {err}")
        return None

# Function to fetch student details for the selected classes
def fetch_student_details(classes, cursor):
    """Fetch student details for the given classes."""
    all_students = []
    class_counts = {}
    print("\nFetching student details from the database...")
    for class_num in classes:
        try:
            query = f"SELECT roll_no, name FROM class_{class_num.strip()}"
            cursor.execute(query)
            students = cursor.fetchall()
            print(f"Class {class_num}: {len(students)} students found.")
            class_counts[class_num] = len(students)
            all_students.extend([(class_num, roll_no, name) for roll_no, name in students])
        except mysql.connector.Error as err:
            print(f"Error: Unable to fetch data for class {class_num}. {err}")
    print(f"Total students fetched: {len(all_students)}")
    return all_students, class_counts

# Function to randomize student seating
def shuffle_students(student_list):
    """Shuffle the list of students to randomize seating."""
    print("\nRandomizing student list...")
    random.shuffle(student_list)
    print("Students have been shuffled.")
    return student_list

# Function to create the seating plan
def create_seating_plan(student_list, total_rooms, desks_per_room, rows_per_room):
    """Generate the seating plan."""
    print("\nCreating the seating arrangement...")
    seating_plan = []
    total_desks = total_rooms * desks_per_room

    if len(student_list) > total_desks:
        print("Error: Not enough desks for all students. Reduce the number of students or increase the number of desks.")
        return None

    student_index = 0
    for room in range(1, total_rooms + 1):
        room_plan = []
        for row in range(1, rows_per_room + 1):
            for col in range(1, desks_per_room // rows_per_room + 1):
                if student_index < len(student_list):
                    class_num, roll_no, name = student_list[student_index]
                    room_plan.append((row, col, class_num, roll_no, name))
                    student_index += 1
                else:
                    break
        seating_plan.append((room, room_plan))
    print("Seating arrangement created successfully.")
    return seating_plan

# Function to export the seating plan to a text file
def export_to_text_file(seating_plan, class_counts, display_detailed):
    """Export the seating plan to a text file."""
    print("\nExporting seating arrangement to a text file...")
    try:
        with open("seating_plan.txt", "w") as file:
            file.write("Seating Arrangement for School Examination\n")
            file.write("=" * 80 + "\n")

            # Loop through the rooms
            for room, room_plan in seating_plan:
                file.write(f"\nRoom {room}:\n")
                file.write("-" * 80 + "\n")
                
                row_data = {}
                for seat in room_plan:
                    row, col, class_num, roll_no, name = seat
                    if row not in row_data:
                        row_data[row] = []
                    if display_detailed:
                        row_data[row].append(f"{roll_no} ({name})")
                    else:
                        row_data[row].append(f"{roll_no}")

                for row in sorted(row_data.keys()):
                    file.write(f"Row {row}: " + "\t".join(row_data[row]) + "\n")
                
                # Display class counts below the room
                room_class_counts = {class_num: 0 for class_num in class_counts.keys()}
                for seat in room_plan:
                    class_num = seat[2]
                    room_class_counts[class_num] += 1

                file.write("\nClass-wise Student Count:\n")
                for class_num, count in room_class_counts.items():
                    file.write(f"Class {class_num}: {count} students\n")
                file.write("-" * 80 + "\n")
        
        print("Seating arrangement has been saved to 'seating_plan.txt'.")
    except Exception as e:
        print(f"Error: Unable to save the seating arrangement. {e}")

# Main function
def main():
    """Main function to manage the seating arrangement process."""
    print("Welcome to the School Exam Seating Arrangement System")
    print("Project by: Govind Kumar Yadav (Class 12, JNV Dadri)")
    print("Under the guidance of Mr. Satyendra Sharma (PGT Computer Science)\n")

    # Connect to the database
    conn = connect_to_database()
    if not conn:
        print("Exiting program due to database connection failure.")
        return

    # Get user inputs
    print("\nPlease provide the necessary details to create the seating arrangement.")
    classes = input("Enter the classes to include (e.g., 6,7,8,9): ").split(',')
    num_rooms = int(input("Enter the number of rooms available: "))
    desks_per_room = int(input("Enter the total number of desks per room: "))
    rows_per_room = int(input("Enter the number of rows per room: "))
    display_detailed = input("Do you want detailed seating (Y/N)? ").strip().lower() == 'y'

    # Fetch student details from the database
    cursor = conn.cursor()
    students, class_counts = fetch_student_details(classes, cursor)

    if not students:
        print("No student data available for the selected classes. Exiting program.")
        return

    # Shuffle the students for random seating
    shuffled_students = shuffle_students(students)

    # Create the seating plan
    seating_plan = create_seating_plan(shuffled_students, num_rooms, desks_per_room, rows_per_room)

    if not seating_plan:
        print("Seating arrangement could not be created. Exiting program.")
        return

    # Export the seating plan to a text file
    export_to_text_file(seating_plan, class_counts, display_detailed)

    # Close the database connection
    cursor.close()
    conn.close()
    print("\nProgram completed successfully. Thank you for using the system!")

# Run the main program
main()
