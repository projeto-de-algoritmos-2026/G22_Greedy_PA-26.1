"""
Ponto de entrada para o sistema de Ambulância Inteligente
"""

from src.gui import iniciar_gui


def main():
    """Função principal"""
    print("=" * 60)
    print("AMBULÂNCIA INTELIGENTE - AGENDAMENTO OTIMIZADO")
    print("Algoritmo: Atraso Máximo (Maximum Lateness Scheduling)")
    print("=" * 60)
    print()
    
    # Iniciar interface gráfica
    iniciar_gui()


if __name__ == "__main__":
    main()
