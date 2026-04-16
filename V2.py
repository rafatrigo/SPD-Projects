import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

# ==========================================
# 1. CARREGAMENTO E ENGENHARIA DE RECURSOS
# ==========================================
df = pd.read_csv('datasetFinal.csv')

# Função para separar o Tipo de Execução do Número de Workers (N)
def extrair_cenario(cenario_str):
    cenario_str = str(cenario_str).strip( )
    
    # Se for sequencial, o tipo é "Sequencial" e vamos considerar N = 1
    if "Sequencial" in cenario_str:
        return "Sequencial", 1
    
    # Extrai os números da string (ex: "4 Processos" -> 4)
    numeros = re.findall(r'\d+', cenario_str)
    n = int(numeros[0]) if numeros else 1
    
    if "Processos" in cenario_str:
        return "Processos", n
    elif "Threads" in cenario_str:
        return "Threads", n
    else:
        return "Desconhecido", n

# Aplicando a função para criar duas novas colunas
df[['Tipo_Execucao', 'N_Workers']] = df.apply(
    lambda row: pd.Series(extrair_cenario(row['Cenario'])), axis=1
)

# Configuração visual
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("--- Dados Transformados (Amostra) ---")
print(df[['Cenario', 'Tipo_Execucao', 'N_Workers', 'Tempo_s']].head(10))

# ==========================================
# 2. NOVOS PLOTS FOCADOS EM PARALELISMO
# ==========================================

# Plot 1: Curva de Escalabilidade (Tempo vs N Workers)
# O gráfico mais importante para avaliar paralelismo!
plt.figure(figsize=(10, 6))
# Filtramos fora o Sequencial para a linha, mas podemos adicioná-lo como uma linha base
df_paralelo = df[df['Tipo_Execucao'] != 'Sequencial']

sns.lineplot(
    data=df_paralelo, 
    x='N_Workers', 
    y='Tempo_s', 
    hue='Tipo_Execucao', 
    marker='o',
    errorbar='sd', # Mostra a variação
    linewidth=2.5,
    markersize=8
)

# Adicionando uma linha horizontal para a média do tempo Sequencial (Baseline)
tempo_sequencial_medio = df[df['Tipo_Execucao'] == 'Sequencial']['Tempo_s'].mean()
if not pd.isna(tempo_sequencial_medio):
    plt.axhline(y=tempo_sequencial_medio, color='r', linestyle='--', label=f'Sequencial (Média: {tempo_sequencial_medio:.2f}s)')

plt.title('Curva de Escalabilidade: Tempo de Execução vs Quantidade de Workers', fontsize=14)
plt.xlabel('Número de Workers (N)')
plt.ylabel('Tempo Médio (segundos)')
plt.xticks([2, 4, 8, 16, 32]) # Ajuste os ticks de acordo com os 'N' que você testou
plt.legend(title="Tipo de Execução")
plt.tight_layout()
plt.show()

# Plot 2: Comparação de Desempenho por Processador (Barras Agrupadas)
# Compara como cada Processador lida com Threads vs Processos no N máximo testado
n_maximo = df_paralelo['N_Workers'].max()
df_max_workers = df[(df['N_Workers'] == n_maximo) | (df['Tipo_Execucao'] == 'Sequencial')]

plt.figure(figsize=(12, 6))
sns.barplot(
    data=df_max_workers, 
    x='Processador', 
    y='Tempo_s', 
    hue='Tipo_Execucao',
    palette='Set2'
)
plt.title(f'Comparação de Tempo por Processador (Sequencial vs {n_maximo} Threads/Processos)', fontsize=14)
plt.xlabel('Processador')
plt.ylabel('Tempo Médio (segundos)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Plot 3: Eficiência do SO lidando com Threads vs Processos
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df_paralelo, 
    x='Sistema_Operacional', 
    y='Tempo_s', 
    hue='Tipo_Execucao',
    palette='mako'
)
plt.title('Desempenho de Threads vs Processos por Sistema Operacional', fontsize=14)
plt.xlabel('Sistema Operacional')
plt.ylabel('Tempo de Execução (segundos)')
plt.tight_layout()
plt.show()