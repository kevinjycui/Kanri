from nlp import Entity

userStatuses = {}


def statusChange(newStatus, userName):
    response = ''
    userStatuses[userName] = newStatus

    if newStatus == "In a meeting":
        response = userName + " is now in a meeting."
    else:
        response = userName + " is now " + newStatus
    return response

def getUserStatuses():
    return str(userStatuses)
