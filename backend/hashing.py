from argon2 import PasswordHasher

hsh = PasswordHasher()


def hashing_password(password: str):
    return hsh.hash(password)


def verify_password(hashed_password: str, password: str):
    try:
        return hsh.verify(hashed_password, password)
    except:
        return False

# print(verify_password(
#     hashed_PASSWORD="***REMOVED***"
# ))
