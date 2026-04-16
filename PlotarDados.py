import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

# ==========================================
# 1. CARREGAMENTO E ENGENHARIA DE RECURSOS
# ==========================================
df = pd.read_csv('datasetFinal.csv')

def extrair_cenario(cenario_str):
    cenario_str = str(cenario_str).strip()
    if "Sequencial" in cenario_str:
        return "Sequencial", 1
    numeros = re.findall(r'\d+', cenario_str)
    n = int(numeros[0]) if numeros else 1
    
    if "Processos" in cenario_str:
        return "Processos", n
    elif "Threads" in cenario_str:
        return "Threads", n
    else:
        return "Desconhecido", n

df[['Tipo_Execucao', 'N_Workers']] = df.apply(
    lambda row: pd.Series(extrair_cenario(row['Cenario'])), axis=1
)
# ==========================================
# 2. REMOÇÃO DE OUTLIERS (Método IQR seguro com Transform)
# ==========================================
# Definimos as colunas que formam os nossos grupos
grupos = ['Cenario', 'Sistema_Operacional', 'Status']

# Calculamos os quartis usando transform, que retorna os valores alinhados ao dataframe original
Q1 = df.groupby(grupos)['Tempo_s'].transform(lambda x: x.quantile(0.25))
Q3 = df.groupby(grupos)['Tempo_s'].transform(lambda x: x.quantile(0.75))
IQR = Q3 - Q1

limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR

# Filtramos o dataframe original mantendo apenas o que está dentro dos limites numéricos
df_clean = df[(df['Tempo_s'] >= limite_inferior) & (df['Tempo_s'] <= limite_superior)].copy()


# ==========================================
# 3. PLOTS SOLICITADOS
# ==========================================
sns.set_theme(style="whitegrid")

# --- PLOT 4 REVISADO: Tempo Médio separado por Status (Sem Outliers) ---
# Usamos legend_out=False para forçar a legenda a ficar dentro da área do gráfico
g = sns.catplot(
    data=df_clean, 
    kind="bar",
    x="Cenario", 
    y="Tempo_s", 
    hue="Sistema_Operacional", 
    col="Status", 
    errorbar=None, # Removido para que os números não fiquem em cima das barras de erro
    palette='viridis',
    height=6, 
    aspect=1.2,
    sharey=False,
    legend_out=False # Evita que a legenda fuja da imagem
)

# Ajuste do título para y=0.98 (1.05 jogava o título para fora do canvas)
g.fig.suptitle('Tempo Médio de Execução por Cenário e SO (Sem Outliers)', y=0.98, fontsize=16)
g.set_axis_labels("Cenário", "Tempo Médio (segundos)")

# Iterando sobre os subgráficos para adicionar os valores nas barras
for ax in g.axes.flat:
    ax.tick_params(axis='x', rotation=45)
    
    # ax.containers guarda as barras geradas pelo seaborn
    for container in ax.containers:
        # Adiciona o texto no topo (fmt='%.2f' formata para 2 casas decimais)
        ax.bar_label(container, fmt='%.2f', padding=3, fontsize=10)

# tight_layout reajusta as margens para garantir que título e eixos caibam na imagem
g.tight_layout()
plt.show()

# ==========================================
# 4. CÁLCULO E PLOT DO SPEEDUP
# ==========================================
# (Passos A, B e C continuam iguais aos seus)
baseline = df_clean[df_clean['Tipo_Execucao'] == 'Sequencial'].groupby(['Sistema_Operacional', 'Status'])['Tempo_s'].mean().reset_index()
baseline.rename(columns={'Tempo_s': 'Tempo_Baseline'}, inplace=True)

df_speedup = pd.merge(df_clean, baseline, on=['Sistema_Operacional', 'Status'])
df_speedup['Speedup'] = df_speedup['Tempo_Baseline'] / df_speedup['Tempo_s']
df_speedup_paralelo = df_speedup[df_speedup['Tipo_Execucao'] != 'Sequencial']

plt.figure(figsize=(12, 6))

# Salvamos o objeto do gráfico na variável 'ax' para podermos iterar sobre ele
ax = sns.barplot(
    data=df_speedup_paralelo, 
    x='Cenario', 
    y='Speedup', 
    hue='Sistema_Operacional', 
    palette='magma',
    errorbar=None
)

plt.axhline(y=1.0, color='r', linestyle='--', linewidth=2, label='Baseline (Sequencial = 1x)')
# Usamos 'pad' no título para dar um respiro sem jogar para fora
plt.title('Aceleração (Speedup) em relação ao Cenário Sequencial', fontsize=16, pad=15)
plt.xlabel('Cenário')
plt.ylabel('Speedup (X vezes mais rápido)')
plt.xticks(rotation=45, ha='right')

# Adicionando os valores de speedup no topo de cada barra com o sufixo "x"
for container in ax.containers:
    ax.bar_label(container, fmt='%.2fx', padding=3, fontsize=10)

# Posicionando a legenda manualmente no canto superior direito interno
plt.legend(loc='upper right')

# Garante que nada (como a rotação do eixo X) fique fora do PNG salvo
plt.tight_layout() 
plt.show()


import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# ==========================================
# PLOT 1: Curva de Escalabilidade (Com Vértices Anotados)
# ==========================================

# 1. Filtra os dados paralelos
df_paralelo_clean = df_clean[df_clean['Tipo_Execucao'] != 'Sequencial']

# 2. Cria o grid de gráficos
g = sns.relplot(
    data=df_paralelo_clean, 
    kind="line",
    x='N_Workers', 
    y='Tempo_s', 
    hue='Tipo_Execucao', 
    col='Status',
    row='Sistema_Operacional',
    marker='o',
    errorbar=None, 
    linewidth=2.5,
    markersize=8,
    palette='Set1',
    height=5, # Aumentei levemente a altura para dar espaço aos rótulos
    aspect=1.3,
    facet_kws={'sharey': False} 
)

g.fig.suptitle('Curva de Escalabilidade: Desempenho Paralelo por SO e Status', y=1.03, fontsize=16)
g.set_axis_labels("Número de Workers (N)", "Tempo Médio (segundos)")

baseline_seq = df_clean[df_clean['Tipo_Execucao'] == 'Sequencial'].groupby(['Sistema_Operacional', 'Status'])['Tempo_s'].mean().reset_index()
xticks_validos = sorted(df_paralelo_clean['N_Workers'].unique())

# 3. Iteramos sobre cada subgráfico para adicionar linhas e rótulos
for (dict_chaves), ax in g.axes_dict.items():
    so_atual = dict_chaves[0]
    status_atual = dict_chaves[1]
    
    ax.set_xticks(xticks_validos)
    
    # --- Adicionando o Baseline (Sequencial) ---
    valor_baseline = baseline_seq[(baseline_seq['Sistema_Operacional'] == so_atual) & (baseline_seq['Status'] == status_atual)]['Tempo_s'].values
    if len(valor_baseline) > 0:
        tempo_seq = valor_baseline[0]
        ax.axhline(y=tempo_seq, color='gray', linestyle='--', linewidth=1.5, alpha=0.7, label=f'Sequencial ({tempo_seq:.2f}s)')
    
    # --- Adicionando os Rótulos nos Vértices (Evitando Sobreposição) ---
    # Pegamos apenas as linhas de dados (ignoramos a linha tracejada do baseline)
    linhas_dados = [line for line in ax.lines if line.get_linestyle() not in ['--', ':']]
    
    for idx, line in enumerate(linhas_dados):
        x_data = line.get_xdata()
        y_data = line.get_ydata()
        cor_linha = line.get_color() # Usa a mesma cor da linha para o texto
        
        # Truque de Mestre: Se for a primeira linha (ex: Threads), joga o texto para cima.
        # Se for a segunda linha (ex: Processos), joga o texto para baixo.
        deslocamento_y = 10 if idx % 2 == 0 else -15
        alinhamento_v = 'bottom' if idx % 2 == 0 else 'top'
        
        for x, y in zip(x_data, y_data):
            if pd.isna(y): continue # Evita erro se houver dado vazio
            
            ax.annotate(
                f'{y:.2f}', 
                xy=(x, y), 
                xytext=(0, deslocamento_y), # Move no eixo Y
                textcoords='offset points', 
                ha='center', 
                va=alinhamento_v,
                fontsize=9,
                fontweight='bold',
                color=cor_linha,
                # Caixa branca translúcida atrás do número para não misturar com a grade do fundo
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85)
            )

    ax.legend(fontsize=9, loc='best')

# Ajusta as margens para tudo caber perfeitamente
plt.tight_layout()
plt.show()


# ==========================================
# PLOT 3 REVISADO: Boxplot Threads vs Processos (Por SO e Status)
# ==========================================

# 1. Definimos a ordem para garantir que o texto alinhe com a caixa correta
ordem_so = df_paralelo_clean['Sistema_Operacional'].unique()
ordem_tipo = ['Processos', 'Threads'] # Fixamos a ordem do hue

# 2. Criamos o grid separando por Status
g = sns.catplot(
    data=df_paralelo_clean, 
    kind="box",
    x='Sistema_Operacional', 
    y='Tempo_s', 
    hue='Tipo_Execucao',
    col='Status',
    palette='mako',
    order=ordem_so,
    hue_order=ordem_tipo,
    height=6, 
    aspect=1.2,
    sharey=False, # Escalas Y independentes
    legend_out=False # Mantém a legenda dentro da imagem
)

# Ajuste do título para não sobrepor
g.fig.suptitle('Eficiência: Threads vs Processos por SO e Status', y=0.98, fontsize=16)
g.set_axis_labels("Sistema Operacional", "Tempo de Execução (segundos)")

# 3. Lógica para anotar a Mediana em cima de cada Boxplot
for status, ax in g.axes_dict.items():
    # Filtra os dados apenas para o painel atual (Encontrado ou Não Encontrado)
    df_panel = df_paralelo_clean[df_paralelo_clean['Status'] == status]
    
    # Percorre cada Sistema Operacional (Eixo X)
    for x_pos, so in enumerate(ordem_so):
        
        # O Seaborn com 2 'hues' desloca a primeira caixa em -0.2 e a segunda em +0.2 no eixo X
        offsets = [-0.2, 0.2] 
        
        for offset, tipo in zip(offsets, ordem_tipo):
            # Calcula a mediana exata para esse agrupamento específico
            mediana = df_panel[(df_panel['Sistema_Operacional'] == so) & (df_panel['Tipo_Execucao'] == tipo)]['Tempo_s'].median()
            
            # Se existir dado válido, desenha o texto
            if not pd.isna(mediana):
                ax.annotate(
                    f'{mediana:.2f}s',
                    xy=(x_pos + offset, mediana),
                    xytext=(0, 8), # Empurra o texto 8 pixels para cima da mediana
                    textcoords='offset points',
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    fontweight='bold',
                    color='black',
                    # Fundo branco translúcido para o texto não se misturar com a grade
                    bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85)
                )

# Aplica o layout ajustado para nada ficar cortado nas bordas
g.tight_layout()
plt.show()