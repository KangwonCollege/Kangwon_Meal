def find_enum(cls, key: str):
    enum_val = [i for i in list(cls) if i.value == key]
    if len(enum_val) == 0:
        return key
    return enum_val[0]
