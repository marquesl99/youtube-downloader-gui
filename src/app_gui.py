"""
=====================================================
Baixador de Vídeos Pessoal - Interface Gráfica (GUI)
=====================================================

Autor: Mark Musk - Dev Python
Data: 08/11/2025
Versão: 1.2

Descrição:
Este módulo define a classe AppGUI, responsável por construir
e gerenciar toda a interface gráfica do usuário (GUI).
Agora inclui a lógica para threading (NFR-002), seleção de
local (FR-002) e comunicação com o módulo downloader.py.

Requisitos Atendidos:
- FR-001, FR-002, FR-004, FR-005, NFR-002
"""

# Importações de módulos
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog  # (FR-002) Para a janela "Salvar Como"
from tkinter import messagebox  # Para exibir erros
import threading              # (NFR-002) Para evitar congelamento da GUI

# Importação do nosso módulo de lógica
from downloader import VideoDownloader

class AppGUI:
    """
    Classe principal da Interface Gráfica.
    
    Encapsula widgets, lógica de layout e a comunicação
    com a thread de download.
    """

    def __init__(self, master: tk.Tk):
        """
        Inicializa a interface gráfica principal.

        Args:
            master (tk.Tk): A janela raiz (root) do Tkinter.
        """
        self.master = master
        
        self._configurar_janela()
        self._criar_widgets()
        self._organizar_layout()
        
        # --- Instanciação do Downloader ---
        # Instanciamos o downloader, passando os métodos "seguros"
        # (thread-safe) como callbacks.
        self.downloader = VideoDownloader(
            callback_status=self._safe_update_status,
            callback_progress=self._safe_update_progress,
            callback_error=self._safe_notify_error,
            callback_complete=self._safe_notify_complete
        )

    def _configurar_janela(self):
        self.master.title("Baixador de Vídeos Pessoal v1.0")
        self.master.minsize(550, 350)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

    def _criar_widgets(self):
        # (Criação de widgets... igual à versão anterior)
        
        self.frame_principal = ttk.Frame(self.master, padding="20 20 20 20")

        self.label_url = ttk.Label(self.frame_principal, text="Cole a URL do YouTube:")
        self.var_url = tk.StringVar()
        self.entry_url = ttk.Entry(self.frame_principal, textvariable=self.var_url)

        # --- Botão de Download (FR-001.2) ---
        # NOVO: Conectamos o 'command' ao método _iniciar_download
        self.botao_baixar = ttk.Button(
            self.frame_principal, 
            text="Baixar",
            command=self._iniciar_download # Conecta o clique à função
        )

        self.progress_bar = ttk.Progressbar(self.frame_principal, orient='horizontal',
                                              mode='determinate', length=100)

        self.text_status = tk.Text(self.frame_principal, height=10, 
                                   state="disabled", bg="#f0f0f0",
                                   wrap=tk.WORD)
        
        self.scrollbar_status = ttk.Scrollbar(self.frame_principal, 
                                              orient=tk.VERTICAL, 
                                              command=self.text_status.yview)
        self.text_status.config(yscrollcommand=self.scrollbar_status.set)

        self._log_status("Pronto") # Renomeado de _atualizar_status

    def _organizar_layout(self):
        # (Organização do layout... igual à versão anterior)
        self.frame_principal.grid(row=0, column=0, sticky="nsew")

        self.frame_principal.columnconfigure(1, weight=1)

        self.label_url.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_url.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.botao_baixar.grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky="ew", 
                               padx=5, pady=10)
        self.text_status.grid(row=2, column=0, columnspan=2, sticky="nsew", 
                              padx=5, pady=5)
        self.scrollbar_status.grid(row=2, column=2, sticky="ns", pady=5)
        
        self.frame_principal.rowconfigure(2, weight=1)

    # --- Lógica de Download e Threading ---

    def _iniciar_download(self):
        """
        Função chamada pelo clique no botão "Baixar".
        
        Valida a URL, abre a janela "Salvar Como" (FR-002) e
        dispara a thread de download (NFR-002).
        """
        url = self.var_url.get()
        if not url:
            messagebox.showwarning("URL Vazia", "Por favor, cole uma URL do YouTube.")
            return

        # --- FR-002: Seleção de Local de Salvamento ---
        # Abre a janela nativa "Salvar Como..."
        caminho_final = filedialog.asksaveasfilename(
            title="Salvar vídeo como...",
            defaultextension=".mp4",
            filetypes=[("Arquivos MP4", "*.mp4"), ("Todos os arquivos", "*.*")]
        )

        # Se o usuário cancelar a janela (caminho_final fica vazio)
        if not caminho_final:
            self._log_status("Download cancelado pelo usuário.")
            return

        # --- NFR-002: Despachando a Thread ---
        try:
            # Desabilita os widgets para evitar downloads múltiplos
            self._set_ui_state(ativo=False)
            
            # Limpa a barra de progresso
            self._safe_update_progress(0)
            
            self._log_status(f"Iniciando download para: {url}")

            # Cria a thread que executará o download
            self.download_thread = threading.Thread(
                target=self.downloader.iniciar_download,
                args=(url, caminho_final),
                daemon=True # Permite que a app feche mesmo se a thread travar
            )
            self.download_thread.start()

        except Exception as e:
            self._safe_notify_error(f"Erro ao iniciar a thread: {e}")

    def _set_ui_state(self, ativo: bool):
        """
        Habilita ou desabilita os controles da interface
        para prevenir ações do usuário durante o download.
        """
        estado_botao = "normal" if ativo else "disabled"
        estado_entry = "normal" if ativo else "readonly"
        
        self.botao_baixar.config(state=estado_botao)
        self.entry_url.config(state=estado_entry)
    
    # --- Métodos de Callback (Thread-Safe) ---
    # Estes métodos são chamados pelo VideoDownloader (de outra thread)
    # e usam 'self.master.after' para agendar a atualização na
    # thread principal da GUI, evitando conflitos.

    def _safe_update_status(self, mensagem: str):
        """Callback thread-safe para atualizar o log de status."""
        self.master.after(0, self._log_status, mensagem)

    def _safe_update_progress(self, valor: int):
        """Callback thread-safe para atualizar a barra de progresso (FR-004)."""
        self.master.after(0, lambda: self.progress_bar.config(value=valor))

    def _safe_notify_error(self, erro_msg: str):
        """Callback thread-safe para notificar erros (FR-005)."""
        # Agendamos duas ações: mostrar o erro e reativar a UI
        self.master.after(0, lambda: messagebox.showerror("Erro no Download", erro_msg))
        self.master.after(0, self._set_ui_state, True)
        self.master.after(0, self._safe_update_progress, 0) # Reseta a barra

    def _safe_notify_complete(self, msg_final: str):
        """Callback thread-safe para notificar conclusão (FR-005)."""
        self.master.after(0, self._log_status, msg_final)
        self.master.after(0, self._set_ui_state, True)

    def _log_status(self, mensagem: str):
        """
        (Anteriormente _atualizar_status)
        Insere mensagens na caixa de texto de status.
        Este método DEVE ser chamado apenas pela thread principal (ou via _safe_update_status).
        """
        self.text_status.config(state="normal")
        self.text_status.insert(tk.END, f"{mensagem}\n")
        self.text_status.see(tk.END) # Auto-scroll
        self.text_status.config(state="disabled")

    def run(self):
        """
        Inicia o loop principal (mainloop) do Tkinter.
        """
        self.master.mainloop()