import hashlib
import argparse
import threading
import multiprocessing
import time
import platform
import psutil
import csv
import os
import numpy as np
from datetime import datetime

class ThreadValue:
    def __init__(self, initial_value):
        self.value = initial_value

def obter_info_sistema():
    so_tipo = platform.system()
    so_nome_completo = ""

    if so_tipo == "Linux":
        # segundo o gemini o freedesktop_os_release é melhor para retornar detalhes da distro (ex: Ubuntu, 22.04)
        try:
            info =platform.freedesktop_os_release()
            so_nome_completo = f"{info['NAME']} {info.get('VERSION_ID', '')}"
        except:
            so_nome_completo = f"Linux {platform.release()}"
    elif so_tipo == "Windows":
        so_nome_completo = f"Windows {platform.release()} (v{platform.version()})"
        
    else:
        so_nome_completo = f"{so_tipo} {platform.release()}"

    try:
        import cpuinfo
        cpu = cpuinfo.get_cpu_info()['brand_raw']
    except:
        cpu = platform.processor()

    return {
        "so_versao": so_nome_completo,
        "processador": cpu,
        "cores_fisicos": psutil.cpu_count(logical=False),
        "threads_logicos": psutil.cpu_count(logical=True),
        "ram_gb": round(psutil.virtual_memory().total / (1024**3), 2)
    }

# Busca por força bruta
# Tenta encontrar o número que gera o hash alvo de forma sequencial
def encontrar_numero_por_hash(hash_alvo, entrada_max):
    for i in range(1,entrada_max+1):
        # Converte o número em string e depois em bytes para gerar o hash
        candidato = str(i).encode()
        hash_gerado = hashlib.md5(candidato).hexdigest()

        if hash_gerado == hash_alvo:
            return i
    return None

def hash_worker(hash_target, start, end, stop_event, shared_result):

    for i in range(start,end):
        if stop_event.is_set():
            return
        
        candidato = str(i).encode()
        hash_gerado = hashlib.md5(candidato).hexdigest()
    
        if hash_gerado == hash_target:
            shared_result.value = i
            stop_event.set() # tell the other tastks to stop
            return
    return None

# type 1 = threading
# type 0 = multiprocessing
def main(hash_target, max_entries, num_threads=1, type=1):

    if type == 1:
        worker = threading.Thread
        stop_event = threading.Event()
        shared_result = ThreadValue(-1)
    else:
        worker = multiprocessing.Process
        stop_event = multiprocessing.Event()
        shared_result = multiprocessing.Value('i', -1)
     
    chunk_size = max_entries // num_threads
    tasks = []

    for i in range(num_threads):
        start = i * chunk_size

        if i == num_threads - 1:
            end = max_entries
        else:
            end = start + chunk_size

        parameters = {
            "target": hash_worker,
            "args": (hash_target, start, end, stop_event, shared_result)
        }

        t = worker(**parameters)
        tasks.append(t)
        t.start()

    for t in tasks:
        t.join()

    return shared_result.value if shared_result.value != -1 else None



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="MD5 Brute-Force Script")

    # Add the arguments you want to accept
    parser.add_argument(
        "-n", "--number", 
        required=True, 
        type=str, 
        help="The base number to generate the target hash")
    
    parser.add_argument(
        "--max_entries", 
        required=True, 
        type=int, 
        help="The maximum search limit")
    
    parser.add_argument("--threads", 
        type=int, 
        default=1, 
        help="Number of threads/processes (Default: 1)")
    
    parser.add_argument("--type", 
        type=int, 
        choices=[0, 1], 
        default=1, 
        help="1 for Threads, 0 for Processes (Default: 1)")
    parser.add_argument("--runs", 
        type=int, 
        default=1, 
        help="Número de execuções do teste")

    args = parser.parse_args()

    # Replace fixed values with variables from 'args'
    num_bytes = args.number.encode('utf-8')
    hash_obj = hashlib.md5(num_bytes)
    hash_target = hash_obj.hexdigest()

    #Primeiro coleto todas informações do sistema
    info_hw = obter_info_sistema()
    data_teste = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    modo_str = modo_str = 'Threads' if args.type == 1 else 'Processes'
    nome = f"{modo_str} - {args.threads} workers"

    #inicializa as listas
    resultados_finais = []
    tempo_execucao = []

    print(f"\n--- Starting Search ---")
    print(f"Target: {args.number} -> Hash: {hash_target}")
    print(f"Mode: {'Threads' if args.type == 1 else 'Processes'} | Workers: {args.threads}")
    print(f"Search limit: {args.max_entries}")
    #Confere isso aqui @Rafael
    print(f"Execuções programadas: {args.runs}")
    print(f"-----------------------\n")

    
    for idx in range(args.runs):
        inicio_t = time.time()

        # Pass the variables to your main function
        result = main(hash_target, args.max_entries, args.threads, args.type)
        
        fim_t = time.time()
        t = fim_t - inicio_t
        tempo_execucao.append(t)

        status = "Encontrado" if result is not None else "Não Encontrado"
        media = np.mean(tempo_execucao)

        resultados_finais.append({
            "Data": data_teste,
            "Sistema_Operacional": info_hw['so_versao'],
            "Processador": info_hw['processador'],
            "Cores": info_hw['cores_fisicos'],
            "Threads": info_hw['threads_logicos'],
            "RAM_GB": info_hw['ram_gb'],
            "Cenario": nome,
            "N_Execucao": idx + 1,
            "Tempo_s": round(t, 4),
            "Status": status,
            "Media_Cenario": round(media, 4)
        })

        print(f"Execução {idx + 1}/{args.runs}: Tempo = {round(t, 4)}s | Resultado = {result}")
    
    nome_arquivo_csv = "resultados_benchmark.csv"
    print(f"\n[+] Dados salvos com sucesso no arquivo '{nome_arquivo_csv}'.")
    
    

    print(f"\nFinal result: {result}")