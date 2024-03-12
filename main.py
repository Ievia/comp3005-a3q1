import psycopg


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


# create_table()
getAllStudents()
deleteStudent(4)
getAllStudents()
