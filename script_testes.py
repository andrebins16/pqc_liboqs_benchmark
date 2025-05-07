from pprint import pformat
from sys import stdout
import oqs
import time
from pprint import pformat
import os
import subprocess
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from algoritmos_classicos_funcoes import gera_chaves_rsa, assina_rsa, verifica_rsa

repeticoes = 1

diretorio_chaves = "chaves"
diretorio_assinaturas = "assinaturas"
diretorio_arquivos_entrada = "arquivos_entrada"
diretorio_resultados = "resultados_tempos_medias"

lista_algoritmos_classicos = [{"nome":"RSA", "funcao_gera":gera_chaves_rsa, "funcao_assina":assina_rsa, "funcao_verifica":verifica_rsa}]
lista_arquivos = [{"nome": "10MB", "tamanho_mb": 10}, {"nome": "100MB", "tamanho_mb": 100}, {"nome": "1GB", "tamanho_mb": 1024}] 
lista_algoritmos = ["Dilithium5", "Falcon-1024", "SPHINCS+-SHAKE-256s-simple", "RSA"]
lista_combinada_algoritmos_arquivos = [{"algoritmo": alg, "arquivo": arq["nome"]} for alg in lista_algoritmos for arq in lista_arquivos]

dicionario_tempos_geracao = {}
dicionario_tempos_assinatura = {}
dicionario_tempos_verificacao = {}

dicionario_medias_geracao = {}
dicionario_medias_assinatura = {}
dicionario_medias_verificacao = {}

def gera_chaves(algoritmo):
    inicio = time.time()
    with oqs.Signature(algoritmo) as gerador:
        chave_publica = gerador.generate_keypair()
        chave_privada = gerador.export_secret_key()
    fim = time.time()
    tempo = fim - inicio
    return chave_publica, chave_privada, tempo

def assina(algoritmo, mensagem, chave_privada):
    inicio = time.time()
    with oqs.Signature(algoritmo, chave_privada) as assinador:
        assinatura = assinador.sign(mensagem)
    fim = time.time()
    tempo = fim - inicio
    return assinatura, tempo

def verifica(algoritmo, mensagem, assinatura, chave_publica):
    inicio = time.time()
    with oqs.Signature(algoritmo) as verificador:
        resultado = verificador.verify(mensagem, assinatura, chave_publica)
    fim = time.time()
    tempo = fim - inicio
    if not resultado:
        raise Exception("Assinatura inválida")
    return resultado, tempo


def gera_chaves_arquivo(algoritmo):
    objeto_algoritmo_classico = procura_algoritmo_na_lista_de_classicos_e_retorna(algoritmo) #para verificar se é algoritmo classico, pois dai as funções são personalizadas
    if objeto_algoritmo_classico != None:
        chave_publica, chave_privada, tempo = objeto_algoritmo_classico["funcao_gera"]()
    else:
        chave_publica, chave_privada, tempo = gera_chaves(algoritmo)
        
    with open(f"{diretorio_chaves}/{algoritmo}_chave_publica.key", "wb") as f:
        f.write(chave_publica)
    with open(f"{diretorio_chaves}/{algoritmo}_chave_privada.key", "wb") as f:
        f.write(chave_privada)
    return tempo

def assina_arquivo(algoritmo, arquivo_entrada):
    with open(f"{diretorio_arquivos_entrada}/{arquivo_entrada}", "rb") as f:
        mensagem = f.read()
    with open(f"{diretorio_chaves}/{algoritmo}_chave_privada.key", "rb") as f:
        chave_privada = f.read()

    objeto_algoritmo_classico = procura_algoritmo_na_lista_de_classicos_e_retorna(algoritmo) #para verificar se é algoritmo classico, pois dai as funções são personalizadas
    if objeto_algoritmo_classico != None:
        assinatura, tempo = objeto_algoritmo_classico["funcao_assina"](mensagem, chave_privada)
    else:
        assinatura, tempo = assina(algoritmo, mensagem, chave_privada)
    
    with open(f"{diretorio_assinaturas}/{algoritmo}_{arquivo_entrada}.sig", "wb") as f:
        f.write(assinatura)
    return tempo

def verifica_arquivo(algoritmo, arquivo_entrada):
    with open(f"{diretorio_arquivos_entrada}/{arquivo_entrada}", "rb") as f:
        mensagem = f.read()
    with open(f"{diretorio_assinaturas}/{algoritmo}_{arquivo_entrada}.sig", "rb") as f:
        assinatura = f.read()
    with open(f"{diretorio_chaves}/{algoritmo}_chave_publica.key", "rb") as f:
        chave_publica = f.read()

    objeto_algoritmo_classico = procura_algoritmo_na_lista_de_classicos_e_retorna(algoritmo) #para verificar se é algoritmo classico, pois dai as funções são personalizadas
    if objeto_algoritmo_classico != None:
        resultado, tempo = objeto_algoritmo_classico["funcao_verifica"](mensagem, assinatura, chave_publica)
    else:
        resultado, tempo = verifica(algoritmo, mensagem, assinatura, chave_publica)
    
    return tempo


def roda_testes_geracao_chaves():
    for algoritmo in lista_algoritmos:
        dicionario_tempos_geracao[algoritmo] = []
        for i in range(repeticoes):
            tempo = gera_chaves_arquivo(algoritmo)
            dicionario_tempos_geracao[algoritmo].append(tempo)
        dicionario_medias_geracao[algoritmo] = sum(dicionario_tempos_geracao[algoritmo]) / repeticoes

def roda_testes_assinaturas():
    for algoritmo in lista_algoritmos: #só para garantir que as chaves estao geradas (se rodar somente esse metodo)
        gera_chaves_arquivo(algoritmo) 
    
    for arquivo in lista_arquivos:
        dicionario_tempos_assinatura[arquivo["nome"]] = {}
        dicionario_medias_assinatura[arquivo["nome"]] = {}
    
    for alg_arq in lista_combinada_algoritmos_arquivos:     
        dicionario_tempos_assinatura[alg_arq["arquivo"]][alg_arq["algoritmo"]] = []
        for i in range(repeticoes):
            tempo = assina_arquivo(alg_arq["algoritmo"], alg_arq["arquivo"])
            dicionario_tempos_assinatura[alg_arq["arquivo"]][alg_arq["algoritmo"]].append(tempo)
        dicionario_medias_assinatura[alg_arq["arquivo"]][alg_arq["algoritmo"]] = sum(dicionario_tempos_assinatura[alg_arq["arquivo"]][alg_arq["algoritmo"]]) / repeticoes

def roda_testes_verificacoes():
    for algoritmo in lista_algoritmos: #só para garantir que as chaves estao geradas (se rodar somente esse metodo)
        gera_chaves_arquivo(algoritmo) 

    for arquivo in lista_arquivos:
        dicionario_tempos_verificacao[arquivo["nome"]] = {}
        dicionario_medias_verificacao[arquivo["nome"]] = {}

    for alg_arq in lista_combinada_algoritmos_arquivos:
        assina_arquivo(alg_arq["algoritmo"], alg_arq["arquivo"]) #só para garantir que as assinaturas estao geradas (se rodar somente esse metodo)
        
        dicionario_tempos_verificacao[alg_arq["arquivo"]][alg_arq["algoritmo"]] = []
        for i in range(repeticoes):
            tempo = verifica_arquivo(alg_arq["algoritmo"], alg_arq["arquivo"])
            dicionario_tempos_verificacao[alg_arq["arquivo"]][alg_arq["algoritmo"]].append(tempo)
        dicionario_medias_verificacao[alg_arq["arquivo"]][alg_arq["algoritmo"]] = sum(dicionario_tempos_verificacao[alg_arq["arquivo"]][alg_arq["algoritmo"]]) / repeticoes


def salvar_dicionario(nome_arquivo, dicionario):
    with open(nome_arquivo, "w") as f:
        f.write(pformat(dicionario))

def inicializa_diretorios_e_arquivos():
    os.makedirs(diretorio_chaves, exist_ok=True)
    os.makedirs(diretorio_assinaturas, exist_ok=True)
    os.makedirs(diretorio_arquivos_entrada, exist_ok=True)
    os.makedirs(diretorio_resultados, exist_ok=True)
    
    for arq in lista_arquivos:
        caminho_arquivo = f"{diretorio_arquivos_entrada}/{arq['nome']}"
        if not os.path.exists(caminho_arquivo):
            subprocess.run(["dd", "if=/dev/urandom", f"of={caminho_arquivo}", "bs=1M", f"count={arq['tamanho_mb']}"],check=True)

def procura_algoritmo_na_lista_de_classicos_e_retorna(algoritmo):
    for alg in lista_algoritmos_classicos:
        if alg["nome"] == algoritmo:
            return alg
    return None


if __name__ == '__main__':
    print("Iniciando testes...")

    inicializa_diretorios_e_arquivos()
    
    roda_testes_geracao_chaves()
    roda_testes_assinaturas()
    roda_testes_verificacoes()
    
    salvar_dicionario(f"{diretorio_resultados}/tempos_geracao.txt", dicionario_tempos_geracao)
    salvar_dicionario(f"{diretorio_resultados}/tempos_assinatura.txt", dicionario_tempos_assinatura)
    salvar_dicionario(f"{diretorio_resultados}/tempos_verificacao.txt", dicionario_tempos_verificacao)
    nomes_algoritmos_classicos = [alg["nome"] for alg in lista_algoritmos_classicos]
    salvar_dicionario(f"{diretorio_resultados}/medias.txt", {"geracao": dicionario_medias_geracao, "assinatura": dicionario_medias_assinatura, "verificacao": dicionario_medias_verificacao, "algoritmos_classicos": nomes_algoritmos_classicos})

    print("Testes finalizados.")