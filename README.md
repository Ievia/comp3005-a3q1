# COMP 3005 A3 - Question 1

Video: https://youtu.be/Hypzvbgz1OA

> Built in python 3.12 using Intellij IDEA
> 
> Depends on the "psycopg", "re" and "tabulate" python3 libraries

> ### QUICK RUN GUIDE
> 1. Create a database names "comp3005a3q1" in postgres, and make sure you have a user named "postgres" that doesn't
> have a password.
> 2. Type < python3 main.py > in the terminal to run the code.
> 3. Follow the on-screen prompts, type "1", "2", "3", "4" to select an option, or any other number else to quit the 
> program.
> 4. Enter all required info as prompted.

All code is found in a single python file < main.py > including the code to create the table and the required code as
mentioned in the assignment specs.

The code assumes you have a database named "comp3005a3q1" and a user named "postgres" which has no password. The code
can't create either of them, so they need to be made before the code can be run.

Running < python3 main.py > in the project directory's terminal will run the code as a purely terminal application.
It will show the following prompt:

```
Options:
    1. Print all the students
    2. Add a student
    3. Update a student's email
    4. Delete a student
    Enter any other number to quit
                
Pick an option 1-4 (inclusive):
```

Select 1, 2, or 3 to execute that option, and more prompts will follow. Typing anything else will quit the app.
For example, typing 2 will provide the following output (with input provided):

```
Pick an option 1-4 (inclusive): 1
What is the student's first name? John
What is the student's last name? Smith
What is the student's email? johnsmith@gmail.com
What date did they enroll (YYYY-MM-DD)? 2024-03-18
Do you want to continue? (y) y
```

> Note: Enrollment date must be entered in the YYYY-MM-DD format

Continue following onscreen prompts until program ends.
