def validate_bool(my_bool):
    if isinstance(my_bool, bool):
        return
    if my_bool.lower() not in ("true", "false"):
        raise ValueError
