import psycopg
import re
from tabulate import tabulate


def create_table():
    # Assumes the database has a user 'postgres' who can access & create
    #  a table, and has no password
    with psycopg.connect("dbname=comp3005a3q1 user=postgres") as conn:
        with conn.cursor() as cur:

            # create and populate table
            cur.execute("""
                create table students (
                    student_id      serial primary key,
                    first_name      text   not null,
                    last_name       text   not null,
                    email           text   not null     unique,
                    enrollment_date date
                );
            """)

            # insert data - sql code copied from assignment spec
            cur.execute("""
                INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
                ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
                ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
                ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
            """)

        conn.commit()


def getAllStudents():
    with psycopg.connect("dbname=comp3005a3q1 user=postgres") as conn:
        with conn.cursor() as cur:
            # retrieves all the data in the table
            cur.execute("""
                select * from students
            """)
            data = cur.fetchall()

            # prints the data in a nicely formatted way
            print("\n")
            print(tabulate(data, headers=("ID", "First Name", "Last Name", "Email", "Enrollment Date")))
            print("\n")


# adds a student to the table with the passed in variables
def addStudent(first_name, last_name, email, enrollment_date):
    with psycopg.connect("dbname=comp3005a3q1 user=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                insert into students (first_name, last_name, email, enrollment_date)
                values (%s, %s, %s, %s)
            """, (first_name, last_name, email, enrollment_date))

        conn.commit()


# updates a student with a given student_id with its new_email
def updateStudentEmail(student_id, new_email):
    with psycopg.connect("dbname=comp3005a3q1 user=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                update students
                set    email = %s
                where  student_id = %s
            """, (new_email, student_id))

        conn.commit()


# deletes a student given a student_id
def deleteStudent(student_id):
    with psycopg.connect("dbname=comp3005a3q1 user=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                delete from students
                where student_id = %s
            """, (student_id,))

        conn.commit()


def main():
    # create a table named 'students' if it doesn't exist
    try:
        create_table()
        print("Creating table...")
    except psycopg.errors.DuplicateTable:
        print("Table 'students' already exists")

    # main loop
    while True:
        choice = 0
        # get user input
        while True:
            try:
                print("""
Options:
    1. Print all the students
    2. Add a student
    3. Update a student's email
    4. Delete a student
    Enter any other number to quit
                """)
                choice = int(input("Pick an option 1-4 (inclusive): "))
                if choice < 1 or choice > 4:
                    print("Goodbye!")
                    break
                break
            except ValueError:
                print("Input a value 1-4 (inclusive)")

        match choice:
            case 1:
                getAllStudents()
            case 2:
                f_name = input("What is the student's first name? ")
                l_name = input("What is the student's last name? ")
                email = input("What is the student's email? ")

                # pattern for a valid date - since postgres is picky
                valid_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
                while True:
                    enrollment_date = input("What date did they enroll (YYYY-MM-DD)? ")
                    if bool(valid_date_pattern.match(enrollment_date)):
                        break
                    else:
                        print("Invalid format for date entered (YYYY-MM-DD)")

                addStudent(f_name, l_name, email, enrollment_date)
            case 3:
                while True:
                    id_check = input("Enter the id of the student you wish to update: ")
                    with psycopg.connect("dbname=comp3005a3q1 user=postgres") as conn:
                        with conn.cursor() as cur:
                            # checks if a student with the given id exists
                            cur.execute("""
                                select count(*) from students where student_id = %s
                            """, (id_check, ))
                            count = cur.fetchone()[0]
                            if count == 1:
                                break
                            else:
                                print("Student with that student id doesn't exist")
                new_email = input("Enter the student's new email: ")
                updateStudentEmail(id_check, new_email)
            case 4:
                id_check = input("Enter the id of the student you wish to delete: ")
                while True:
                    with psycopg.connect("dbname=comp3005a3q1 user=postgres") as conn:
                        with conn.cursor() as cur:
                            # checks if a student with the given id exists
                            cur.execute("""
                                    select count(*) from students where student_id = %s
                                """, (id_check, ))
                            count = cur.fetchone()[0]
                            if count == 1:
                                break
                            else:
                                print("Student with that student id doesn't exist")
                deleteStudent(id_check)
            # break out of the code if any other number is entered
            case _:
                break

        cont = input("Do you want to continue? (y) ")
        if cont[0].lower() != 'y':
            print("Goodbye!")
            break


# calls the main function
if __name__ == "__main__":
    main()
