"""
=====================================================
Baixador de Vídeos Pessoal - Lógica de Download (v2.0)
=====================================================

Autor: Mark Musk - Dev Python
Data: 08/11/2025
Versão: 2.0 (Refatorado)

Descrição:
Este módulo contém a classe VideoDownloader, agora refatorada
para usar a biblioteca 'yt-dlp' em vez do 'pytube'.
'yt-dlp' é mais robusta contra atualizações de API do YouTube
e gerencia nativamente o merge de áudio e vídeo (FR-003).

Dependências:
- yt-dlp (instalado via requirements.txt)
- FFmpeg (Requisito NFR-004): 'yt-dlp' depende dele para
  fazer o merge de streams de alta qualidade.
"""

# Importações de módulos
import yt_dlp  # A nova biblioteca de download
from typing import Callable # Para tipagem dos callbacks

class VideoDownloader:
    """
    Encapsula toda a lógica de download e processamento do vídeo
    usando a API Python do yt-dlp.
    """

    def __init__(self, 
                 callback_status: Callable[[str], None],
                 callback_progress: Callable[[int], None],
                 callback_error: Callable[[str], None],
                 callback_complete: Callable[[str], None]):
        """
        Inicializa o downloader.

        Args:
            callback_status (Callable): Função chamada para atualizar 
                                        mensagens de status.
            callback_progress (Callable): Função chamada para atualizar 
                                          a barra de progresso (0-100).
            callback_error (Callable): Função chamada quando um erro ocorre.
            callback_complete (Callable): Função chamada ao concluir com sucesso.
        """
        # --- Callbacks ---
        # Estes são os mesmos métodos "seguros" da AppGUI
        self.update_status = callback_status
        self.update_progress = callback_progress
        self.notify_error = callback_error
        self.notify_complete = callback_complete

        # Variável para armazenar o caminho final
        self.caminho_final = ""

    def _yt_dlp_hook(self, d: dict):
        """
        Hook (callback) chamado pelo yt-dlp durante o processo.
        
        Este método recebe um dicionário 'd' com o status
        atual do download e pós-processamento.

        Args:
            d (dict): Dicionário de status do yt-dlp.
        """
        
        # --- Feedback de Status (FR-005) ---
        if d['status'] == 'downloading':
            # Captura a porcentagem do download
            # O yt-dlp formata a string, ex: " 10.5%"
            if '_percent_str' in d:
                percent_str = d['_percent_str'].strip().replace('%', '')
                try:
                    # Usamos 90% da barra para o download, 10% para o merge
                    percent = float(percent_str) * 0.9
                    self.update_progress(int(percent))
                except ValueError:
                    pass # Ignora se a string não for um número
        
        # --- Pós-processamento (Merge FFmpeg) ---
        elif d['status'] == 'postprocessing':
            # Quando o FFmpeg é chamado para o merge
            self.update_status("Juntando áudio e vídeo com FFmpeg...")
            # Avança a barra para 95% para indicar o merge
            self.update_progress(95)
            
        # --- Conclusão ---
        elif d['status'] == 'finished':
            self.update_progress(100)
            # O 'filename' em 'd' pode não ser o caminho final exato
            # que definimos, então usamos o que salvamos.
            self.notify_complete(f"Download Concluído!\nSalvo em: {self.caminho_final}")
        
        # --- Erros ---
        elif d['status'] == 'error':
            self.notify_error(f"Erro durante o download: {d.get('filename', 'N/A')}")


    def iniciar_download(self, url: str, caminho_final: str):
        """
        Ponto de entrada principal para iniciar o processo de download.
        
        Este método executa em uma thread separada (gerenciada pela GUI).

        Args:
            url (str): A URL do vídeo do YouTube.
            caminho_final (str): O caminho completo onde o arquivo
                                 final deve ser salvo.
        """
        try:
            self.update_status("Iniciando yt-dlp...")
            self.update_progress(0)
            self.caminho_final = caminho_final

            # --- Configuração das Opções do yt-dlp ---
            
            # FR-003: "bestvideo..." seleciona o melhor vídeo MP4
            #         "+bestaudio..." seleciona o melhor áudio M4A
            #         "/best[ext=mp4]" fallback se não houver streams separados
            #         "/best" fallback final
            # Isso exige que o FFmpeg esteja no PATH (NFR-004)
            
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': caminho_final,  # (FR-002) Onde salvar o arquivo
                'progress_hooks': [self._yt_dlp_hook], # (FR-004) Callback de progresso
                'postprocessor_hooks': [self._yt_dlp_hook], # Captura o 'finished'
                'noprogress': True, # Desliga o logger de progresso padrão
                'quiet': True, # Suprime a saída padrão
                'warning': self.update_status, # Redireciona warnings
                'noplaylist': True, # (Ref: Fora do Escopo) Garante 1 vídeo
            }

            self.update_status("Validando URL e buscando streams...")
            
            # Instancia e executa o download
            # yt_dlp.YoutubeDL é o objeto principal
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url]) # Inicia o download

        except yt_dlp.utils.DownloadError as e:
            # Erro específico do yt-dlp (ex: URL inválida, vídeo indisponível)
            self.update_status(f"Erro do yt-dlp: {e}")
            self.notify_error(f"Falha no Download:\n{e}")
            
        except Exception as e:
            # Erro geral (ex: permissão de escrita no disco)
            self.update_status(f"Erro inesperado: {e}")
            self.notify_error(f"Falha inesperada:\n{e}")