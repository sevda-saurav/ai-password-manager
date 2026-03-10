import re

def password_strength(password):

    score = 0

    if len(password) >= 12:
        score += 1

    if re.search("[A-Z]", password):
        score += 1

    if re.search("[0-9]", password):
        score += 1

    if re.search("[!@#$%^&*]", password):
        score += 1

    if score == 4:
        return "Very Strong"
    elif score == 3:
        return "Strong"
    elif score == 2:
        return "Medium"
    else:
        return "Weak"