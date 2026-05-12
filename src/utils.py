"""
Utilitários para entrada/saída de dados
"""

import json
import os
from pathlib import Path
from src.models import Atendimento, Rota

# Base do projeto (pasta acima de src)
BASE_DIR = Path(__file__).resolve().parent.parent


class GerenciadorDados:
    """Gerencia a leitura e escrita de dados"""
    
    ARQUIVO_PADRAO = "atendimentos.json"
    
    @staticmethod
    def carregar_atendimentos(caminho_arquivo=None):
        """
        Carrega atendimentos de um arquivo JSON.
        
        Args:
            caminho_arquivo: Caminho do arquivo (usa padrão se None)
        
        Returns:
            Lista de objetos Atendimento
        """
        if caminho_arquivo is None:
            caminho = BASE_DIR / GerenciadorDados.ARQUIVO_PADRAO
        else:
            caminho = Path(caminho_arquivo)
            if not caminho.is_absolute():
                caminho = BASE_DIR / caminho_arquivo

        if not caminho.exists():
            print(f"Arquivo {caminho} não encontrado.")
            return []

        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            atendimentos = []
            for item in dados:
                atendimentos.append(Atendimento.from_dict(item))
            
            return atendimentos
        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")
            return []
    
    @staticmethod
    def salvar_atendimentos(atendimentos, caminho_arquivo=None):
        """
        Salva atendimentos em um arquivo JSON.
        
        Args:
            atendimentos: Lista de objetos Atendimento
            caminho_arquivo: Caminho do arquivo (usa padrão se None)
        """
        if caminho_arquivo is None:
            caminho = BASE_DIR / GerenciadorDados.ARQUIVO_PADRAO
        else:
            caminho = Path(caminho_arquivo)
            if not caminho.is_absolute():
                caminho = BASE_DIR / caminho_arquivo

        try:
            dados = [a.to_dict() for a in atendimentos]
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            print(f"Dados salvos em {caminho}")
        except Exception as e:
            print(f"Erro ao salvar arquivo: {e}")
    
    @staticmethod
    def salvar_rota(rota, caminho_arquivo="rota_resultado.json"):
        """
        Salva a rota otimizada em um arquivo JSON.
        
        Args:
            rota: Objeto Rota
            caminho_arquivo: Caminho do arquivo
        """
        caminho = Path(caminho_arquivo)
        if not caminho.is_absolute():
            caminho = BASE_DIR / caminho_arquivo

        try:
            dados = rota.to_dict()
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            print(f"Rota salva em {caminho}")
        except Exception as e:
            print(f"Erro ao salvar rota: {e}")
    
    @staticmethod
    def criar_exemplo():
        """Cria um arquivo de exemplo com atendimentos"""
        exemplo = [
            {
                "id": 1,
                "descricao": "Curativo",
                "duracao": 5,
                "momento_chamado": 0
            },
            {
                "id": 2,
                "descricao": "Febre",
                "duracao": 10,
                "momento_chamado": 1
            },
            {
                "id": 3,
                "descricao": "Acidente grave",
                "duracao": 40,
                "momento_chamado": 2
            },
            {
                "id": 4,
                "descricao": "Dor de cabeça",
                "duracao": 8,
                "momento_chamado": 3
            },
            {
                "id": 5,
                "descricao": "Pressão alta",
                "duracao": 12,
                "momento_chamado": 5
            }
        ]

        caminho = BASE_DIR / "atendimentos_exemplo.json"

        if caminho.exists():
            print(f"Arquivo de exemplo já existe: {caminho}")
            try:
                with open(caminho, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                return dados
            except Exception:
                print("Aviso: não foi possível ler o arquivo existente; retornando exemplo em memória.")
                return exemplo

        try:
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(exemplo, f, indent=2, ensure_ascii=False)
            print(f"Arquivo de exemplo criado: {caminho}")
        except PermissionError:
            print(f"Permissão negada ao criar {caminho}; usando exemplo em memória.")

        return exemplo


def ler_entrada_usuario():
    """
    Função interativa para o usuário entrar com dados de atendimentos.
    
    Returns:
        Lista de objetos Atendimento
    """
    atendimentos = []
    print("\n=== ENTRADA DE ATENDIMENTOS ===")
    print("Digite os dados dos atendimentos. Digite 'sair' para finalizar.\n")
    
    contador = 1
    while True:
        print(f"--- Atendimento {contador} ---")
        
        descricao = input("Descrição (ou 'sair'): ").strip()
        if descricao.lower() == 'sair':
            break
        
        try:
            duracao = int(input("Duração (minutos): "))
            momento_chamado = int(input("Momento do chamado (minutos, padrão 0): ") or "0")

            atendimento = Atendimento(
                id=contador,
                descricao=descricao,
                duracao=duracao,
                momento_chamado=momento_chamado
            )
            atendimentos.append(atendimento)
            print("✓ Atendimento adicionado\n")
            contador += 1
        
        except ValueError:
            print("Erro: Digite números válidos para duração e momento do chamado.\n")
            continue
    
    return atendimentos