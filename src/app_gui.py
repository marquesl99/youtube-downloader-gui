"""
=====================================================
Baixador de Vídeos Pessoal - Interface Gráfica (GUI)
=====================================================

Autor: Mark Musk - Dev Python
Data: 08/11/2025
Versão: 1.0

Descrição:
Este módulo define a classe AppGUI, responsável por construir
e gerenciar toda a interface gráfica do usuário (GUI) 
utilizando Tkinter e o tema 'ttk' para um visual mais moderno.

Requisitos Atendidos:
- FR-001 (Parcial): Define os widgets da interface principal.
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
        self._configurar_janela()
        self._criar_widgets()

    def _configurar_janela(self):
        """
        Define as configurações iniciais da janela principal.
        """
        self.master.title("Baixador de Vídeos Pessoal v1.0")
        self.master.geometry("600x400")  # Tamanho inicial (Largura x Altura)
        self.master.resizable(False, False) # Impede redimensionamento

    def _criar_widgets(self):
        """
        Cria todos os widgets principais da aplicação, conforme FR-001.
        
        Neste momento, os widgets são apenas criados (instanciados),
        mas ainda não posicionados na tela.
        """
        
        # --- Frame Principal ---
        # Usaremos um frame principal com padding para organizar o conteúdo
        self.frame_principal = ttk.Frame(self.master, padding="20 20 20 20")

        # --- Seção da URL (FR-001.1) ---
        self.label_url = ttk.Label(self.frame_principal, text="Cole a URL do YouTube:")
        self.var_url = tk.StringVar() # Variável para armazenar o texto da entry
        self.entry_url = ttk.Entry(self.frame_principal, textvariable=self.var_url, width=60)

        # --- Botão de Download (FR-001.2) ---
        self.botao_baixar = ttk.Button(self.frame_principal, text="Baixar")
                                      # (A lógica de clique será adicionada depois)

        # --- Barra de Progresso (FR-001.4) ---
        self.progress_bar = ttk.Progressbar(self.frame_principal, orient='horizontal',
                                              mode='determinate', length=100)

        # --- Feedback de Status (FR-001.3) ---
        # Usaremos um 'Text' por permitir múltiplas linhas e scroll,
        # mas o desabilitamos para que o usuário não possa digitar.
        self.text_status = tk.Text(self.frame_principal, height=10, width=70, 
                                   state="disabled", bg="#f0f0f0")
        
        # Adiciona um estado inicial "Pronto" (FR-005)
        self._atualizar_status("Pronto")

    def _atualizar_status(self, mensagem: str):
        """
        Helper para atualizar a caixa de texto de status.
        
        (Este método será expandido futuramente para lidar com
         logs de múltiplas linhas).

        Args:
            mensagem (str): A nova mensagem a ser exibida.
        """
        # Habilita o widget temporariamente para inserir texto
        self.text_status.config(state="normal")
        
        # Limpa o conteúdo antigo e insere o novo
        # (Futuramente, podemos querer anexar mensagens em vez de limpar)
        self.text_status.delete("1.0", tk.END) 
        self.text_status.insert(tk.END, f"Status: {mensagem}\n")
        
        # Desabilita novamente para evitar edição pelo usuário
        self.text_status.config(state="disabled")

    def run(self):
        """
        Inicia o loop principal (mainloop) do Tkinter.
        """
        # Antes de iniciar o loop, precisamos posicionar os widgets
        # que criamos. Vamos fazer isso na próxima etapa.
        
        # Por enquanto, apenas o frame principal
        self.frame_principal.pack(expand=True, fill=tk.BOTH)
        
        # (Aqui virá a lógica de layout dos outros widgets)
        
        print("Iniciando a interface gráfica...")
        self.master.mainloop()