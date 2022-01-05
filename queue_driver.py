import sys
from queue_brain import TALoop, StudentLoop


def isTA():  # pylint: disable=invalid-name
    "Determines if the user is a TA. \nReturns True if so, False if not."
    course = f"ta{sys.argv[2]}"
    for i in range(3, len(sys.argv)):
        if course == sys.argv[i]:
            return True

    return False


def main():

    file = f"comp{sys.argv[2]}queue.csv"

    if isTA():
        TALoop(TA=sys.argv[1], file=file).cmdloop()
    else:
        StudentLoop(name=sys.argv[1], file=file).cmdloop()


if __name__ == "__main__":
    main()
