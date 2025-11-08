## Baixador de Vídeos Pessoal (YouTube Downloader GUI)

> Interface gráfica simples para baixar vídeos do YouTube usando `yt-dlp` e `ffmpeg`.

### Visão geral

Este projeto fornece uma GUI leve em Python (Tkinter) para baixar vídeos do YouTube. Cole a URL, escolha onde salvar o arquivo e clique em "Baixar" — a aplicação usa `yt-dlp` para obter os melhores streams disponíveis e `ffmpeg` para juntar áudio e vídeo quando necessário.

Principais características
- Interface gráfica simples (Tkinter)
- Usa `yt-dlp` para downloads robustos
- Suporte a seleção de local de salvamento (Salvar como...)
- Barra de progresso e log de status
- Download em thread para não travar a GUI

## Requisitos

- Python 3.8+ (testado com 3.10/3.11)
- Dependências Python listadas em `requirements.txt` (principal: `yt-dlp`)
- FFmpeg disponível no PATH (necessário para mesclar áudio/vídeo em certas streams)

Observação: `ffmpeg` não é um pacote Python. No Windows você pode instalá-lo manualmente (baixando o binário) ou via gerenciadores como `choco` / `winget` se disponíveis.

## Instalação (Windows - PowerShell)

1. Crie um ambiente virtual (opcional, recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale as dependências:

```powershell
pip install -r requirements.txt
```

3. Verifique se o `ffmpeg` está disponível (no PATH):

```powershell
ffmpeg -version
```

Se o comando acima falhar, instale o FFmpeg e adicione-o ao PATH do sistema.

## Como usar (GUI)

Execute a aplicação a partir da raiz do projeto usando o arquivo `main.py` dentro da pasta `src`:

```powershell
python src\main.py
```

Alternativa (entre na pasta `src` e execute `main.py`):

```powershell
cd src
python main.py
```

Fluxo de uso:
1. Cole a URL do vídeo do YouTube no campo "Cole a URL do YouTube".
2. Clique em "Baixar".
3. Escolha o local e nome do arquivo via a janela "Salvar como...".
4. A barra de progresso e o log exibirão o andamento e mensagens (merge via FFmpeg, conclusão, erros).

Observações:
- Se a URL apontar para um vídeo com streams separados (vídeo + áudio), o `yt-dlp` baixará as melhores streams e usará o `ffmpeg` para juntar (merge).
- Caso o usuário cancele a seleção de arquivo, o download será cancelado.

## Uso programático

O módulo `src/downloader.py` expõe a classe `VideoDownloader` que pode ser reutilizada em outros scripts. Ela aceita callbacks para atualizar status, progresso, erros e conclusão.

Exemplo mínimo (esquema):

```python
from src.downloader import VideoDownloader

def status(msg):
    print(msg)

def progress(p):
    print(p)

vd = VideoDownloader(status, progress, lambda e: print(e), lambda f: print(f))
vd.iniciar_download("https://www.youtube.com/watch?v=...", "C:\\meus_videos\\video.mp4")
```

## Testes

O repositório inclui uma pasta `tests/`. Para rodar os testes com o unittest embutido:

```powershell
python -m unittest discover -v
```

Se preferir usar `pytest`, instale-o (`pip install pytest`) e execute `pytest`.

## Problemas comuns e solução

- Erro: "ffmpeg: comando não encontrado" — Instale o FFmpeg e adicione-o ao PATH.
- Permissão negada ao salvar — Verifique se você tem permissão de escrita no diretório escolhido.
- URL inválida ou vídeo não disponível — confirme a URL no navegador; alguns vídeos podem ter restrições.

## Contribuindo

Contribuições são bem-vindas. Boas formas de colaborar:
- Abrir issues com bugs ou sugestões
- Enviar pull requests com correções ou melhorias (ex.: suporte a pastas, escolha de qualidade, tradução)

Antes de enviar PRs, por favor:
1. Abra uma issue descrevendo a mudança proposta.
2. Garanta que o código esteja formatado no estilo do projeto e que testes (se aplicáveis) passem.

## Licença

Nenhuma licença explícita foi encontrada neste repositório. Se você é o autor e deseja disponibilizar o código publicamente, adicione um arquivo `LICENSE` (por exemplo, MIT) para deixar os termos claros.

## Contato

Se precisar de ajuda ou quiser reportar algo específico, abra uma issue neste repositório ou adicione comentários no código.

---

Arquivo adicionado automaticamente: `README.md` — descrição, instalação e instruções de uso para Windows/PowerShell.
# youtube-downloader-gui
Script em Python para baixar videos do Youtube 
