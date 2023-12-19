from pandas import read_csv
from connection import get_request, patch_request
from time import sleep


def get_data():
    try:
        permit_data = read_csv("permit.csv")
        students_data = read_csv("students.csv")
        participants_data = read_csv("participants.csv")
    except FileNotFoundError:
        print("File(s) not found, make sure all these files are available.")
        print("Permit data --> permit.csv")
        print("Students data --> students.csv")
        print("Participant data --> participants.csv")
        print("For more detail, read on my github.")

    students_data.Email = students_data.Email.apply(lambda x: x.lower())
    participants_data["User Email"] = participants_data["User Email"].apply(
        lambda x: x.lower()
    )
    participants_data = participants_data[
        participants_data["Total Duration (Minutes)"] > 30
    ][["User Email"]]
    absent = [
        email
        for email in students_data["Email"]
        if email not in participants_data["User Email"].to_list()
    ]

    try:
        permit_data.Email = permit_data.Email.apply(lambda x: x.lower())
        reasons = [
            "sakit",
            "kerja",
            "ibadah",
            "kegiatan_akademik",
            "kegiatan_organisasi",
            "keluarga_sakit",
            "kerabat_sakit",
            "keluarga_meninggal",
            "kerabat_meninggal",
        ]
        permit_data.Reason = permit_data.Reason.apply(
            lambda x: "_".join(x.split()).lower()
            if "_".join(x.split()).lower() in reasons
            else None
        )
    except:
        pass

    for email in permit_data.Email:
        try:
            absent.remove(email)
        except ValueError:
            pass

    return participants_data, permit_data, students_data, absent


def is_ready(session_id, students_data, api_token):
    api_url = f"https://api.rakamin.com/api/v1/attendance_histories?module_session_id={session_id}&disable_pagination=true"
    LMS_data = get_request(url=api_url, api_token=api_token)
    LMS_email = [record["admin_output"]["email"] for record in LMS_data["data"]]
    check_email_list = [
        email for email in students_data.Email if email not in LMS_email
    ]
    num_missing = len(check_email_list)
    if num_missing == 0:
        print("All students are available, proceed.")
        return True, LMS_data
    else:
        print(f"These students not yet exist (total: {num_missing}):")
        for e in check_email_list[:3]:
            print(e)
            sleep(0.7)
        if num_missing > 3:
            print("...")
            sleep(0.7)
            for e in check_email_list[-3:]:
                print(e)
                sleep(0.7)
        return False, None


def change_attendance(id, api_token, status="attended", reason=None):
    api_url = f"https://api.rakamin.com/api/v1/attendance_histories/{id}"
    payload = {"status": status, "permit_reason": reason}
    patch_request(url=api_url, api_token=api_token, payload=payload)


def extra(students_data, absent, permit_data):
    for email in students_data["Email"]:
        if email in absent:
            print("Tidak Hadir")
        elif email in permit_data["Email"]:
            print("Izin")
        else:
            print("Hadir")


def start(api_token, participants_data, permit_data, LMS_data):
    for person in LMS_data["data"]:  # attended, missed, permitted
        email_target = person["admin_output"]["email"]
        name_target = person["admin_output"]["student_name"].title()
        sleep(1)
        if email_target in participants_data["User Email"].tolist():
            status = "attended"
            print(f"Successfully set {name_target} to attended")
            change_attendance(id=person["id"], api_token=api_token, status=status)
        elif email_target in permit_data.Email.to_list():
            status = "permitted"
            reason = permit_data["Reason"][
                permit_data["Email"] == email_target
            ].to_list()[0]
            print(f"Successfully set {name_target} to permitted, reason: {reason}")
            change_attendance(
                id=person["id"], api_token=api_token, status=status, reason=reason
            )
        else:
            change_attendance(id=person["id"], api_token=api_token, status="missed")
            print(f"Successfully set {name_target} to absent")
