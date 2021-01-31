def sendStatusChangeMessage(newStatus, userName):
    response = ''

    if newStatus == "In a meeting":
        response = userName + " is now in a meeting."
    else:
        response = userName + " is now " + newStatus
    return response

