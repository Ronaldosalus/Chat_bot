import customtkinter as ctk
from tkinter import filedialog
import PyPDF2
from gtts import gTTS
import os


# Função para converter texto em fala (mantida fora da classe)
def falar(texto):
    tts = gTTS(text=texto, lang='pt', slow=False)
    caminho_audio = os.path.join(os.getcwd(), "resposta.mp3")
    tts.save(caminho_audio)
    os.system(f"start {caminho_audio}")  # Reproduz o áudio no Windows

class trisalinoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Marco 1.2')
        self.geometry('800x400')  # Tamanho ajustado para acomodar melhor os botões ao lado da caixa de texto

        # Criando frame para organizar a caixa de texto e os botões
        self.frame_texto = ctk.CTkFrame(self, width=550, height=300)
        self.frame_texto.grid(row=0, column=0, padx=20, pady=20)

        # Caixa de texto para mostrar o conteúdo do PDF
        self.pdf_textbox = ctk.CTkTextbox(self.frame_texto, width=400, height=300)
        self.pdf_textbox.grid(row=0, column=0, padx=20, pady=10)

        # Criando frame para os botões
        self.frame_botoes = ctk.CTkFrame(self, width=150, height=300)
        self.frame_botoes.grid(row=0, column=1, padx=10, pady=10)

        # Botão para carregar e ler PDF (lado da caixa de texto)
        self.load_pdf_button = ctk.CTkButton(self.frame_botoes, text="Carregar PDF", command=self.carregar_pdf)
        self.load_pdf_button.grid(row=0, column=0, padx=10, pady=10)

        # Botão para sair (lado da caixa de texto)
        self.quit_button = ctk.CTkButton(self.frame_botoes, text="Sair", command=self.quit)
        self.quit_button.grid(row=1, column=0, padx=10, pady=10)

    def carregar_pdf(self):
        caminho_pdf = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if caminho_pdf:
            texto_pdf = self.ler_pdf(caminho_pdf)
            self.pdf_textbox.insert(ctk.END, texto_pdf)
            # Chamando a função falar diretamente
            falar(texto_pdf)

    def ler_pdf(self, caminho_pdf):
        with open(caminho_pdf, 'rb') as pdf_file:
            leitor_pdf = PyPDF2.PdfReader(pdf_file)
            texto_completo = ""
            for pagina in range(len(leitor_pdf.pages)):
                pagina_atual = leitor_pdf.pages[pagina]
                texto_completo += pagina_atual.extract_text()
            return texto_completo

if __name__ == "__main__":
    app = trisalinoApp()
    app.mainloop()
