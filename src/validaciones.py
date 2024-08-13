def validar_codigo(codigo: str) -> bool:
    """(str) -> bool
    Vaolida si òdigo (si es nemèrico y de longitud 8).
    Return True 

    >>> valida_codigo(325817)
    true
    >>> valida_codigo(3456789)
    false
    """
    return (codigo.isnumeric() and len(codigo) == 6)


def validar_nombre(nombre: str) -> bool:
    """(str) -> bool
    Valda el nombre (si es un texto sin espacios en blanco de entre 1 y 30 caracteres).
    Return True 
    
    >>> valida_nombre('Lògica')
    true
    >>> valida_nombre('')
    false
    """
    nombre = nombre.strip()
    return (len(nombre) > 0 and len(nombre) <= 30)

# Valida que los crèditos estèn entre 1 y 9.
def validar_creditos(creditos: int) -> bool:
    """(str) -> bool
    Valida que los crèditos estèn entre 1 y 9.
    Return True.
    
    >>> valida_nombre(7)
    true
    >>> valida_nombre(12)
    false
    """
    creditos_texto = str(creditos)
    if creditos_texto.isnumeric():
        return (creditos >= 1 and creditos <= 9)
    else:
        return False