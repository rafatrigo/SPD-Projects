import hashlib
import time

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

# Hash e número de entrada correspondente
# Teste vc mesmo outras chaves hash alvos criadas em: https://www.md5hashgenerator.com/
ALVO = "d1ca3aaf52b41acd68ebb3bf69079bd1" #Corresponde ao número "10000000"
#ALVO = "283f42764da6dba2522412916b031080" #Corresponde ao número "9999999"
#ALVO = "f0898af949a373e72a4f6a34b4de9090" #Corresponde ao número "7654321"

LIMITE = 10000000

print(f"Iniciando busca sequencial pelo hash: {ALVO}...")
    
inicio = time.time()
resultado = encontrar_numero_por_hash(ALVO, LIMITE)
fim = time.time()
    
tempo_total = fim - inicio

if resultado is not None:
    print(f"Sucesso! A senha encontrada foi: {resultado}")
else:
    print("Senha não encontrada no intervalo.")
        
print(f"Tempo total de execução (Sequencial): {tempo_total:.4f} segundos")
