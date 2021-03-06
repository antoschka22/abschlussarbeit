from .db import get_db_cursor

def get_user_by_credentials(credentials):
    with get_db_cursor() as cursor:
        cursor.execute("select * from users where username = %s and password = %s", [credentials['username'], credentials['password']])
        return cursor.fetchone()
    
def get_username_by_name_dao(username: str):
    with get_db_cursor() as cursor:
        cursor.execute("select * from users where username = %s", [username])
        return cursor.fetchone()
    
def dao_update_user(username: str, token):
    with get_db_cursor() as cursor:
        cursor.execute("""
                    UPDATE users SET username=%s, password=%s, instagram_at=%s where username=%s returning *
                       """, [token['username'], token['password'], token['instagram_at'], username])
        return cursor.fetchone()
    
def dao_update_user_access_token(username: str, token: str):
    with get_db_cursor() as cursor:
        cursor.execute("""
                    UPDATE users SET instagram_at=%s where username=%s returning instagram_at
                       """, [token['token'], username])
        return cursor.fetchone()