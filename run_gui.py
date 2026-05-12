import sys
import os

# Adicionar o diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui import iniciar_gui

if __name__ == "__main__":
    print("Iniciando Interface Gráfica da Ambulância Inteligente...")
    print("Aguarde alguns segundos para o Tkinter abrir...\n")
    
    try:
        iniciar_gui()
    except Exception as e:
        print(f"Erro ao iniciar GUI: {e}")
        import traceback
        traceback.print_exc()