"""
=====================================================
Baixador de Vídeos Pessoal - Interface Gráfica (GUI)
=====================================================

Autor: Mark Musk - Dev Python
Data: 09/11/2025
Versão: 1.3

Descrição:
Este módulo define a classe AppGUI.
Versão atualizada para incluir a seleção de formato de 
download (MP4 ou MP3).

Requisitos Atendidos:
- FR-001, FR-002, FR-004, FR-005, NFR-002
- (NOVO) Suporte à seleção de formato na GUI.
"""

# Importações de módulos
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading

# Importação do nosso módulo de lógica
from downloader import VideoDownloader

class AppGUI:
    """
    Classe principal da Interface Gráfica.
    """

    def __init__(self, master: tk.Tk):
        """
        Inicializa a interface gráfica principal.
        """
        self.master = master
        
        self._configurar_janela()
        self._criar_widgets()
        self._organizar_layout()
        
        # Instanciação do Downloader (sem alteração)
        self.downloader = VideoDownloader(
            callback_status=self._safe_update_status,
            callback_progress=self._safe_update_progress,
            callback_error=self._safe_notify_error,
            callback_complete=self._safe_notify_complete
        )

    def _configurar_janela(self):
        self.master.title("Baixador de Vídeos Pessoal v1.1") # (Versão atualizada)
        self.master.minsize(550, 380) # (Altura levemente aumentada)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

    def _criar_widgets(self):
        """
        Cria todos os widgets principais da aplicação.
        """
        
        self.frame_principal = ttk.Frame(self.master, padding="20 20 20 20")

        # --- Seção da URL (Sem alteração) ---
        self.label_url = ttk.Label(self.frame_principal, text="Cole a URL do YouTube:")
        self.var_url = tk.StringVar()
        self.entry_url = ttk.Entry(self.frame_principal, textvariable=self.var_url)

        # --- Botão de Download (Sem alteração no widget) ---
        self.botao_baixar = ttk.Button(
            self.frame_principal, 
            text="Baixar",
            command=self._iniciar_download
        )

        # --- (NOVO) Seção de Seleção de Formato ---
        self.var_formato = tk.StringVar(value="mp4") # Valor padrão é 'mp4'
        self.frame_formatos = ttk.Frame(self.frame_principal) # Frame para agrupar os botões

        self.radio_mp4 = ttk.Radiobutton(
            self.frame_formatos, 
            text="Vídeo (MP4)", 
            variable=self.var_formato, 
            value="mp4"
        )
        self.radio_mp3 = ttk.Radiobutton(
            self.frame_formatos, 
            text="Áudio (MP3)", 
            variable=self.var_formato, 
            value="mp3"
        )

        # --- Barra de Progresso (Sem alteração) ---
        self.progress_bar = ttk.Progressbar(self.frame_principal, orient='horizontal',
                                              mode='determinate', length=100)

        # --- Feedback de Status (Sem alteração) ---
        self.text_status = tk.Text(self.frame_principal, height=10, 
                                   state="disabled", bg="#f0f0f0",
                                   wrap=tk.WORD)
        self.scrollbar_status = ttk.Scrollbar(self.frame_principal, 
                                              orient=tk.VERTICAL, 
                                              command=self.text_status.yview)
        self.text_status.config(yscrollcommand=self.scrollbar_status.set)

        self._log_status("Pronto")

    def _organizar_layout(self):
        """
        Posiciona os widgets na tela usando o gerenciador .grid().
        (Layout atualizado para incluir os seletores de formato).
        """
        
        self.frame_principal.grid(row=0, column=0, sticky="nsew")

        # Configuração das Colunas (Col 1 se expande)
        self.frame_principal.columnconfigure(1, weight=1)

        # --- Linha 0: URL e Botão de Baixar (Sem alteração) ---
        self.label_url.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_url.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.botao_baixar.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        # --- (NOVO) Linha 1: Seleção de Formato ---
        # Ocupa as 3 colunas, botões centralizados
        self.frame_formatos.grid(row=1, column=0, columnspan=3, pady=8)
        # Organiza os Radiobuttons dentro do seu próprio frame
        self.radio_mp4.pack(side=tk.LEFT, padx=10)
        self.radio_mp3.pack(side=tk.LEFT, padx=10)

        # --- (MODIFICADO) Linha 2: Barra de Progresso ---
        # (Movida da linha 1 para a linha 2)
        self.progress_bar.grid(row=2, column=0, columnspan=3, sticky="ew", 
                               padx=5, pady=10)

        # --- (MODIFICADO) Linha 3: Área de Status e Scrollbar ---
        # (Movida da linha 2 para a linha 3)
        self.text_status.grid(row=3, column=0, columnspan=2, sticky="nsew", 
                              padx=5, pady=5)
        self.scrollbar_status.grid(row=3, column=2, sticky="ns", pady=5)
        
        # (MODIFICADO) Configura a linha 3 para expandir
        self.frame_principal.rowconfigure(3, weight=1)

    # --- Lógica de Download e Threading ---

    def _iniciar_download(self):
        """
        (MODIFICADO)
        Função chamada pelo clique no botão "Baixar".
        Agora lê o formato selecionado e o passa adiante.
        """
        url = self.var_url.get()
        if not url:
            messagebox.showwarning("URL Vazia", "Por favor, cole uma URL do YouTube.")
            return

        # --- (NOVO) Lê a escolha do formato ---
        formato_escolhido = self.var_formato.get() # Será "mp4" ou "mp3"

        # --- (MODIFICADO) FR-002: Seleção de Local de Salvamento ---
        # Define os tipos de arquivo e extensão padrão com base na escolha
        if formato_escolhido == "mp4":
            extensao_padrao = ".mp4"
            tipos_arquivo = [("Arquivos MP4", "*.mp4"), ("Todos os arquivos", "*.*")]
        else: # mp3
            extensao_padrao = ".mp3"
            tipos_arquivo = [("Arquivos MP3", "*.mp3"), ("Todos os arquivos", "*.*")]

        caminho_final = filedialog.asksaveasfilename(
            title="Salvar arquivo como...",
            defaultextension=extensao_padrao,
            filetypes=tipos_arquivo
        )

        if not caminho_final:
            self._log_status("Download cancelado pelo usuário.")
            return

        # --- (MODIFICADO) NFR-002: Despachando a Thread ---
        try:
            self._set_ui_state(ativo=False)
            self._safe_update_progress(0)
            self._log_status(f"Iniciando download ({formato_escolhido.upper()}) para: {url}")

            # Atualiza a chamada para passar o formato escolhido
            self.download_thread = threading.Thread(
                target=self.downloader.iniciar_download,
                args=(url, caminho_final, formato_escolhido), # (NOVO PARÂMETRO)
                daemon=True 
            )
            self.download_thread.start()

        except Exception as e:
            self._safe_notify_error(f"Erro ao iniciar a thread: {e}")

    # --- (Restante dos métodos _set_ui_state, callbacks e run sem alteração) ---

    def _set_ui_state(self, ativo: bool):
        estado_botao = "normal" if ativo else "disabled"
        estado_entry = "normal" if ativo else "readonly"
        
        self.botao_baixar.config(state=estado_botao)
        self.entry_url.config(state=estado_entry)
        # (NOVO) Desabilita os radio buttons durante o download
        self.radio_mp4.config(state=estado_botao)
        self.radio_mp3.config(state=estado_botao)
    
    # ... (callbacks _safe_... e _log_status permanecem iguais) ...

    def _safe_update_status(self, mensagem: str):
        self.master.after(0, self._log_status, mensagem)

    def _safe_update_progress(self, valor: int):
        self.master.after(0, lambda: self.progress_bar.config(value=valor))

    def _safe_notify_error(self, erro_msg: str):
        self.master.after(0, lambda: messagebox.showerror("Erro no Download", erro_msg))
        self.master.after(0, self._set_ui_state, True)
        self.master.after(0, self._safe_update_progress, 0)

    def _safe_notify_complete(self, msg_final: str):
        self.master.after(0, self._log_status, msg_final)
        self.master.after(0, self._set_ui_state, True)

    def _log_status(self, mensagem: str):
        self.text_status.config(state="normal")
        self.text_status.insert(tk.END, f"{mensagem}\n")
        self.text_status.see(tk.END)
        self.text_status.config(state="disabled")

    def run(self):
        self.master.mainloop()