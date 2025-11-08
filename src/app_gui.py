"""
=====================================================
Baixador de Vídeos Pessoal - Interface Gráfica (GUI)
=====================================================

Autor: Mark Musk - Dev Python
Data: 08/11/2025
Versão: 1.1

Descrição:
Este módulo define a classe AppGUI, responsável por construir
e gerenciar toda a interface gráfica do usuário (GUI) 
utilizando Tkinter e o tema 'ttk' para um visual mais moderno.

Requisitos Atendidos:
- FR-001: Define e organiza os widgets da interface principal.
- FR-005 (Parcial): Exibe o status "Pronto" inicial.
"""

# Importações de módulos
import tkinter as tk
from tkinter import ttk  # 'themed tk' para widgets mais modernos

class AppGUI:
    """
    Classe principal da Interface Gráfica.
    
    Esta classe encapsula todos os widgets e a lógica de interação
    da janela principal da aplicação.
    """

    def __init__(self, master: tk.Tk):
        """
        Inicializa a interface gráfica principal.

        Args:
            master (tk.Tk): A janela raiz (root) do Tkinter 
                            criada no main.py.
        """
        self.master = master
        
        # Centraliza a lógica de configuração da janela
        self._configurar_janela()
        
        # Cria os widgets (como antes)
        self._criar_widgets()
        
        # NOVO: Organiza os widgets na tela
        self._organizar_layout()

    def _configurar_janela(self):
        """
        Define as configurações iniciais da janela principal.
        """
        self.master.title("Baixador de Vídeos Pessoal v1.0")
        
        # Define um tamanho mínimo para a janela
        self.master.minsize(550, 350)
        
        # Configura o frame principal para expandir com a janela
        # (Embora o redimensionamento esteja desativado por enquanto,
        # isso é uma boa prática).
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

    def _criar_widgets(self):
        """
        Cria todos os widgets principais da aplicação, conforme FR-001.
        """
        
        # --- Frame Principal ---
        # Usamos 'sticky' para garantir que o frame se expanda
        # para preencher a janela principal.
        self.frame_principal = ttk.Frame(self.master, padding="20 20 20 20")

        # --- Seção da URL (FR-001.1) ---
        self.label_url = ttk.Label(self.frame_principal, text="Cole a URL do YouTube:")
        self.var_url = tk.StringVar() 
        self.entry_url = ttk.Entry(self.frame_principal, textvariable=self.var_url)

        # --- Botão de Download (FR-001.2) ---
        self.botao_baixar = ttk.Button(self.frame_principal, text="Baixar")

        # --- Barra de Progresso (FR-001.4) ---
        self.progress_bar = ttk.Progressbar(self.frame_principal, orient='horizontal',
                                              mode='determinate', length=100)

        # --- Feedback de Status (FR-001.3) ---
        self.text_status = tk.Text(self.frame_principal, height=10, 
                                   state="disabled", bg="#f0f0f0",
                                   wrap=tk.WORD) # Quebra de linha por palavra
        
        # --- Scrollbar para o Texto de Status ---
        self.scrollbar_status = ttk.Scrollbar(self.frame_principal, 
                                              orient=tk.VERTICAL, 
                                              command=self.text_status.yview)
        # Vincula a scrollbar ao widget de texto
        self.text_status.config(yscrollcommand=self.scrollbar_status.set)

        # Adiciona o estado inicial "Pronto" (FR-005)
        self._atualizar_status("Pronto")

    def _organizar_layout(self):
        """
        Posiciona os widgets na tela usando o gerenciador .grid().
        """
        
        # Coloca o frame principal na janela raiz (master)
        # 'sticky' (nsew) faz o frame se expandir em todas as direções
        # caso a janela seja redimensionada.
        self.frame_principal.grid(row=0, column=0, sticky="nsew")

        # --- Configuração das Colunas do Grid (Dentro do frame_principal) ---
        # Coluna 0 (labels, etc.)
        self.frame_principal.columnconfigure(0, weight=0) 
        # Coluna 1 (entry, progressbar) - se expandirá com a janela
        self.frame_principal.columnconfigure(1, weight=1)
        # Coluna 2 (botão, scrollbar)
        self.frame_principal.columnconfigure(2, weight=0)

        # --- Linha 0: Label e Entry da URL ---
        self.label_url.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        # 'sticky' (ew) faz a entry expandir horizontalmente
        self.entry_url.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # --- Linha 1: Botão de Download ---
        # O botão fica na coluna 2, alinhado à direita (east)
        self.botao_baixar.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        # --- Linha 2: Barra de Progresso ---
        # 'columnspan=3' faz a barra ocupar as 3 colunas
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky="ew", 
                               padx=5, pady=10)

        # --- Linha 3: Área de Status e Scrollbar ---
        # 'sticky' (nsew) faz a caixa de texto expandir em todas as direções
        self.text_status.grid(row=2, column=0, columnspan=2, sticky="nsew", 
                              padx=5, pady=5)
        self.scrollbar_status.grid(row=2, column=2, sticky="ns", pady=5)
        
        # Configura a linha 2 (área de texto) para expandir verticalmente
        self.frame_principal.rowconfigure(2, weight=1)


    def _atualizar_status(self, mensagem: str):
        """
        Helper para atualizar a caixa de texto de status.
        
        Agora, anexa novas mensagens em vez de apagar o histórico.

        Args:
            mensagem (str): A nova mensagem a ser exibida.
        """
        self.text_status.config(state="normal")
        
        # Insere a nova mensagem no final
        self.text_status.insert(tk.END, f"{mensagem}\n")
        
        # Auto-scroll para o final
        self.text_status.see(tk.END)
        
        self.text_status.config(state="disabled")

    def run(self):
        """
        Inicia o loop principal (mainloop) do Tkinter.
        """
        # O layout agora é chamado no __init__,
        # então o run() apenas inicia o mainloop.
        self.master.mainloop()