def flag_conv(val: int, flag_dict: dict) -> list[str]:
    return [name for name, bit in flag_dict.items() if isinstance(bit, int) and val & bit]
