import csv
import cmd
from datetime import datetime
from termcolor import colored
from filelock import SoftFileLock


def overwrite(line, lineNumber, filename):
    """
    Overwrite a given line in a csv file with another line
    """
    queueList = []

    
    with open(filename, 'r') as queue:
        oldFile = csv.reader(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)
        queueList.extend(oldFile)

    with open(filename, "w") as queue, SoftFileLock(f"{filename}.lock"):
        writer = csv.writer(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)
        
        counter = 1
        for row in queueList:
            if counter == lineNumber:
                writer.writerow(line)
            else:
                writer.writerow(row)
            counter += 1

def addToQueue(name, comment, location, filename):
    """
    Add a student to the bottom of the queue
    """
    with open(filename, "a") as queue, SoftFileLock(f"{filename}.lock"):
        writer = csv.writer(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)
        writer.writerow([name, comment, location, 
                         datetime.now().strftime('%m-%d-%Y %H:%M:%S')])

def doneStudent(TA, filename):
    """
    Mark that the current student has been helped
    """
    with open(filename, "r") as queue:
        reader = csv.reader(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            if row[1] == TA and row[2] == "helping":
                lineNum = reader.line_num
                row[2] = "done"
                overwrite(line=row, lineNumber=lineNum, filename=filename)
                return

        print("You aren't helping anyone!")

def helpStudent(TA, filename):
    """
    Find the next available student and mark them as being helped
    Also update the comment to the TA's UTLN
    Also if the TA is already helping someone, ask to remove that person
    from the queue
    """

    with open(filename, "r") as queue:
        reader = csv.reader(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            if row[1] == TA and row[2] == "helping":
                print("You're already helping someone! Do you want to remove them from the queue? (y/n)")
                if input() == "y":
                    doneStudent(TA= TA, filename= filename)
                else:
                    print("Okay, I won't remove them. Please finish with them before helping another student.")
                    return

    with open(filename, "r") as queue:
        reader = csv.reader(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            if row[2] != "helping" and row[2] != "done" \
                                    and row[2] != "missing":
                printStudent(student= row)
                lineNum = reader.line_num
                row[1] = TA
                row[2] = "helping"
                overwrite(line=row, lineNumber=lineNum, filename=filename)
                return
        
    print("no one needs help!")

def updateLine(lineNumber, comment, location, filename):

    with open(filename, "r") as queue:
        reader = csv.reader(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)

        lineNumber = int(lineNumber)
        i = 0
        for row in (reader):
            i += 1
            if i == lineNumber:
                studentName = row[0]
                timestamp = row[3]
                line = [studentName, comment, location, timestamp]
                overwrite(line=line, lineNumber=lineNumber, filename=filename)

def clearQueue(filename):
    data = []

    with SoftFileLock(f"{filename}.lock"):

        with open(filename, "r") as queue:
            reader = csv.reader(queue, delimiter=" ", quotechar="|", 
                                quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                data.append(row)

        with open(filename, "w") as queue:
            writer = csv.writer(queue, delimiter=" ", quotechar="|", 
                                quoting=csv.QUOTE_MINIMAL)

            for row in data:
                if row[2] != "done":
                    writer.writerow(row)

def removeLine(name, filename):
    "Remove a student from the queue entirely"
    data = []
    
    with SoftFileLock(f"{filename}.lock"):

        with open(filename, "r") as queue:
            reader = csv.reader(queue, delimiter=" ", quotechar="|", 
                                quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                data.append(row)

        with open(filename, "w") as queue:
            writer = csv.writer(queue, delimiter=" ", quotechar="|", 
                                quoting=csv.QUOTE_MINIMAL)

            for row in data:
                if not (row[0] == name and row[2] != "helping" 
                                    and row[2] != "done"):
                    writer.writerow(row)

def printQueue(filename, key):
    """
    Print the entire queue with nice formatting
    """

    with open(filename, "r") as queue:
        reader = csv.reader(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)
        
        blankRow = ["", "", "", ""]
        i = 0
        for row in reader:
            digit = str(i)
            chaser = " " * (3 - len(digit))
            print(digit, end=chaser)
            i += 1
            if key == "d":
                if row[2] == "done":
                    printRow(row, "cyan")
                elif row[2] == "helping":
                    printRow(blankRow, "green")
                elif row[2] == "missing":
                    printRow(blankRow, "yellow")
                else:
                    printRow(blankRow, "red")
            elif key == "h":
                if row[2] == "done":
                    printRow(blankRow, "cyan")
                elif row[2] == "helping":
                    printRow(row, "green")
                elif row[2] == "missing":
                    printRow(blankRow, "yellow")
                else:
                    printRow(blankRow, "red")
            elif key == "n":
                if row[2] == "done":
                    printRow(blankRow, "cyan")
                elif row[2] == "helping":
                    printRow(blankRow, "green")
                elif row[2] == "missing":
                    printRow(blankRow, "yellow")
                else:
                    printRow(row, "red")
            elif key == "m":
                if row[2] == "done":
                    printRow(blankRow, "cyan")
                elif row[2] == "helping":
                    printRow(blankRow, "green")
                elif row[2] == "missing":
                    printRow(row, "yellow")
                else:
                    printRow(blankRow, "red")
            else:
                if row[2] == "done":
                    printRow(row, "cyan")
                elif row[2] == "helping":
                    printRow(row, "green")
                elif row[2] == "missing":
                    printRow(row, "yellow")
                else:
                    printRow(row, "red")

def printRow(row, color):
    print(colored(f"{(row[0]):>10.10}", color), end="|")
    print(colored(f"{row[1]:<40.40}", color), end="|")
    print(colored(f"{row[2]:<10.10}", color), end="|")
    print(colored(f"{row[3]:<20.20}", color))

def printStudent(student):
    """
    Print a student nicely
    """


    print(f" Student: {student[0]}")
    print(f" Comment: {student[1]}")
    print(f"Location: {student[2]}")

class taLoop(cmd.Cmd):
    """
    Run the command loop from the TA's perspective
    """

    prompt = "-> "
    intro = "Welcome to the queue manager!"

    def __init__(self, TA, file):
        super(taLoop, self).__init__()
        self.name = TA
        self.file = file

    def do_next(self, line):
        "Help the next student in the queue"
        helpStudent(TA=self.name, filename=self.file)

    def do_done(self, line):
        "Mark the current student as done"
        doneStudent(TA=self.name, filename=self.file)

    def do_print(self, line):
        "Print the status of the queue \nusage: print [a n h m d] \n a = all (default), n = need help, h = helping, m = missing, d = done"

        if len(line) == 1:
            printQueue(filename=self.file, key=line[0])
        else:
            printQueue(filename=self.file, key="a")

    def do_add(self, line):
        "Add a student to the queue \nusage: add [name, comment, location]"
        if len(line) == 3:
            addToQueue(name=line[0], comment=line[1], 
                       location=line[2], filename=self.file)
        else:
            student  = input(" student: ")
            comment  = input(" comment: ")
            location = input("location: ")
            addToQueue(name=student, comment=comment, 
                       location=location, filename=self.file)

    def do_update(self, line):
        "Update a student's record in the queue \nusage: update <record number>"
        if len(line) == 1:
            comment  = input(" comment: ")
            location = input("location: ")
            updateLine(lineNumber=line[0], comment=comment, 
                       location=location, filename=self.file)
        else:
            print("usage: update <record number>")
    
    def do_remove(self, line):
        "Remove a student from the queue \nusage: remove <utln>"

        if (len(line) == 1):
            removeLine(name=line[0], filename=self.file)
        else:
            utln = input("utln: ")
            removeLine(name=utln, filename=self.file)

    def do_clear(self, line):
        "Remove all completed records from queue"
        confirmation = input("Are you sure you want to remove all completed records? (y/n) ")

        if confirmation == "y":
            clearQueue(self.file);

    def do_quit(self, line):
        "End the program"
        print("Thank you for working the queue!")
        return True

    def do_EOF(self, line):
        "End the program"
        print("\nThank you for working the queue!")
        return True

class studentLoop(cmd.Cmd):
    """
    Run the command loop from the student's perspective
    """

    prompt = "-> "
    intro = "Welcome to the queue manager!"

    def __init__(self, name, file):
        super(studentLoop, self).__init__()
        self.name = name
        self.file = file

    def do_print(self, line):
        "Print the status of the queue \nusage: print [a n h m d] \n a = all (default), n = need help, h = helping, m = missing, d = done"

        if len(line) == 1:
            printQueue(filename=self.file, key=line[0])
        else:
            printQueue(filename=self.file, key="a")

    def do_add(self, line):
        "Add yourself to the queue \nusage: add [comment location]"

        if len(line) == 2:
            addToQueue(name=self.name, comment=line[0], 
                       location=line[1], filename=self.file)
        else:
            comment  = input(" comment: ")
            location = input("location: ")
            addToQueue(name=self.name, comment=comment,
                       location=location, filename=self.file)
    
    def do_remove(self, line):
        "Remove yourself from the queue"
        removeLine(self.name)

    def do_quit(self, line):
        "End the program"
        print("Thank you for using the queue!")
        return True

    def do_EOF(self, line):
        "End the program"
        print("\nThank you for using the queue!")
        return True
