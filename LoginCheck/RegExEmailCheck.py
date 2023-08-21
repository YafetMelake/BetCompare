'''Function that checks to make sure email is valid using regular expression to verify 
    that there is an @ sign a . and also a 3 letter ending fo the domain extension'''

import re

def check_email(email):
    
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'     

    return True if re.search(regex,email) else False