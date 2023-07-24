import re

def check_email(email):
    
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'     

    return True if re.search(regex,email) else False