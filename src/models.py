class Atendimento:
    """Representa um atendimento médico"""
    
    def __init__(self, id, descricao, duracao, momento_chamado=0):
        """
        Args:
            id: Identificador único do atendimento
            descricao: Descrição do atendimento (ex: Curativo, Febre, etc)
            duracao: Tempo de duração em minutos
            momento_chamado: Momento do chamado (padrão 0)
        """
        self.id = id
        self.descricao = descricao
        self.duracao = duracao
        self.momento_chamado = momento_chamado
        self.tempo_conclusao = None
        self.atraso = None
        self.ordem_atendimento = None
    
    def __repr__(self):
        return (f"Atendimento(id={self.id}, desc='{self.descricao}', "
                f"duracao={self.duracao}min, atraso={self.atraso})")
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'descricao': self.descricao,
            'duracao': self.duracao,
            'momento_chamado': self.momento_chamado,
            'tempo_conclusao': self.tempo_conclusao,
            'atraso': self.atraso,
            'ordem_atendimento': self.ordem_atendimento
        }

    @staticmethod
    def from_dict(data):
        """Cria a partir de um dicionário"""
        atendimento = Atendimento(
            id=data['id'],
            descricao=data['descricao'],
            duracao=data['duracao'],
            momento_chamado=data.get('momento_chamado', data.get('tempo_chegada', 0))
        )
        atendimento.tempo_conclusao = data.get('tempo_conclusao')
        atendimento.atraso = data.get('atraso')
        atendimento.ordem_atendimento = data.get('ordem_atendimento')
        return atendimento


class Rota:
    """Representa a rota da ambulância"""
    
    def __init__(self, duracao_trajeto_entre_pontos=5):
        """
        Args:
            duracao_trajeto_entre_pontos: Tempo em minutos entre pontos
        """
        self.atendimentos = []
        self.tempo_total = 0
        self.duracao_trajeto = duracao_trajeto_entre_pontos
    
    def adicionar_atendimento(self, atendimento):
        """Adiciona um atendimento à rota"""
        self.atendimentos.append(atendimento)
    
    def calcular_tempos(self):
        """Calcula os tempos de conclusão e atrasos"""
        tempo_atual = 0
        
        for i, atendimento in enumerate(self.atendimentos):
            # Tempo de trajeto (exceto no primeiro)
            if i > 0:
                tempo_atual += self.duracao_trajeto
            
            # Tempo de atendimento
            tempo_atual += atendimento.duracao
            atendimento.tempo_conclusao = tempo_atual
            
            # Atraso = max(0, tempo_conclusao - prazo_desejado)
            # Prazo desejado = tempo_chegada + duração (serviço imediato)
            prazo_desejado = atendimento.momento_chamado + atendimento.duracao
            atendimento.atraso = max(0, atendimento.tempo_conclusao - prazo_desejado)
            atendimento.ordem_atendimento = i + 1
        
        self.tempo_total = tempo_atual
    
    def obter_atraso_maximo(self):
        """Retorna o atraso máximo entre todos os atendimentos"""
        if not self.atendimentos:
            return 0
        return max(a.atraso for a in self.atendimentos)
    
    def to_dict(self):
        """Converte para dicionário"""
        return {
            'atendimentos': [a.to_dict() for a in self.atendimentos],
            'tempo_total': self.tempo_total,
            'duracao_trajeto': self.duracao_trajeto,
            'atraso_maximo': self.obter_atraso_maximo()
        }
