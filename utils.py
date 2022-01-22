def read_int32(val):
    """
    Recibe bytes y los convierte a entero
    """
    return int.from_bytes(val,"little")
