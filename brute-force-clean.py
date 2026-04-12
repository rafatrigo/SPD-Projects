import hashlib

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