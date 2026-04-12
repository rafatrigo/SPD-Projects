import hashlib
import argparse
import threading
import multiprocessing

class ThreadValue:
    def __init__(self, initial_value):
        self.value = initial_value

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

    args = parser.parse_args()

    # Replace fixed values with variables from 'args'
    num_bytes = args.number.encode('utf-8')
    hash_obj = hashlib.md5(num_bytes)
    hash_target = hash_obj.hexdigest()

    print(f"\n--- Starting Search ---")
    print(f"Target: {args.number} -> Hash: {hash_target}")
    print(f"Mode: {'Threads' if args.type == 1 else 'Processes'} | Workers: {args.threads}")
    print(f"Search limit: {args.max_entries}")
    print(f"-----------------------\n")

    # Pass the variables to your main function
    result = main(hash_target, args.max_entries, args.threads, args.type)

    print(f"\nFinal result: {result}")