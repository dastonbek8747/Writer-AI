from argon2 import PasswordHasher

hsh = PasswordHasher()


def hashing_password(password: str):
    return hsh.hash(password)


def verify_password(hashed_password: str, password: str):
    try:
        return hsh.verify(hashed_password, password)
    except:
        return False

# print(hashing_password("daston8747"))
# print(verify_password(
#     hashed_password="$argon2id$v=19$m=65536,t=3,p=4$Q6JCxDjLrR5uL4rg8XJlTQ$qZ0mvd7QFMf7LcAOlktJXR4lFwC5X/eOiwBDTyjiABE"
#     , password="daston8747"
# ))
