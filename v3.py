import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# ==========================================
# Substitua 'seu_arquivo.csv' pelo nome real do seu arquivo
df = pd.read_csv('datasetFinal.csv')

# Configuração de estilo para os gráficos
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Exibir as primeiras linhas e informações básicas para conferência
print("--- Primeiras Linhas ---")
print(df.head())
print("\n--- Informações do Dataset ---")
print(df.info())

# ==========================================
# 2. ANÁLISE EXPLORATÓRIA E PLOTS
# ==========================================

# Plot 1: Distribuição do Status (Quantos acharam o hash vs Não acharam)
plt.figure(figsize=(8, 5))
ax = sns.countplot(data=df, x='Status', palette='pastel')
plt.title('Contagem de Buscas: Encontrado vs Não Encontrado', fontsize=14)
plt.xlabel('Status')
plt.ylabel('Quantidade de Execuções')
# Adicionando os rótulos de dados em cima das barras
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points')
plt.tight_layout()
plt.show()

# Plot 2: Boxplot de Tempo de Execução por Processador
# Ideal para ver a variância e os outliers de cada CPU
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Processador', y='Tempo_s', hue='Status', palette='Set2')
plt.title('Distribuição do Tempo de Execução por Processador e Status', fontsize=14)
plt.xlabel('Processador')
plt.ylabel('Tempo (segundos)')
plt.xticks(rotation=45, ha='right') # Rotacionar nomes longos de processadores
plt.tight_layout()
plt.show()

# Plot 3: Relação entre Memória RAM e Tempo de Execução
# Scatter plot para ver se mais RAM significa menor tempo, colorindo pelo cenário
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='RAM_GB', y='Tempo_s', hue='Cenario', style='Status', s=100, alpha=0.7)
plt.title('Impacto da Memória RAM no Tempo de Execução por Cenário', fontsize=14)
plt.xlabel('Memória RAM (GB)')
plt.ylabel('Tempo (segundos)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Plot 4: Tempo Médio por Cenário (Gráfico de Barras)
# Agrupado por Sistema Operacional para ver se o SO afeta o desempenho
plt.figure(figsize=(12, 6))
sns.barplot(data=df, x='Cenario', y='Tempo_s', hue='Sistema_Operacional', errorbar='sd', palette='viridis')
plt.title('Tempo Médio de Execução por Cenário e Sistema Operacional', fontsize=14)
plt.xlabel('Cenário')
plt.ylabel('Tempo Médio (segundos)')
plt.tight_layout()
plt.show()

# Plot 5: Correlação entre Cores, Threads, RAM e Tempo (Apenas Numéricos)
plt.figure(figsize=(8, 6))
cols_numericas = ['Cores', 'Threads', 'RAM_GB', 'Tempo_s', 'Media_Cenario']
matriz_correlacao = df[cols_numericas].corr()
sns.heatmap(matriz_correlacao, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
plt.title('Matriz de Correlação das Variáveis de Hardware e Tempo', fontsize=14)
plt.tight_layout()
plt.show()

# ==========================================
# 3. AGRUPAMENTOS E TABELAS DE RESUMO (Opcional)
# ==========================================
print("\n--- Tempo Médio por Processador e Status ---")
resumo_proc = df.groupby(['Processador', 'Status'])['Tempo_s'].mean().reset_index()
print(resumo_proc.sort_values(by='Tempo_s'))