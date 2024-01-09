import bcrypt


def get_hashed_salted_password(password: str) -> str:
    """Return hashed password using `bcrypt`."""
    hashed_password = bcrypt.hashpw(
        password=password.encode("utf-8"), salt=bcrypt.gensalt()
    )
    r = hashed_password.decode("utf-8")
    return r


def is_psw_correct(password: str, hashed_password: str) -> bool:
    """Verify password against hashed password using `bcrypt`."""
    r = bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )
    return r
