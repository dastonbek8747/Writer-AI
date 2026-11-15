from argon2 import PasswordHasher

hsh = PasswordHasher()


def hashing_password(password: str):
    return hsh.hash(password)


def verify_password(hashed_password: str, password: str):
    try:
        return hsh.verify(hashed_password, password)
    except:
        return False

# Misol (haqiqiy qiymatlarni .env faylida saqlang):
# print(hashing_password("your_password"))
# print(verify_password(hashed_password="<hash>", password="your_password"))
