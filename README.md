# G22_Greedy_PA-26.1

Projeto que implementa um algoritmo guloso para ordenar atendimento de pacientes
de modo a minimizar o atraso máximo.

Como executar

- Requisitos: Python 3.8+ (nenhuma dependência externa obrigatória para rodar o programa)
- A partir da raiz do repositório:

```bash
python3 src/main.py
```

Opções úteis:

- Rodar com exemplo embutido:

```bash
python3 src/main.py --example
```

- Ler pacientes de um arquivo JSON (lista de objetos com campos "nome", "tempo", "prazo"):

```bash
python3 src/main.py --file dados.json
```

Exemplo de `dados.json`:

```json
[
  {"nome": "Ana", "tempo": 30, "prazo": 60},
  {"nome": "Beto", "tempo": 20, "prazo": 40}
]
```

Testes

Instale as dependências de desenvolvimento e rode os testes com pytest:

```bash
python3 -m pip install -r requirements.txt
pytest -q
```

Melhorias incluídas

- Validações de entradas interativas e de arquivo JSON
- Suporte a modo não interativo (`--no-interactive`)
- Testes unitários básicos para `algoritmo.py`
# G22_Greedy_PA-26.1