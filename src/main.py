"""
=====================================================
Baixador de Vídeos Pessoal - Ponto de Entrada (Main)
=====================================================

Autor: Mark Musk - Dev Python
Data: 08/11/2025
Versão: 1.0

Descrição:
Este é o script principal (ponto de entrada) da aplicação.
Sua única responsabilidade é instanciar e executar a interface 
gráfica principal (AppGUI) definida em app_gui.py.
"""

# Importações de módulos
import tkinter as tk
from app_gui import AppGUI

def main():
    """
    Função principal que inicializa e executa a aplicação.
    
    Cria a janela raiz do Tkinter, instancia a classe AppGUI
    e inicia o loop principal da aplicação (mainloop).
    """
    try:
        # Cria a janela raiz. É uma boa prática criar a raiz aqui
        # e passá-la para a classe da aplicação.
        root = tk.Tk()
        
        # Instancia nossa aplicação principal
        app = AppGUI(master=root)
        
        # Inicia o loop principal da interface gráfica
        # O script ficará "preso" aqui até que a janela seja fechada.
        app.run()
        
    except Exception as e:
        # Um tratamento de erro genérico "pega-tudo" no ponto mais alto
        # da aplicação, caso algo muito inesperado ocorra durante
        # a inicialização.
        print(f"Erro fatal ao iniciar a aplicação: {e}")
        # Em uma aplicação real, poderíamos logar isso ou mostrar
        # um pop-up de erro nativo do sistema.

if __name__ == "__main__":
    # Este bloco garante que main() só seja executado quando
    # o script for chamado diretamente (e não importado).
    main()