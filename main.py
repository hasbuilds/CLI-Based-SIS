import json, os, secrets, string
from json import JSONDecodeError
from openpyxl import Workbook
import getpass
from dotenv import load_dotenv

# Loading .env
load_dotenv()

# --- Environment Variables ---
ADMIN_FILE = os.getenv("ADMIN_FILE", "admin_data.json")
STUDENTS_FILE = os.getenv("STUDENTS_FILE", "students_data.json")
SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
KEY_LENGTH = int(os.getenv("KEY_LENGTH", 6))


# Admin validation
def valid_school(school): return "primary" in school.lower()
def valid_name(name): return len(name) <= 50
def valid_bd(bd): return bd.isdigit() and len(bd) == 8 and int(bd[:2]) <= 31 and int(bd[2:4]) <= 12
def valid_email(email): return "@" in email and (email.endswith(".com") or email.endswith(".org"))
def key(length=KEY_LENGTH): 
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

# Student Validation
def valid_sex(sex): return sex.strip().upper()
def students_names(student_name): return len(student_name) <= 50
def students_bd(student_bd): return student_bd.isdigit() and len(student_bd) == 8 and int(student_bd[:2]) <= 31 and int(student_bd[2:4]) <= 12
def students_classes(student_class): return isinstance(student_class, int) and 1 <= student_class <= 7
def admission(student_admission): return str(student_admission).isdigit() and len(str(student_admission)) == 4

# --- Load Admin Data ---
user_data = []
if os.path.exists(ADMIN_FILE):
    with open(ADMIN_FILE, "r") as f:
        try:
            user_data = json.load(f)
        except JSONDecodeError:
            pass

# --- Startup Page ---
while True:
    print("\n<=============| Welcome to the CLI-based-SIS |================>")
    print("\n<=====| Credits: Hassan Hamis | kalolelohh@gmail.com |========>")
    print("1. Sign Up\n2. Log In\n0. Exit")
    prompt = input("Enter (1/2/0): ").strip()

    if prompt == "0":
        print("Goodbye!")
        exit()

    elif prompt == "1":
        print("Sign Up:")
        try:
            name = input("Enter name: ").title().strip()
            bd = input(f"Hi {name}, Enter your birthdate (DDMMYYYY): ").strip()
            email = input("Enter email: ").strip()
            school = input("Enter your School: ").strip()
            
            if valid_bd(bd) and valid_name(name) and valid_email(email) and valid_school(school):
                birthday = f"{bd[:2]}/{bd[2:4]}/{bd[4:]}"
                logic_key = key()
                print(f"Verification code is {logic_key}\nPlease Verify!\n")
                verified_key = input("Enter Provided key: ")
                if verified_key == logic_key:
                    pwd = getpass.getpass("Enter your Password: ")
                    real_pwd = getpass.getpass("Reenter your Password to confirm: ")
                    if real_pwd != pwd:
                        print("Try again!")
                        continue
                else:
                     print("Try again!")
                     continue      
                user = {
                    "name": name,
                    "birthday": birthday,
                    "email": email,
                    "school": school,
                    "password": real_pwd
                }
                user_data.append(user)
                with open(ADMIN_FILE, "w") as f:
                    json.dump(user_data, f, indent=4)
                print(f"Registered! Your password is: {pwd}")
            else:
                print("Invalid inputs.")
        except ValueError:
            print("Something went wrong. Try again.")

    elif prompt == "2":
        print("Log In:")
        login_email = input("Email: ").lower().strip()
        login_pwd = getpass.getpass("Password: ").strip()

        found = next((u for u in user_data if u["email"] == login_email and u["password"] == login_pwd), None)
        if found:
            print(f"Welcome back {found['name']}! Access granted.")
            name = found["name"]
        else:
            print("Invalid credentials.")
            continue
    else:
        print("Invalid option.")
        continue

    while True:
        print('=' * 64)
        print(f"\nWelcome to The Students Portal:")
        print("Please choose:\n1. Register Student\n2. Remove Student\n3. Students List\n4. Export Students Data\n0. Logout")    

        choice = input("Enter choice (1/2/3/4/0): ").strip()
        if choice == "0":
            print("Logging out...")
            exit()

        elif choice == "1":
            print('=' * 64)
            print("Please enter student data carefully!")
            try:
                entry = int(input("No. of students to be added: "))
            except ValueError:
                print("Enter valid number!")   
                continue
            tries = 3
            while entry > 0 and tries > 0:
                try:
                    sex = input("Sex (M/F): ").strip().upper()
                    student_name = str(input("Enter full student name: ")).title()
                    student_bd = input(f"What is {student_name}'s birthday (DDMMYYYY): ").strip()
                    student_class = int(input(f"In which class is {student_name}: ").strip())
                    student_admission = int(input("Enter a year for admission (YYYY): ").strip())
                    if students_names(student_name) and admission(student_admission) and students_bd(student_bd) and students_classes(student_class):
                        stud_bd = f"{student_bd[:2]}/{student_bd[2:4]}/{student_bd[4:]}"
                        new_student = {
                            student_name: {
                                "Sex": sex,
                                "Birthdate": stud_bd,
                                "Class": student_class,
                                "Year of Admission": student_admission
                            }
                        }

                        try:
                            with open(STUDENTS_FILE, "r") as f:
                                existing = json.load(f)
                        except (FileNotFoundError, JSONDecodeError):
                            existing = {}

                        existing.update(new_student)
                        with open(STUDENTS_FILE, "w") as f:
                            json.dump(existing, f, indent=4)
                        print(f"Dear Admin, {student_name} data stored successfully!")
                        entry -= 1                                     
                    else:
                        print("Invalid student data. Please try again.")
                except ValueError:
                    print("Invalid input. Make sure to enter the correct formats.")
                tries -= 1

        elif choice == "2":
            print('=' * 64)
            try:
                with open(STUDENTS_FILE, "r") as f:
                    data = json.load(f)

                student_name = input("Enter full student name to remove: ").title().strip()
                if student_name in data:
                    print("<============| Student Found! |=============>")
                    stud_nt = str(data[student_name]).replace("'" and "{" and "}", "")
                    print(f"{stud_nt}")

                    confirm_del = input(f"Are you sure you want to remove {student_name}? (y): ").strip().lower()
                    if confirm_del == "y":
                        del data[student_name]
                        with open(STUDENTS_FILE, "w") as f:
                            json.dump(data, f, indent=4)
                        print("Deletion done successfully!")
                    else:
                        print("Deletion canceled!")
                else:
                    print("Student not found.")
            except (FileNotFoundError, JSONDecodeError):
                print("No students data found.")

        elif choice == "3":
            print('=' * 64)
            try:
                with open(STUDENTS_FILE, "r") as f:
                    students_data = json.load(f)
                    if students_data:
                        print("{:<20} {:<15} {:<15} {:<10} {:<20}".format("Name", "Sex", "Birthdate", "Class", "Year of Admission"))
                        print("-" * 65)
                        for name, details in students_data.items():
                            print("{:<20} {:<15} {:<15} {:<10} {:<20}".format(
                                name,
                                details["Sex"],
                                details["Birthdate"],
                                details["Class"],
                                details["Year of Admission"]
                            ))
                    else:
                        print("No students registered yet.")
            except (FileNotFoundError, JSONDecodeError):
                print("No students data found.")

        elif choice == "4":
            print('=' * 64)
            print("Welcome! Choose options: \n1. Export to Excel.\n2. Export to CSV\n0. Exit!")
            choice = input("Enter your choice: ")
            if choice == "1":
                with open(STUDENTS_FILE, "r") as f:
                    students_data = json.load(f)
                    if students_data:
                        wb = Workbook()
                        ws = wb.active
                        ws.title = "Students_admission_data"
                        ws.append(["Name", "Sex", "Birthdate", "Class", "Year of Admission"])
                        for name, details in students_data.items():
                            ws.append([name, details["Sex"], details["Birthdate"], details["Class"], details["Year of Admission"]])
                        wb.save("students_admissions.xlsx")
                        print("✅ Exported to 'Students_admissions.xlsx'")
