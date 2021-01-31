from nlp import Entity

userStatuses = []


def statusChange(newStatus, userName):
    response = ''

    #userStatuses[userName] = newStatus

    response = userName + " is now " + newStatus
    return response

def getUserStatuses():
    return str(userStatuses)
