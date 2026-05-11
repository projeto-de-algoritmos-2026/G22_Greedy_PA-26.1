
from src.models import Atendimento, Rota


def atraso_maximo_scheduling(atendimentos, duracao_trajeto=5):
    
    if not atendimentos:
        return Rota(duracao_trajeto)
    
    # Cria uma cópia para não modificar a lista original
    atendimentos_copia = [
        Atendimento(
            a.id, a.descricao, a.duracao, a.momento_chamado
        ) for a in atendimentos
    ]
    
   
    # Implementação manual de ordenação
    n = len(atendimentos_copia)
    for i in range(n):
        for j in range(i + 1, n):
            if atendimentos_copia[j].duracao < atendimentos_copia[i].duracao:
                # Trocar posições
                atendimentos_copia[i], atendimentos_copia[j] = (
                    atendimentos_copia[j], atendimentos_copia[i]
                )
    
    # Criar rota com atendimentos ordenados
    rota = Rota(duracao_trajeto)
    for atendimento in atendimentos_copia:
        rota.adicionar_atendimento(atendimento)
    
    # Calcular tempos e atrasos
    rota.calcular_tempos()
    
    return rota


def atraso_maximo_com_prazos(atendimentos, duracao_trajeto=5):
    
    if not atendimentos:
        return Rota(duracao_trajeto)
    
    atendimentos_copia = [
        Atendimento(
            a.id, a.descricao, a.duracao, a.tempo_chegada
        ) for a in atendimentos
    ]
    
    
    # Verificar se há prazos diferentes
    tem_prazos = any(a.momento_chamado != atendimentos_copia[0].momento_chamado 
                     for a in atendimentos_copia)
    
    if tem_prazos:
        # Ordenar por tempo de chegada + duração (prazo)
        n = len(atendimentos_copia)
        for i in range(n):
            for j in range(i + 1, n):
                prazo_i = atendimentos_copia[i].momento_chamado + atendimentos_copia[i].duracao
                prazo_j = atendimentos_copia[j].momento_chamado + atendimentos_copia[j].duracao
                if prazo_j < prazo_i:
                    atendimentos_copia[i], atendimentos_copia[j] = (
                        atendimentos_copia[j], atendimentos_copia[i]
                    )
    else:
    
        n = len(atendimentos_copia)
        for i in range(n):
            for j in range(i + 1, n):
                if atendimentos_copia[j].duracao < atendimentos_copia[i].duracao:
                    atendimentos_copia[i], atendimentos_copia[j] = (
                        atendimentos_copia[j], atendimentos_copia[i]
                    )
    
    rota = Rota(duracao_trajeto)
    for atendimento in atendimentos_copia:
        rota.adicionar_atendimento(atendimento)
    
    rota.calcular_tempos()
    return rota


def calcular_metricas(rota):
    """
    Calcula métricas da rota.
    
    Returns:
        Dicionário com métricas
    """
    if not rota.atendimentos:
        return {
            'tempo_total': 0,
            'atraso_maximo': 0,
            'atraso_medio': 0,
            'soma_atrasos': 0
        }
    
    soma_atrasos = sum(a.atraso for a in rota.atendimentos)
    atraso_medio = soma_atrasos / len(rota.atendimentos)
    
    return {
        'tempo_total': rota.tempo_total,
        'atraso_maximo': rota.obter_atraso_maximo(),
        'atraso_medio': atraso_medio,
        'soma_atrasos': soma_atrasos,
        'quantidade_atendimentos': len(rota.atendimentos)
    }