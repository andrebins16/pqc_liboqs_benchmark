import json
import matplotlib.pyplot as plt
import os
import sys

if len(sys.argv) < 2:
    print("Uso: python script.py <caminho_para_arquivo_de_dados>")
    sys.exit(1)

arquivo = sys.argv[1]

# carrega dados
with open(arquivo, "r") as f:
    dados = eval(f.read())

# diretório de saída
os.makedirs("graficos", exist_ok=True)

def plot_horizontal(dados, tempos, titulo, nome_arquivo):
    algoritmos = list(tempos.keys())
    valores = list(tempos.values())
    cores = ['firebrick' if alg in dados['algoritmos_classicos'] else 'steelblue' for alg in algoritmos]

    plt.figure(figsize=(10, 6))
    plt.barh(algoritmos, valores, color=cores, edgecolor='black')
    plt.xlabel("Tempo [s]")
    plt.title(titulo)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"graficos/{nome_arquivo}.png")
    plt.close()

# gráfico geração
plot_horizontal(
    dados,
    dados["geracao"],
    "Tempo médio de geração das chaves",
    "geracao"
)

# gráficos por tamanho
for categoria in ["assinatura", "verificacao"]:
    for tamanho, tempos in dados[categoria].items():
        titulo = f"Tempo médio de {categoria.capitalize()} - {tamanho}"
        nome_arquivo = f"{categoria}_{tamanho}"
        plot_horizontal(dados, tempos, titulo, nome_arquivo)