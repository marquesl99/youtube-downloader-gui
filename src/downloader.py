"""
=====================================================
Baixador de Vídeos Pessoal - Lógica de Download
=====================================================

Autor: Mark Musk - Dev Python
Data: 08/11/2025
Versão: 1.0

Descrição:
Este módulo contém a classe VideoDownloader, responsável por
toda a lógica de interação com o pytube, seleção de streams
(FR-003), download e merge de arquivos usando FFmpeg (FR-003).

Esta classe é desacoplada da GUI e comunica seu estado
através de callbacks.

Dependências:
- pytube (instalado via requirements.txt)
- FFmpeg (Requisito NFR-004): Deve estar instalado no sistema
  e acessível no PATH do ambiente.
"""

# Importações de módulos
import os
import subprocess # Para chamar o FFmpeg
from pytube import YouTube
from typing import Callable # Para tipagem dos callbacks

# --- Constantes ---
# Usaremos nomes de arquivos temporários para o merge
TEMP_VIDEO_FILE = "temp_video.mp4"
TEMP_AUDIO_FILE = "temp_audio.mp4"

class VideoDownloader:
    """
    Encapsula toda a lógica de download e processamento do vídeo.
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
        self.yt = None
        
        # --- Callbacks ---
        # Funções que a GUI nos passará para atualizarmos o status
        # sem que esta classe precise "conhecer" o Tkinter.
        self.update_status = callback_status
        self.update_progress = callback_progress
        self.notify_error = callback_error
        self.notify_complete = callback_complete
        
        # Registra a função de progresso no pytube
        # (Isso será feito após carregar o vídeo)

    def _on_pytube_progress(self, stream, chunk, bytes_remaining):
        """
        Callback interno chamado pelo pytube durante o download.
        
        Calcula a porcentagem baixada e chama o callback de progresso
        fornecido pela GUI.
        """
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        
        # Calcula a porcentagem
        # Usamos 90% como teto, pois os 10% finais serão o merge
        percentage = (bytes_downloaded / total_size) * 100
        
        # Reportamos o progresso (limitado a 90% da barra total)
        # O merge do FFmpeg preencherá os 10% restantes.
        self.update_progress(int(percentage * 0.9))

    def _limpar_temporarios(self):
        """
        Remove os arquivos temporários de áudio e vídeo.
        """
        self.update_status("Limpando arquivos temporários...")
        if os.path.exists(TEMP_VIDEO_FILE):
            os.remove(TEMP_VIDEO_FILE)
        if os.path.exists(TEMP_AUDIO_FILE):
            os.remove(TEMP_AUDIO_FILE)

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
            self.update_status("Validando URL e conectando ao YouTube...")
            self.update_progress(0)
            
            self.yt = YouTube(url, on_progress_callback=self._on_pytube_progress)

            # --- FR-003: Lógica de Melhor Qualidade ---
            self.update_status(f"Buscando streams para: {self.yt.title}")
            
            # 1. Melhor Stream de Vídeo (adaptativo, .mp4, apenas vídeo)
            video_stream = self.yt.streams.filter(
                adaptive=True, file_extension='mp4', only_video=True
            ).order_by('resolution').desc().first()
            
            # 2. Melhor Stream de Áudio (adaptativo, .mp4, apenas áudio)
            audio_stream = self.yt.streams.filter(
                adaptive=True, file_extension='mp4', only_audio=True
            ).order_by('abr').desc().first()

            if not video_stream or not audio_stream:
                raise ValueError("Não foi possível encontrar streams adaptativos de áudio/vídeo.")

            # --- Download ---
            self.update_status(f"Baixando vídeo ({video_stream.resolution})...")
            video_stream.download(filename=TEMP_VIDEO_FILE)
            
            self.update_status(f"Baixando áudio ({audio_stream.abr})...")
            # Reinicia o progresso para o download do áudio (ainda nos 90%)
            self.update_progress(0) 
            audio_stream.download(filename=TEMP_AUDIO_FILE)

            # --- Merge com FFmpeg (FR-003, NFR-004) ---
            self.update_status("Juntando áudio e vídeo com FFmpeg...")
            self.update_progress(90) # Progresso salta para 90%

            # Comando FFmpeg:
            # -i video -i audio : define as entradas
            # -c:v copy -c:a copy : copia os codecs sem re-encodar (rápido)
            # -y : sobrescreve o arquivo de saída se existir
            cmd = [
                'ffmpeg',
                '-i', TEMP_VIDEO_FILE,
                '-i', TEMP_AUDIO_FILE,
                '-c:v', 'copy',
                '-c:a', 'copy',
                '-y', # Sobrescreve o arquivo final
                caminho_final
            ]

            # Usamos subprocess.run para chamar o FFmpeg
            # 'stdout' e 'stderr' capturam a saída para depuração
            # 'check=True' lança exceção se o FFmpeg falhar
            resultado = subprocess.run(cmd, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE, 
                                     text=True, 
                                     check=True)

            self.update_progress(100)
            self.update_status("Merge concluído.")
            self.notify_complete(f"Download Concluído!\nSalvo em: {caminho_final}")

        except subprocess.CalledProcessError as e:
            # Erro específico do FFmpeg
            self.update_status("Erro no FFmpeg. Verifique a instalação.")
            self.notify_error(f"Erro no FFmpeg:\n{e.stderr}")
            
        except Exception as e:
            # Erro geral (URL inválida, rede, pytube, etc.)
            self.update_status(f"Erro: {e}")
            self.notify_error(f"Falha no Download:\n{e}")
            
        finally:
            # Garante que os arquivos temporários sejam limpos
            self._limpar_temporarios()