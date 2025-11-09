# src/domain/value_objects/enums.py
from enum import Enum
import string


class EstadoAnalisis(str, Enum):
    PENDIENTE = "pendiente"
    COMPLETADO = "completado"
    ERROR = "error"


# Genera una lista de todos los caracteres permitidos
caracteres_permitidos = list(string.ascii_lowercase) + list(string.ascii_uppercase) + list(string.digits)


# Enum para letras permitidas
# Usamos una definición explícita que es compatible con Python 3.12 y FastAPI/Pydantic
class LetraPermitida(str, Enum):
    """
    Versión explícita con todos los caracteres definidos.
    Más verbosa pero más clara y con mejor soporte de IDE.
    """
    # Minúsculas
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd'
    e = 'e'
    f = 'f'
    g = 'g'
    h = 'h'
    i = 'i'
    j = 'j'
    k = 'k'
    l = 'l'
    m = 'm'
    n = 'n'
    o = 'o'
    p = 'p'
    q = 'q'
    r = 'r'
    s = 's'
    t = 't'
    u = 'u'
    v = 'v'
    w = 'w'
    x = 'x'
    y = 'y'
    z = 'z'
    
    # Mayúsculas
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    H = 'H'
    I = 'I'
    J = 'J'
    K = 'K'
    L = 'L'
    M = 'M'
    N = 'N'
    O = 'O'
    P = 'P'
    Q = 'Q'
    R = 'R'
    S = 'S'
    T = 'T'
    U = 'U'
    V = 'V'
    W = 'W'
    X = 'X'
    Y = 'Y'
    Z = 'Z'
    
    # Números
    ZERO = '0'
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'


# Función auxiliar para validación
def es_letra_valida(caracter: str) -> bool:
    """
    Valida si un caracter está en el conjunto permitido.
    
    Args:
        caracter: String de un solo caracter a validar
        
    Returns:
        True si el caracter es válido, False en caso contrario
    """
    if len(caracter) != 1:
        return False
    return caracter in caracteres_permitidos


# Si necesitas obtener todos los valores permitidos:
def obtener_caracteres_validos() -> list[str]:
    """Retorna la lista de todos los caracteres válidos"""
    return caracteres_permitidos.copy()