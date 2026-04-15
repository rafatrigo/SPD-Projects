import numpy as np
import argparse
from datetime import datetime
import hashlib
import time

import os_info
import hash_finder
import write_results

FILE_NAME="resultados_benchmark.csv"


def main(hash_target, max_entries, num_threads=1, num_tests=30, result_filename=FILE_NAME, sleep=300):

    #inicializa as listas
    resultados_finais = []
    tempo_execucao = []

    # system info
    info_hw = os_info.obter_info_sistema()
    data_teste = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    for test in range(3):
        if test == 0:
            mode = 0 # sequential
            type = 0
        elif test == 1:
            mode = 1 # parallel
            type = 0 # process
        else:
            mode = 1 # parallel
            type = 1 # thread

        print("Sleeping...")
        time.sleep(sleep)

        for idx in range(num_tests):
            inicio_t = time.time()

            # Pass the variables to your main function
            result = hash_finder.main(hash_target, max_entries, num_threads, type, mode)
            
            fim_t = time.time()
            t = fim_t - inicio_t
            tempo_execucao.append(t)

            status = "Encontrado" if result is not None else "Não Encontrado"
            media = np.mean(tempo_execucao)

            if mode == 0:
                nome = "Sequencial"
            elif type == 1:
                nome = f"{num_threads} Threads"
            else:
                nome = f"{num_threads} Processos"

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

            print(f"Execução {idx + 1}/{num_tests}: Tempo = {round(t, 4)}s | Resultado = {result}")
    
    write_results.to_csv(result_filename, resultados_finais)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MD5 Brute-Force Script")

    # Add the arguments you want to accept
    parser.add_argument(
        "-n", "--number", 
        required=True, 
        type=str, 
        help="The base number to generate the target hash")
    
    parser.add_argument(
        "-m", "--max_entries", 
        required=True, 
        type=int, 
        help="The maximum search limit")
    
    parser.add_argument(
        "-t", "--threads", 
        type=int, 
        default=1, 
        help="Number of threads/processes (Default: 1)")
    
    parser.add_argument(
        "--num_tests", 
        type=int, 
        default=30, 
        help="Number of tests in each scenario")
    
    parser.add_argument(
        "-f", "--filename", 
        type=str,
        default=FILE_NAME,
        help="The result csv file name")
    
    parser.add_argument(
        "--sleep", 
        type=int, 
        default=300, 
        help="Waiting time between scenarios")
    

    
    args = parser.parse_args()

    # create target hash based on number
    num_bytes = args.number.encode('utf-8')
    hash_obj = hashlib.md5(num_bytes)
    hash_target = hash_obj.hexdigest()

    main(hash_target, args.max_entries, args.threads, args.num_tests, args.filename, args.sleep)

    print("Completed!")