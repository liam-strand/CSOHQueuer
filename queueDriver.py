import sys
from queueBrain import taLoop, studentLoop

def isTA():
    course = sys.argv[2]
    for i in range(3, len(sys.argv)):
        if course in sys.argv[i]:
            return True

    return False

def main():

    file = f"comp{sys.argv[2]}queue.csv"

    if isTA():
        taLoop(TA=sys.argv[1], file=file).cmdloop()
    else:
        studentLoop(name=sys.argv[1], file=file).cmdloop()

if __name__ == "__main__":
    main()

