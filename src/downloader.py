"""
=====================================================
Baixador de Vídeos Pessoal - Lógica de Download (v2.1)
=====================================================

Autor: Mark Musk - Dev Python
Data: 09/11/2025
Versão: 2.1 (Refatorado)

Descrição:
Este módulo contém a classe VideoDownloader (yt-dlp).
Atualizado para aceitar um parâmetro de formato (mp4 ou mp3)
e ajustar as opções de download e pós-processamento do yt-dlp
de acordo.

Dependências:
- yt-dlp
- FFmpeg (essencial para o merge de mp4 e extração de mp3)
"""

# Importações de módulos
import yt_dlp
from typing import Callable

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
        Inicializa o downloader. (Sem alterações)
        """
        self.update_status = callback_status
        self.update_progress = callback_progress
        self.notify_error = callback_error
        self.notify_complete = callback_complete

        self.caminho_final = ""

    def _yt_dlp_hook(self, d: dict):
        """
        Hook (callback) chamado pelo yt-dlp. (Sem alterações)
        """
        
        if d['status'] == 'downloading':
            if '_percent_str' in d:
                percent_str = d['_percent_str'].strip().replace('%', '')
                try:
                    # Se for MP3, o "download" é tudo (não há merge)
                    # Se for MP4, 90% é download, 10% é merge
                    # (Vamos simplificar e deixar 90% para download em ambos)
                    percent = float(percent_str) * 0.9
                    self.update_progress(int(percent))
                except ValueError:
                    pass
        
        elif d['status'] == 'postprocessing':
            # Isso agora captura tanto o merge (MP4) quanto a extração (MP3)
            self.update_status("Pós-processando (FFmpeg)...")
            self.update_progress(95)
            
        elif d['status'] == 'finished':
            self.update_progress(100)
            self.notify_complete(f"Download Concluído!\nSalvo em: {self.caminho_final}")
        
        elif d['status'] == 'error':
            self.notify_error(f"Erro durante o download: {d.get('filename', 'N/A')}")


    def iniciar_download(self, url: str, caminho_final: str, formato_escolhido: str):
        """
        (MODIFICADO)
        Ponto de entrada principal para iniciar o processo de download.
        Agora aceita 'formato_escolhido' para definir as opções.

        Args:
            url (str): A URL do vídeo do YouTube.
            caminho_final (str): O caminho completo onde o arquivo
                                 final deve ser salvo.
            formato_escolhido (str): "mp4" ou "mp3".
        """
        try:
            self.update_status("Iniciando yt-dlp...")
            self.update_progress(0)
            self.caminho_final = caminho_final

            # --- (MODIFICADO) Configuração dinâmica das Opções do yt-dlp ---
            
            ydl_opts = {
                'outtmpl': caminho_final,
                'progress_hooks': [self._yt_dlp_hook],
                'postprocessor_hooks': [self._yt_dlp_hook],
                'noprogress': True,
                'quiet': True,
                'warning': self.update_status,
                'noplaylist': True,
            }

            if formato_escolhido == "mp3":
                # --- Opções para MP3 (Extração de Áudio) ---
                self.update_status("Configurando para extração de áudio (MP3)...")
                
                # 1. Pede o melhor áudio disponível
                ydl_opts['format'] = 'bestaudio/best'
                
                # 2. Define o pós-processador para extrair e converter
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio', # Usa FFmpeg
                    'preferredcodec': 'mp3',       # Converte para MP3
                    'preferredquality': '192',     # Qualidade (192k é um bom padrão)
                }]
                
                # O 'outtmpl' já está correto (ex: 'video.mp3'),
                # o yt-dlp gerencia a troca de extensão.

            else: # O padrão é MP4
                # --- Opções para MP4 (Vídeo + Áudio) ---
                self.update_status("Configurando para download de vídeo (MP4)...")
                
                # (FR-003) Pede o melhor vídeo e áudio MP4 e os junta
                ydl_opts['format'] = ('bestvideo[ext=mp4]+bestaudio[ext=m4a]/'
                                      'best[ext=mp4]/best')
                
                # O 'outtmpl' (ex: 'video.mp4') e o FFmpeg
                # farão o merge automaticamente.

            # --- Fim da Configuração ---

            self.update_status("Validando URL e buscando streams...")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except yt_dlp.utils.DownloadError as e:
            self.update_status(f"Erro do yt-dlp: {e}")
            self.notify_error(f"Falha no Download:\n{e}")
            
        except Exception as e:
            self.update_status(f"Erro inesperado: {e}")
            self.notify_error(f"Falha inesperada:\n{e}")