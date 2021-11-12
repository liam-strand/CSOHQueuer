import sys
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

def removeFromQueue(TA, filename):
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
                    removeFromQueue(TA= TA, filename= filename)
                else:
                    print("Okay, I won't remove them. Please finish with them before helping another student.")
                    return

    with open(filename, "r") as queue:
        reader = csv.reader(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            if row[2] != "helping" and row[2] != "done" and row[2] != "missing":
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

    with open(filename, "r") as queue:
        reader = csv.reader(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            data.append(row)

    with open(filename, "w") as queue, SoftFileLock(f"{filename}.lock"):
        writer = csv.writer(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)

        for row in data:
            if row[2] != "done":
                writer.writerow(row)

def printQueue(filename):
    """
    Print the entire queue with nice formatting
    """

    print(f"{filename}:")
    print("-----------------")

    with open(filename, "r") as queue:
        reader = csv.reader(queue, delimiter=" ", quotechar="|", 
                            quoting=csv.QUOTE_MINIMAL)

        for row in reader:
            if row[2] == "done":
                print(colored(row, "cyan"))
            elif row[2] == "helping":
                print(colored(row, "green"))
            elif row[2] == "missing":
                print(colored(row, "yellow"))
            else:
                print(colored(row, "red"))
    
    print("-----------------")

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
        removeFromQueue(TA=self.name, filename=self.file)

    def do_print(self, line):
        "Print the status of the queue"
        printQueue(filename=self.file)

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
            
    def do_clear(self, line):
        confirmation = input("Are you sure you want to remove all completed records? (y/n) ")

        if confirmation == "y":
            clearQueue(self.file);

    def do_quit(self, line):
        "End the program"
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
        "Print the status of the queue"
        printQueue(filename=self.file)

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
    
    def do_quit(self, line):
        "End the program"
        return True
