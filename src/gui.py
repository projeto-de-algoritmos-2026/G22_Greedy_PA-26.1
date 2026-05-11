"""
Interface Gráfica com Tkinter para visualizar a rota da ambulância
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.models import Atendimento
from src.scheduling import atraso_maximo_scheduling, calcular_metricas
from src.utils import GerenciadorDados


class DialogoNovoAtendimento(tk.Toplevel):
    """Diálogo para adicionar novo atendimento"""

    def __init__(self, parent, numero):
        super().__init__(parent)

        self.title(f"Novo Atendimento #{numero}")

        # JANELA MAIOR
        self.geometry("450x350")

        self.resizable(False, False)

        self.result = None

        # Modal
        self.transient(parent)
        self.grab_set()

        # ================= FRAME PRINCIPAL =================
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # ================= DESCRIÇÃO =================
        ttk.Label(
            frame,
            text="Descrição do Atendimento:",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))

        self.entry_desc = ttk.Entry(frame, width=50)
        self.entry_desc.pack(fill=tk.X, pady=(0, 15))
        self.entry_desc.focus()

        # ================= DURAÇÃO =================
        ttk.Label(
            frame,
            text="Duração (minutos):",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))

        frame_dur = ttk.Frame(frame)
        frame_dur.pack(anchor=tk.W, pady=(0, 15))

        self.spin_duracao = ttk.Spinbox(
            frame_dur,
            from_=1,
            to=180,
            width=10
        )

        self.spin_duracao.set(10)
        self.spin_duracao.pack(side=tk.LEFT)

        ttk.Label(frame_dur, text="min").pack(side=tk.LEFT, padx=5)

        # ================= TEMPO DE CHEGADA =================
        ttk.Label(
            frame,
            text="Momento do Chamado (minutos):",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, pady=(0, 5))

        ttk.Label(
            frame,
            text=(
                "Representa o momento em que o chamado apareceu no sistema.\n"
                "Exemplo: 0 = início | 10 = surgiu após 10 minutos"
            ),
            foreground="gray"
        ).pack(anchor=tk.W, pady=(0, 10))

        frame_chegada = ttk.Frame(frame)
        frame_chegada.pack(anchor=tk.W, pady=(0, 20))

        self.spin_chegada = ttk.Spinbox(
            frame_chegada,
            from_=0,
            to=1000,
            width=10
        )

        self.spin_chegada.set(0)
        self.spin_chegada.pack(side=tk.LEFT)

        ttk.Label(frame_chegada, text="min").pack(side=tk.LEFT, padx=5)

        # ================= BOTÕES =================
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(fill=tk.X, pady=(25, 10))

        ttk.Button(
            frame_botoes,
            text="✓ Adicionar",
            command=self.confirmar
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            frame_botoes,
            text="✗ Cancelar",
            command=self.cancelar
        ).pack(side=tk.LEFT, padx=5)

        # ================= CENTRALIZAR =================
        self.update_idletasks()

        largura = self.winfo_width()
        altura = self.winfo_height()

        x = (self.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.winfo_screenheight() // 2) - (altura // 2)

        self.geometry(f"{largura}x{altura}+{x}+{y}")

    def confirmar(self):

        desc = self.entry_desc.get().strip()

        if not desc:
            messagebox.showwarning(
                "Aviso",
                "Digite uma descrição!"
            )
            return

        try:
            duracao = int(self.spin_duracao.get())
            chegada = int(self.spin_chegada.get())

            self.result = {
                "descricao": desc,
                "duracao": duracao,
                "momento_chamado": chegada
            }

            self.destroy()

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Valores inválidos!"
            )

    def cancelar(self):
        self.destroy()


class AmbulanciaGUI:
    """Interface gráfica para o sistema"""

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Ambulância Inteligente - Agendamento Otimizado"
        )

        self.root.geometry("1400x800")

        self.atendimentos = []
        self.rota_otimizada = None
        self.duracao_trajeto = 5
        self.contador_atendimentos = 0

        self.criar_interface()

    def criar_interface(self):

        # ================= INSTRUÇÕES =================
        frame_instrucoes = ttk.LabelFrame(
            self.root,
            text="INSTRUÇÕES",
            padding=10
        )

        frame_instrucoes.pack(
            fill=tk.X,
            padx=10,
            pady=10
        )

        texto_instrucoes = (
            "1. CARREGUE DADOS: Clique em 'Usar Exemplo' ou use 'Adicionar Atendimento'\n"
            "2. TRAJETO: Tempo que a ambulância leva entre um local e outro\n"
            "3. TEMPO DE CHEGADA: Momento em que o chamado apareceu no sistema\n"
            "4. OTIMIZE: Clique em 'Otimizar Rota' para calcular a melhor ordem\n"
            "5. VISUALIZE: Verde = no prazo | Vermelho = atrasado"
        )

        ttk.Label(
            frame_instrucoes,
            text=texto_instrucoes,
            justify=tk.LEFT
        ).pack(anchor=tk.W)

        # ================= PAINEL DE CONTROLE =================
        frame_botoes = ttk.Frame(self.root)

        frame_botoes.pack(
            fill=tk.X,
            padx=10,
            pady=10
        )

        # ================= CARREGAR DADOS =================
        ttk.Label(
            frame_botoes,
            text="CARREGAR DADOS:",
            font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(
            frame_botoes,
            text="Usar Exemplo",
            command=self.usar_exemplo
        ).pack(side=tk.LEFT, padx=3)

        # ================= SEPARADOR =================
        ttk.Separator(
            frame_botoes,
            orient=tk.VERTICAL
        ).pack(side=tk.LEFT, fill=tk.Y, padx=15)

        # ================= ADICIONAR =================
        ttk.Button(
            frame_botoes,
            text="Adicionar Atendimento",
            command=self.adicionar_atendimento_manual
        ).pack(side=tk.LEFT, padx=3)

        # ================= SEPARADOR =================
        ttk.Separator(
            frame_botoes,
            orient=tk.VERTICAL
        ).pack(side=tk.LEFT, fill=tk.Y, padx=15)

        # ================= TRAJETO =================
        ttk.Label(
            frame_botoes,
            text="Trajeto (min):",
            font=("Arial", 9, "bold")
        ).pack(side=tk.LEFT, padx=5)

        self.spin_trajeto = ttk.Spinbox(
            frame_botoes,
            from_=1,
            to=30,
            width=5
        )

        self.spin_trajeto.set(5)

        self.spin_trajeto.pack(side=tk.LEFT, padx=5)

        ttk.Label(
            frame_botoes,
            text="min"
        ).pack(side=tk.LEFT)

        ttk.Label(
            frame_botoes,
            text="Tempo de deslocamento entre um atendimento e outro",
            foreground="gray"
        ).pack(side=tk.LEFT, padx=10)

        # ================= SEPARADOR =================
        ttk.Separator(
            frame_botoes,
            orient=tk.VERTICAL
        ).pack(side=tk.LEFT, fill=tk.Y, padx=15)

        # ================= OTIMIZAR =================
        ttk.Button(
            frame_botoes,
            text="OTIMIZAR ROTA",
            command=self.otimizar_rota,
            width=20
        ).pack(side=tk.LEFT, padx=5)

        # ================= LIMPAR =================
        ttk.Button(
            frame_botoes,
            text="Limpar",
            command=self.limpar
        ).pack(side=tk.LEFT, padx=3)

        # ================= NOTEBOOK =================
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.notebook = ttk.Notebook(frame_principal)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # ================= ABA TABELA =================
        frame_tabela = ttk.Frame(self.notebook)

        self.notebook.add(
            frame_tabela,
            text="Tabela de Atendimentos"
        )

        colunas = (
            "ID",
            "Descrição",
            "Duração",
            "Conclusão",
            "Atraso",
            "Status"
        )

        self.tree = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings",
            height=25
        )

        col_widths = {
            "ID": 50,
            "Descrição": 250,
            "Duração": 100,
            "Conclusão": 120,
            "Atraso": 100,
            "Status": 150
        }

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths[col])

        scrollbar = ttk.Scrollbar(
            frame_tabela,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )

        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ================= ABA MÉTRICAS =================
        frame_metricas_aba = ttk.Frame(self.notebook)

        self.notebook.add(
            frame_metricas_aba,
            text="Métricas e Análise"
        )

        frame_metricas_conteudo = ttk.Frame(
            frame_metricas_aba,
            padding=20
        )

        frame_metricas_conteudo.pack(
            fill=tk.BOTH,
            expand=True
        )

        # ================= RESUMO =================
        frame_m1 = ttk.LabelFrame(
            frame_metricas_conteudo,
            text="RESUMO DA ROTA",
            padding=15
        )

        frame_m1.pack(fill=tk.X, pady=10)

        self.label_tempo_total = ttk.Label(
            frame_m1,
            text="Tempo Total: -- min",
            font=("Arial", 14, "bold")
        )

        self.label_tempo_total.pack(anchor=tk.W, pady=5)

        self.label_atraso_max = ttk.Label(
            frame_m1,
            text="Atraso Máximo: -- min",
            font=("Arial", 14, "bold"),
            foreground="#e74c3c"
        )

        self.label_atraso_max.pack(anchor=tk.W, pady=5)

        self.label_atraso_medio = ttk.Label(
            frame_m1,
            text="Atraso Médio: -- min",
            font=("Arial", 14, "bold")
        )

        self.label_atraso_medio.pack(anchor=tk.W, pady=5)

        self.label_soma_atrasos = ttk.Label(
            frame_m1,
            text="∑ Soma de Atrasos: -- min",
            font=("Arial", 14, "bold")
        )

        self.label_soma_atrasos.pack(anchor=tk.W, pady=5)

        self.label_quantidade = ttk.Label(
            frame_m1,
            text="📍 Quantidade de Atendimentos: 0",
            font=("Arial", 12)
        )

        self.label_quantidade.pack(anchor=tk.W, pady=5)

        # ================= LEGENDA =================
        frame_legenda = ttk.LabelFrame(
            frame_metricas_conteudo,
            text="LEGENDA DE CORES",
            padding=10
        )

        frame_legenda.pack(fill=tk.X, pady=20)

        # VERDE
        frame_leg1 = ttk.Frame(frame_legenda)
        frame_leg1.pack(anchor=tk.W, pady=5)

        canvas_verde = tk.Canvas(
            frame_leg1,
            width=30,
            height=30,
            bg="#27ae60",
            highlightthickness=0
        )

        canvas_verde.pack(side=tk.LEFT, padx=5)

        ttk.Label(
            frame_leg1,
            text="VERDE = Atendimento concluído dentro do prazo",
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=10)

        # VERMELHO
        frame_leg2 = ttk.Frame(frame_legenda)
        frame_leg2.pack(anchor=tk.W, pady=5)

        canvas_vermelho = tk.Canvas(
            frame_leg2,
            width=30,
            height=30,
            bg="#e74c3c",
            highlightthickness=0
        )

        canvas_vermelho.pack(side=tk.LEFT, padx=5)

        ttk.Label(
            frame_leg2,
            text="VERMELHO = Atendimento atrasado",
            font=("Arial", 11)
        ).pack(side=tk.LEFT, padx=10)

        # ================= STATUS =================
        frame_status = ttk.Frame(self.root)
        frame_status.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)

        self.label_status = ttk.Label(
            frame_status,
            text="Pronto",
            foreground="green"
        )

        self.label_status.pack(anchor=tk.W)

    def atualizar_status(self, msg, cor="green"):

        self.label_status.config(
            text=msg,
            foreground=cor
        )

        self.root.update()

    def adicionar_atendimento_manual(self):

        self.contador_atendimentos += 1

        dialogo = DialogoNovoAtendimento(
            self.root,
            self.contador_atendimentos
        )

        self.root.wait_window(dialogo)

        if dialogo.result:

            novo_atendimento = Atendimento(
                id=len(self.atendimentos) + 1,
                descricao=dialogo.result["descricao"],
                duracao=dialogo.result["duracao"],
                momento_chamado=dialogo.result["momento_chamado"]
            )

            self.atendimentos.append(novo_atendimento)

            self.atualizar_status(
                f"✓ Atendimento '{novo_atendimento.descricao}' adicionado!"
            )

            self.atualizar_display()

        else:
            self.contador_atendimentos -= 1

    def usar_exemplo(self):

        GerenciadorDados.criar_exemplo()

        self.atendimentos = GerenciadorDados.carregar_atendimentos(
            "atendimentos_exemplo.json"
        )

        self.atualizar_status(
            "✓ Dados de exemplo carregados!"
        )

        self.atualizar_display()

    def otimizar_rota(self):

        if not self.atendimentos:

            messagebox.showwarning(
                "Aviso",
                "Adicione atendimentos primeiro!"
            )

            return

        try:
            trajeto = int(self.spin_trajeto.get())
            self.duracao_trajeto = trajeto

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Valor de trajeto inválido!"
            )

            return

        self.rota_otimizada = atraso_maximo_scheduling(
            self.atendimentos,
            self.duracao_trajeto
        )

        self.atualizar_status(
            "✓ Rota otimizada!"
        )

        self.atualizar_display()

    def atualizar_display(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        atendimentos_exibir = (
            self.rota_otimizada.atendimentos
            if self.rota_otimizada
            else self.atendimentos
        )

        for att in atendimentos_exibir:

            status = ""
            cor = ""

            if att.atraso is not None:

                if att.atraso > 0:
                    status = "ATRASADO"
                    cor = "Atrasado"
                else:
                    status = "NO PRAZO"
                    cor = "NoPrazo"

            self.tree.insert(
                "",
                "end",
                values=(
                    att.id,
                    att.descricao,
                    f"{att.duracao} min",
                    f"{att.tempo_conclusao} min"
                    if att.tempo_conclusao
                    else "--",
                    f"{att.atraso} min"
                    if att.atraso is not None
                    else "--",
                    status
                ),
                tags=(cor,)
            )

        self.tree.tag_configure(
            "Atrasado",
            background="#e74c3c",
            foreground="white"
        )

        self.tree.tag_configure(
            "NoPrazo",
            background="#27ae60",
            foreground="white"
        )

        if self.rota_otimizada:

            metricas = calcular_metricas(
                self.rota_otimizada
            )

            self.label_tempo_total.config(
                text=f"⏱️ Tempo Total: {metricas['tempo_total']} min"
            )

            self.label_atraso_max.config(
                text=f"🔴 Atraso Máximo: {metricas['atraso_maximo']} min"
            )

            self.label_atraso_medio.config(
                text=f"📊 Atraso Médio: {metricas['atraso_medio']:.1f} min"
            )

            self.label_soma_atrasos.config(
                text=f"∑ Soma de Atrasos: {metricas['soma_atrasos']} min"
            )

            self.label_quantidade.config(
                text=f"📍 Quantidade de Atendimentos: {metricas['quantidade_atendimentos']}"
            )

    def limpar(self):

        self.atendimentos = []
        self.rota_otimizada = None
        self.contador_atendimentos = 0

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.label_tempo_total.config(
            text="⏱️ Tempo Total: -- min"
        )

        self.label_atraso_max.config(
            text="🔴 Atraso Máximo: -- min"
        )

        self.label_atraso_medio.config(
            text="📊 Atraso Médio: -- min"
        )

        self.label_soma_atrasos.config(
            text="∑ Soma de Atrasos: -- min"
        )

        self.label_quantidade.config(
            text="📍 Quantidade de Atendimentos: 0"
        )

        self.atualizar_status(
            "✓ Dados limpos"
        )


def iniciar_gui():

    root = tk.Tk()

    app = AmbulanciaGUI(root)

    root.mainloop()


if __name__ == "__main__":
    iniciar_gui()