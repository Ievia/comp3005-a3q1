import psycopg
import re


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
            cur.execute("""
                select * from students
            """)
            data = cur.fetchall()

            for row in data:
                print(row)


def addStudent(first_name, last_name, email, enrollment_date):
    with psycopg.connect("dbname=comp3005a3q1 user=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                insert into students (%s, %s, %s, %s)
            """, (first_name, last_name, email, enrollment_date))

        conn.commit()


def updateStudentEmail(student_id, new_email):
    with psycopg.connect("dbname=comp3005a3q1 user=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                update students
                set    email = %s
                where  student_id = %s
            """, (new_email, student_id))

        conn.commit()


def deleteStudent(student_id):
    with psycopg.connect("dbname=comp3005a3q1 user=postgres") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                delete from students
                where student_id = %s
            """, (student_id,))

        conn.commit()


def main():
    try:
        create_table()
    except psycopg.errors.DuplicateTable:
        print("table \'students\' already exists")

    # main loop
    while True:
        choice = 0
        # get user input
        while True:
            try:
                print("""
Options:
    1. Add a student
    2. Update a student's email
    3. Delete a student
                """)
                choice = int(input("Pick an option 1-3 (inclusive): "))
                if choice < 1 or choice > 3:
                    print("Input a value 1-3 (inclusive)")
                    continue
                break
            except ValueError:
                print("Input a value 1-3 (inclusive)")

        match choice:
            case 1:
                f_name = input("What is the student's first name? ")
                l_name = input("What is the student's last name? ")
                email = input("What is the student's email? ")

                # pattern for a valid date
                valid_date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
                while True:
                    enrollment_date = input("What date did they enroll (YYYY-MM-DD)? ")
                    if bool(valid_date_pattern.match(enrollment_date)):
                        break
                    else:
                        print("Invalid format for date entered (YYYY-MM-DD)")

                addStudent(f_name, l_name, email, enrollment_date)
        #     case 2:
        #         updateStudentEmail()
        #     case 3:
        #         deleteStudent()

        cont = input("Do you want to continue? (y) ")
        if cont[0].lower() != 'y':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
