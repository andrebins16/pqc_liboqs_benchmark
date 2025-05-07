## Para rodar localmente (LINUX), baixe o liboqs para python usando os seguinte comandos: 

sudo apt update && sudo apt install cmake gcc python3-pip libssl-dev ninja-build -y

git clone --recursive https://github.com/open-quantum-safe/liboqs.git
cd liboqs
mkdir build && cd build
cmake -GNinja .. -DOQS_BUILD_ONLY_LIB=ON
ninja
sudo ninja install

git clone --recursive https://github.com/open-quantum-safe/liboqs-python.git
cd liboqs-python
pip install .

pip install cryptography

## Para personalizar os testes, basta alterar as seguintes variáveis: 

repeticoes = 1

diretorio_chaves = "chaves"
diretorio_assinaturas = "assinaturas"
diretorio_arquivos_entrada = "arquivos_entrada"
diretorio_resultados = "resultados_tempos_medias"

lista_arquivos = [{"nome": "10MB", "tamanho_mb": 10}, {"nome": "100MB", "tamanho_mb": 100}, {"nome": "1GB", "tamanho_mb": 1024}] 
lista_algoritmos = ["Dilithium5", "Falcon-1024", "SPHINCS+-SHAKE-256s-simple"]

## Para incluir mais algoritmos clássicos:
Crie uma função para gerar chaves, assinar e verificar com as mesmas assinaturas da do RSA. Depois, inclua as novas informações aqui: 
- lista_algoritmos_classicos = [{"nome":"RSA", "funcao_gera":gera_chaves_rsa, "funcao_assina":assina_rsa, "funcao_verifica":verifica_rsa}]

## Para rodar os testes, executar script_testes.py

## Para criar os gráficos, rode o seguinte comando: python3 graficos.py resultados_tempos_medias/medias.txt

## To be done:
Incluir algoritmo clássico RSA
Gerar gráficos
Incluir no documento