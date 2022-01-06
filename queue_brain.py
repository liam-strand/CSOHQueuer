import csv
import cmd
from datetime import datetime
from termcolor import colored
from filelock import SoftFileLock


def overwrite(line, line_number, filename):
    """
    Overwrite a given line in a csv file with another line
    """
    queue_list = []

    with open(filename, "r", encoding="utf-8") as queue:
        old_file = csv.reader(
            queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        queue_list.extend(old_file)

    with open(filename, "w", encoding="utf-8") as queue, SoftFileLock(
        f"{filename}.lock"
    ):
        writer = csv.writer(
            queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )

        counter = 0
        for row in queue_list:
            if counter == line_number:
                writer.writerow(line)
            else:
                writer.writerow(row)
            counter += 1


def add_to_queue(name, comment, location, filename):
    """
    Add a student to the bottom of the queue
    """
    with open(filename, "a", encoding="utf-8") as queue, SoftFileLock(
        f"{filename}.lock"
    ):
        writer = csv.writer(
            queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        writer.writerow(
            [name, comment, location, datetime.now().strftime("%m-%d-%Y %H:%M:%S")]
        )


def done_student(t_asst, filename):
    """
    Mark that the current student has been helped
    """
    with open(filename, "r", encoding="utf-8") as queue:
        reader = csv.reader(
            queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )

        for row in reader:
            if row[1] == t_asst and row[2] == "helping":
                line_num = reader.line_num - 1
                row[2] = "done"
                overwrite(line=row, line_number=line_num, filename=filename)
                return

        print("You aren't helping anyone!")


def help_student(t_asst, filename):
    """
    Find the next available student and mark them as being helped
    Also update the comment to the TA's UTLN
    Also if the TA is already helping someone, ask to remove that person
    from the queue
    """

    with open(filename, "r", encoding="utf-8") as queue:
        reader = csv.reader(
            queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )

        for row in reader:
            if row[1] == t_asst and row[2] == "helping":
                print(
                    "You're already helping someone!"
                    "Do you want to remove them from the queue? (y/n)"
                )
                if input() == "y":
                    done_student(t_asst=t_asst, filename=filename)
                else:
                    print(
                        "Okay, I won't remove them. Please finish"
                        "with them before helping another student."
                    )
                    return

    with open(filename, "r", encoding="utf-8") as queue:
        reader = csv.reader(
            queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )

        for row in reader:
            if row[2] != "helping" and row[2] != "done" and row[2] != "missing":
                print_student(student=row)
                line_num = reader.line_num - 1
                row[1] = t_asst
                row[2] = "helping"
                overwrite(line=row, line_number=line_num, filename=filename)
                return

    print("no one needs help!")


def update_line(line_num, comment, location, filename):

    with open(filename, "r", encoding="utf-8") as queue:
        reader = csv.reader(
            queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )

        line_num = int(line_num)
        i = 0
        for row in reader:
            i += 1
            if i == line_num:
                student_name = row[0]
                timestamp = row[3]
                line = [student_name, comment, location, timestamp]
                overwrite(line=line, line_number=line_num, filename=filename)


def clear_queue(filename):
    data = []

    with SoftFileLock(f"{filename}.lock"):

        with open(filename, "r", encoding="utf-8") as queue:
            reader = csv.reader(
                queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            for row in reader:
                data.append(row)

        with open(filename, "w", encoding="utf-8") as queue:
            writer = csv.writer(
                queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )

            for row in data:
                if row[2] != "done":
                    writer.writerow(row)


def remove_line(name, filename):
    "Remove a student from the queue entirely"
    data = []

    with SoftFileLock(f"{filename}.lock"):

        with open(filename, "r", encoding="utf-8") as queue:
            reader = csv.reader(
                queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            for row in reader:
                data.append(row)

        with open(filename, "w", encoding="utf-8") as queue:
            writer = csv.writer(
                queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )

            for row in data:
                if not (row[0] == name and row[2] != "helping" and row[2] != "done"):
                    writer.writerow(row)


def print_queue(filename, key):
    """
    Print the entire queue with nice formatting
    """
    try:
        with open(filename, "r", encoding="utf-8") as queue:
            reader = csv.reader(
                queue, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )

            blank_row = ["", "", "", ""]
            i = 0
            for row in reader:
                digit = str(i)
                chaser = " " * (3 - len(digit)) + "|"
                print(digit, end=chaser)
                i += 1
                if key == "d":
                    if row[2] == "done":
                        print_row(row, "cyan")
                    elif row[2] == "helping":
                        print_row(blank_row, "green")
                    elif row[2] == "missing":
                        print_row(blank_row, "yellow")
                    else:
                        print_row(blank_row, "red")
                elif key == "h":
                    if row[2] == "done":
                        print_row(blank_row, "cyan")
                    elif row[2] == "helping":
                        print_row(row, "green")
                    elif row[2] == "missing":
                        print_row(blank_row, "yellow")
                    else:
                        print_row(blank_row, "red")
                elif key == "n":
                    if row[2] == "done":
                        print_row(blank_row, "cyan")
                    elif row[2] == "helping":
                        print_row(blank_row, "green")
                    elif row[2] == "missing":
                        print_row(blank_row, "yellow")
                    else:
                        print_row(row, "red")
                elif key == "m":
                    if row[2] == "done":
                        print_row(blank_row, "cyan")
                    elif row[2] == "helping":
                        print_row(blank_row, "green")
                    elif row[2] == "missing":
                        print_row(row, "yellow")
                    else:
                        print_row(blank_row, "red")
                else:
                    if row[2] == "done":
                        print_row(row, "cyan")
                    elif row[2] == "helping":
                        print_row(row, "green")
                    elif row[2] == "missing":
                        print_row(row, "yellow")
                    else:
                        print_row(row, "red")
    except FileNotFoundError:
        print("The queue has been cleared and is empty!")
# small change

def print_row(row, color):
    print(colored(f"{row[0]:^10.10}", color), end="|")
    print(colored(f"{row[1]:<35.35}", color), end="|")
    print(colored(f"{row[2]:<9.9}", color), end="|")
    print(colored(f"{row[3]:<20.20}", color))


def print_student(student):
    """
    Print a student nicely
    """

    print(f" Student: {student[0]}")
    print(f" Comment: {student[1]}")
    print(f"Location: {student[2]}")


class TALoop(cmd.Cmd):
    # pylint: disable=no-self-use, unused-argument
    """
    Run the command loop from the TA's perspective
    """

    prompt = "-> "
    intro = "Welcome to the queue manager! You are a TA."

    def __init__(self, TA, file):
        super().__init__()
        self.name = TA
        self.file = file

    def do_next(self, line):
        "Help the next student in the queue"
        help_student(t_asst=self.name, filename=self.file)

    def do_done(self, line):
        "Mark the current student as done"
        done_student(t_asst=self.name, filename=self.file)

    def do_print(self, line):
        """Print the status of the queue
        usage: print [a n h m d]
        a = all (default), n = need help, h = helping, m = missing, d = done"""

        if len(line) == 1:
            print_queue(filename=self.file, key=line[0])
        else:
            print_queue(filename=self.file, key="a")

    def do_add(self, line):
        "Add a student to the queue \nusage: add [name, comment, location]"
        if len(line) == 3:
            add_to_queue(
                name=line[0], comment=line[1], location=line[2], filename=self.file
            )
        else:
            student = input(" student: ")
            comment = input(" comment: ")
            location = input("location: ")
            add_to_queue(
                name=student, comment=comment, location=location, filename=self.file
            )

    def do_update(self, line):
        "Update a student's record in the queue \nusage: update <record number>"
        if len(line) == 1:
            comment = input(" comment: ")
            location = input("location: ")
            update_line(
                line_num=line[0],
                comment=comment,
                location=location,
                filename=self.file,
            )
        else:
            print("usage: update <record number>")

    def do_remove(self, line):
        "Remove a student from the queue \nusage: remove <utln>"

        if len(line) == 1:
            remove_line(name=line[0], filename=self.file)
        else:
            utln = input("utln: ")
            remove_line(name=utln, filename=self.file)

    def do_clear(self, line):
        "Remove all completed records from queue"
        confirmation = input(
            "Are you sure you want to remove all completed records? (y/n) "
        )

        if confirmation == "y":
            clear_queue(self.file)

    def do_quit(self, line):
        "End the program"
        print("Thank you for working the queue!")
        return True

    def do_EOF(self, line):
        "End the program"
        print("\nThank you for working the queue!")
        return True


class StudentLoop(cmd.Cmd):
    # pylint: disable=no-self-use, unused-argument
    """
    Run the command loop from the student's perspective
    """

    prompt = "-> "
    intro = "Welcome to the queue manager! You are a student."

    def __init__(self, name, file):
        super().__init__()
        self.name = name
        self.file = file

    def do_print(self, line):
        """Print the status of the queue
        usage: print [a n h m d]
        a = all (default), n = need help, h = helping, m = missing, d = done"""

        if len(line) == 1:
            print_queue(filename=self.file, key=line[0])
        else:
            print_queue(filename=self.file, key="a")

    def do_add(self, line):
        "Add yourself to the queue \nusage: add [comment location]"

        if len(line) == 2:
            add_to_queue(
                name=self.name, comment=line[0], location=line[1], filename=self.file
            )
        else:
            comment = input(" comment: ")
            location = input("location: ")
            add_to_queue(
                name=self.name, comment=comment, location=location, filename=self.file
            )

    def do_remove(self, line):
        "Remove yourself from the queue"
        remove_line(self.name, self.file)

    def do_quit(self, line):
        "End the program"
        print("Thank you for using the queue!")
        return True

    def do_EOF(self, line):
        "End the program"
        print("\nThank you for using the queue!")
        return True
