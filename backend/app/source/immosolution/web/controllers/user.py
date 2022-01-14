from core.security import *
from dao.dao_user import *

def get_username_by_name(username: str, token_info):
    if is_admin(token_info):
        try:
            return get_username_by_name_dao(username)
        except:
            return "An error has ocurred"
    else:
        return "Wrong credentials", 401
        
def update_user_access_token(username: str, token: str, token_info):
    if is_admin(token_info):
        try:
            return dao_update_user_access_token(username, token)
        except: 
            return "An error has ocurred"
    else:
        return "Wrong credentials", 401