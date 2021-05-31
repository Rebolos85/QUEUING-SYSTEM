import re


def isValidEmail(email: str) -> bool:
    if re.fullmatch(r"\d{11}\@my\.xu\.edu\.ph", email):
        return True
    else:
        return False


def isValidSchoolId(schoolId: str) -> bool:
    if re.fullmatch(r"\d{11}", schoolId):

        return True
    else:
        return False


def isValidMonthInput(months: str) -> bool:
    if re.search(
            '(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)',
            months):

        return True
    else:
        return False


def isValidUsernameInput(usernameInput):
    return len(usernameInput) > 6


def isValidDayInput(dayInput) -> bool:
    pattern = re.compile(r'"\d+"')

    if pattern.search(pattern, dayInput):
        return True
    else:
        return False


def isValidFirstNameAndLastname(completeName: str) -> bool:
    if re.fullmatch(r'[a-zA-Z]+', completeName):
        return True
    else:
        return False


def isValidSuffixes(firstname):
    if re.search(r'([A-Z]+ (?:IX|IV|V?I{0,3})$)+', firstname):
        return True
    else:
        return False


def isValidGmailAccount(gmailAccount: str) -> bool:
    if re.fullmatch("^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$", gmailAccount):
        return True
    else:
        return False


def isValidCompleteName(completeName: str) -> bool:
    if re.search(r'[A-Za-z]{2,25}( [A-Za-z]{2,25})?', completeName):
        return True
    else:
        return False
