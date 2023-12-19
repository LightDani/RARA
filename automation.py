from time import sleep

import auth
import courses
import attendance
import check_libraries
from clear_console import clear_console


def main():
    # List of required libraries
    required_libraries = ["pandas", "time", "requests", "keyring", "os"]
    for lib in required_libraries:
        check_libraries.check_install(lib)

    clear_console()
    for i in range(3):
        print(f"Rakamin Auto Student's Attendance Recap{'.'*(i+1)}")
        print("By Dwi Cahya Nur Faizi")
        sleep(1)
        clear_console()

    api_token = auth.start()
    courses_name, courses_id = courses.get_courses(api_token=api_token)

    clear_console()
    print("Choose your course!")
    for i, name in enumerate(courses_name):
        print(f"{i+1}. {name}")

    try:
        option = int(input("Type a number... "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return exit(1)

    print("\nPlease wait...")

    module_name, module_id = courses.get_live_sessions(
        course_id=courses_id[option - 1], api_token=api_token
    )

    clear_console()
    print("List 6 last live sessions:")
    print("Choose your live session!")
    for i, name in enumerate(module_name[::-1]):
        print(f"{i+1}. {name}, id={module_id[-(i+1)]}")

    try:
        option = int(input("Type a number... "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return exit(1)

    session_id = module_id[-(option)]

    participants_data, permit_data, students_data, absent = attendance.get_data()

    sleep(1)
    clear_console()
    print("Checking all students name are available in LMS...\n")
    sleep(1.5)

    ready, LMS_data = attendance.is_ready(
        session_id=session_id, students_data=students_data, api_token=api_token
    )

    if ready:
        attendance.start(
            api_token=api_token,
            participants_data=participants_data,
            permit_data=permit_data,
            LMS_data=LMS_data,
        )
        print("\nEnjoy! See you later.")
    else:
        sleep(1)
        print("\nLMS is usually ready in 1 day after the live session")
        print("See you later.")
        return exit(1)

    sleep(3)
    clear_console()
    option = input("Wait.. Are you CC JAP? (y/n) ")
    if option.lower() == "y":
        print(
            "\nSince we need to recap both in website and spreadsheet, here i also got your back."
        )
        print("Copy below output and paste it on spreadsheet.\n")
        attendance.extra(
            students_data=students_data, absent=absent, permit_data=permit_data
        )
        print()
    else:
        print("Oh, ok.", end=" ")

    print("Goodbye~")


if __name__ == "__main__":
    main()
