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

## Para personalizar os testes, basta alterar as seguintes variáveis: 

repeticoes = 1

diretorio_chaves = "chaves"
diretorio_assinaturas = "assinaturas"
diretorio_arquivos_entrada = "arquivos_entrada"
diretorio_resultados = "resultados_tempos_medias"

lista_arquivos = [{"nome": "10MB", "tamanho_mb": 10}, {"nome": "100MB", "tamanho_mb": 100}, {"nome": "1GB", "tamanho_mb": 1024}] 
lista_algoritmos = ["Dilithium5", "Falcon-1024", "SPHINCS+-SHAKE-256s-simple"]

## To be done:

Incluir algoritmo clássico RSA
Gerar gráficos
Setar a VM
Incluir no documento