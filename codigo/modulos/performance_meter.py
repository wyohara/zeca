import time
from functools import wraps

def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()
        tempo = fim - inicio
        print(f"⏱️  {func.__name__} executou em {tempo:.4f} segundos")
        return resultado
    return wrapper