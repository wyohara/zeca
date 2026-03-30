import time
import psutil
from functools import wraps
import os

def decorator_tempo(func):
    '''
    whrapper que verifica o tempo de processamento do codigo
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()
        tempo = fim - inicio
        print(f"⏱️  {func.__name__} executou em {tempo:.4f} segundos")
        return resultado
    return wrapper

def decorator_tempo_cpu(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.process_time()  # Tempo de CPU do processo
        resultado = func(*args, **kwargs)
        fim = time.process_time()
        tempo_cpu = fim - inicio
        print(f"⚙️  {func.__name__} usou {tempo_cpu:.4f} segundos de CPU")
        return resultado
    return wrapper

def decorator_uso_ram(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        
        # Coleta memória antes da execução
        mem_antes = process.memory_info()
        rss_antes = mem_antes.rss / 1024 / 1024  # MB
        vms_antes = mem_antes.vms / 1024 / 1024  # MB
        
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()
        
        # Coleta memória depois da execução
        mem_depois = process.memory_info()
        rss_depois = mem_depois.rss / 1024 / 1024  # MB
        vms_depois = mem_depois.vms / 1024 / 1024  # MB
        
        tempo = fim - inicio
        diferenca_rss = rss_depois - rss_antes
        diferenca_vms = vms_depois - vms_antes
        
        print(f"\n💾 MEMÓRIA RAM - {func.__name__}:")
        print(f"   ⏱️  Tempo: {tempo:.4f}s")
        print(f"   📊 RSS (RAM física): {rss_depois:.2f} MB")
        print(f"   📊 VMS (virtual): {vms_depois:.2f} MB")
        print(f"   📈 Variação RSS: {diferenca_rss:+.2f} MB")
        print(f"   📈 Variação VMS: {diferenca_vms:+.2f} MB")
        
        return resultado
    return wrapper
