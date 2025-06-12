from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from pprint import pformat
from sys import stdout
import time
from pprint import pformat
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


def gera_chaves_rsa():
    inicio = time.time()
    #gera as chaves em objetos python
    chave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    chave_publica = chave_privada.public_key()
    fim = time.time()
    tempo = fim - inicio

    #serializar chaves
    chave_privada_serializada = chave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    chave_publica_serializada =chave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return chave_publica_serializada, chave_privada_serializada, tempo


def assina_rsa(mensagem, chave_privada_serializada):
    #carregar chave privada serializada
    chave_privada = serialization.load_pem_private_key(chave_privada_serializada, password=None)
    inicio = time.time()
    assinatura = chave_privada.sign(
        mensagem,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA512()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA512()
    )
    fim = time.time()
    tempo = fim - inicio
    return assinatura, tempo

def verifica_rsa(mensagem, assinatura, chave_publica_serializada):
    #carregar chave publica serializada
    chave_publica = serialization.load_pem_public_key(chave_publica_serializada)
    inicio = time.time()
    try:
        chave_publica.verify(
            assinatura,
            mensagem,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA512()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA512()
        )
        valido = True
    except InvalidSignature:
        valido = False
    
    fim = time.time()
    tempo = fim - inicio
    if not valido:
        raise Exception("Assinatura RSA inválida")
    return valido, tempo

def gera_chaves_ecc():
    inicio = time.time()
    chave_privada = ec.generate_private_key(ec.SECP256R1())
    chave_publica = chave_privada.public_key()
    fim = time.time()
    tempo = fim - inicio

    chave_privada = chave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    chave_publica = chave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return chave_publica, chave_privada, tempo

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def assina_ecc(mensagem, chave_privada_pem):
    chave_privada = serialization.load_pem_private_key(chave_privada_pem, password=None)
    inicio = time.time()
    assinatura = chave_privada.sign(
        mensagem,
        ec.ECDSA(hashes.SHA512())
    )
    fim = time.time()
    tempo = fim - inicio
    return assinatura, tempo

def verifica_ecc(mensagem, assinatura, chave_publica_pem):
    chave_publica = serialization.load_pem_public_key(chave_publica_pem)
    inicio = time.time()
    try:
        chave_publica.verify(
            assinatura,
            mensagem,
            ec.ECDSA(hashes.SHA512())
        )
        valido = True
    except InvalidSignature:
        valido = False
    fim = time.time()
    tempo = fim - inicio
    if not valido:
        raise Exception("Assinatura ECC inválida")
    return valido, tempo