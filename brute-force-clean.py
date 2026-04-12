import hashlib
import threading
import multiprocessing

# Busca por força bruta
# Tenta encontrar o número que gera o hash alvo de forma sequencial
"""
def encontrar_numero_por_hash(hash_alvo, entrada_max):
    for i in range(1,entrada_max+1):
        # Converte o número em string e depois em bytes para gerar o hash
        candidato = str(i).encode()
        hash_gerado = hashlib.md5(candidato).hexdigest()

        if hash_gerado == hash_alvo:
            return i
    return None
"""

RESULT = None

def hash_worker(hash_target, start, end, stop_event):
    global RESULT

    for i in range(start,end):
        if stop_event.is_set():
            return
        
        candidato = str(i).encode()
        hash_gerado = hashlib.md5(candidato).hexdigest()
    
        if hash_gerado == hash_target:
            RESULT = i
            stop_event.set() # tell the other tastks to stop
            return
    return None

# type 1 = threading
# type 0 = multiprocessing
def main(hash_target, max_entries, num_threads=1, type=1):
    global RESULT
    RESULT = None

    stop_event = threading.Event() if type == 1 else multiprocessing.Event()
     
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
            "args": (hash_target, start, end, stop_event)
        }

        t = threading.Thread(**parameters) if type == 1 else multiprocessing.Process(**parameters)
        tasks.append(t)
        t.start()

    for t in tasks:
        t.join()

    return RESULT

if __name__ == "__main__":

    num = str(25)
    num_bytes = num.encode('utf-8')
    hash_obj = hashlib.md5(num_bytes)
    hash_target = hash_obj.hexdigest()

    result = main(hash_target, 100, 3, 0)

    print(f"result: {result}")