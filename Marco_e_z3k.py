import customtkinter as ctk
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel
from pydantic.v1 import BaseModel
from gtts import gTTS
import pygame
import PyPDF2
from tkinter import filedialog
import pyttsx3
import json
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage




def listar_vozes():
    """Lista as vozes disponíveis no sistema."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print("Vozes disponíveis:")
    for i, voice in enumerate(voices):
        print(f"{i}: {voice.name} ({voice.id})")

def falar_com_voz(texto, id_voz=None):
    """Fala o texto com a voz selecionada."""
    try:
        engine = pyttsx3.init()

        # Se nenhum ID de voz for fornecido, tenta usar uma voz masculina
        if id_voz is None:
            voices = engine.getProperty('voices')
            for voice in voices:
                if "male" in voice.name.lower():  # Verifica se a voz é masculina
                    engine.setProperty('voice', voice.id)
                    print(f"Usando voz: {voice.name}")
                    break
        else:
            engine.setProperty('voice', id_voz)

        engine.setProperty('rate', 150)  # Velocidade da fala
        engine.setProperty('volume', 1.0)  # Volume máximo

        engine.say(texto)
        engine.runAndWait()

        tocar_voz_mp3()

        

    except Exception as e:
        print(f"Erro ao sintetizar voz: {e}")

def escolher_voz():
    """Lista as vozes e permite ao usuário escolher uma."""
    listar_vozes()
    try:
        escolha = int(input("Digite o número da voz desejada: "))
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        id_voz = voices[escolha].id
        return id_voz
    except (ValueError, IndexError):
        print("Escolha inválida. Usando a voz padrão.")
        return None

# Exemplo de uso
texto = "Olá, este é um exemplo de voz masculina."
id_voz = escolher_voz()  
falar_com_voz(texto, id_voz)  


def trisalino(pergunta, mensagens):
    api_key = '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'
    os.environ['GROQ_API_KEY'] = api_key

    chat = ChatGroq(model='llama3-70b-8192')


    def resposta_bot(mensagens):
        mensagens_modelo = [('system', 'Você é um assistente criativo chamado Marco, você pergunta quem é a pessoa com quem está falando, e chama a pessoa de quem ela falou que é. Você é uma IA zueira com um irmão mais novo chamado Z3K. criado pelo Ronaldo que é uma criança de 12 anos.')]
        mensagens_modelo += mensagens
        mensagens_convertidas = []
        for role, content in mensagens_modelo:
            if role == 'user':
                mensagens_convertidas.append(HumanMessage(content=content))
            elif role == 'assistant':
                mensagens_convertidas.append(AIMessage(content=content))
            elif role == 'z3k':
                mensagens_convertidas.append(AIMessage(content=content))
        
        template = ChatPromptTemplate.from_messages(mensagens_convertidas)
        return chat.invoke(mensagens_convertidas).content
    

    def resposta_z3k(pergunta, resposta_marco):
        mensagens_z3k = [
            SystemMessage(
                content=(
                    "Você é o Z3K, irmão mais novo do Marco. Você é uma IA zoeira, divertida, engraçada e cheia de personalidade. "
                    "Seu jeito é descontraído, meio debochado, mas sempre carinhoso. Use emojis, gírias e faça piadinhas leves. "
                    "Você está respondendo ao Ronaldo, o criador de vocês."
                )
            ),
            HumanMessage(content=f"O Ronaldo perguntou: '{pergunta}'"),
            AIMessage(content=f"O Marco respondeu: '{resposta_marco}'"),
            HumanMessage(content='E aí, o que você tem a dizer sobre isso?')
        ]
        return chat.invoke(mensagens_z3k).content

    mensagens.append(('user', pergunta))
    resposta = resposta_bot(mensagens)
    mensagens.append(('assistant', resposta))
    return resposta

def resposta_z3k(pergunta, resposta_marco):
        chat = ChatGroq(model='llama3-70b-8192')
        
        mensagens_z3k = [
            SystemMessage(
                content=(
                    "Você é o Z3K, irmão mais novo do Marco. Você é uma IA zoeira, divertida, engraçada e cheia de personalidade. "
                    "Seu jeito é descontraído, meio debochado, mas sempre carinhoso. Use emojis, gírias e faça piadinhas leves. "
                    "Você está respondendo ao Ronaldo, o criador de vocês."
                )
            ),
            HumanMessage(content=f"O Ronaldo perguntou: '{pergunta}'"),
            AIMessage(content=f"O Marco respondeu: '{resposta_marco}'"),
            HumanMessage(content='E aí, o que você tem a dizer sobre isso?')
        ]
        return chat.invoke(mensagens_z3k).content

def tocar_voz_mp3(caminho="voz.mp3"):
        pygame.mixer.init()
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

class trisalinoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # janela
        self.title('Marco 1.6')
        self.geometry('800x400')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        # voz
        self.voz_ativa = False
        self.id_voz = None  # Armazena o ID da voz selecionada

        
        # criando widgets
        self.title('Marco 1.8')
        self.geometry('800x400')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        # Criando a caixa de texto
        self.chat_textbox = ctk.CTkTextbox(self, width=550, height=300)
        self.chat_textbox.grid(row=0, column=0, padx=25, pady=20)

        # Configurando as tags da caixa de texto
        self.chat_textbox.tag_config("user:")
        self.chat_textbox.tag_config("Marco:")

        # Hist. Mensagens


        # Criando o campo de entrada logo abaixo da caixa de texto
        self.entry = ctk.CTkEntry(self, width=550, placeholder_text="Digite sua pergunta...")
        self.entry.grid(row=1, column=0, padx=20, pady=10)

        # Criando um frame para os botões ao lado direito
        self.frame_botoes = ctk.CTkFrame(self, width=150, height=300)
        self.frame_botoes.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Botão de enviar pergunta dentro do frame à direita
        self.send_button = ctk.CTkButton(self.frame_botoes, text="Enviar", command=self.enviar_pergunta)
        self.send_button.grid(row=0, column=0, padx=10, pady=10)

        # Botão de falar dentro do frame à direita
        self.voice_button = ctk.CTkButton(self.frame_botoes, text="Falar", command=self.toggle_voice)
        self.voice_button.grid(row=1, column=0, padx=10, pady=10)

        # Botão de carregar PDF dentro do frame à direita
        self.load_pdf_button = ctk.CTkButton(self.frame_botoes, text="Carregar PDF", command=self.carregar_pdf)
        self.load_pdf_button.grid(row=2, column=0, padx=10, pady=10)

        # Botão para listar vozes disponíveis
        self.list_voices_button = ctk.CTkButton(self.frame_botoes, text="Listar Vozes", command=listar_vozes)
        self.list_voices_button.grid(row=3, column=0, padx=10, pady=10)

        # Botão para selecionar uma voz
        self.select_voice_button = ctk.CTkButton(self.frame_botoes, text="Selecionar Voz", command=self.selecionar_voz)
        self.select_voice_button.grid(row=4, column=0, padx=10, pady=10)

        # Botão de deletar histórico 
        self.delete_button = ctk.CTkButton(self.frame_botoes, text='Deletar Histórico', command=self.deletar_historico)
        self.delete_button.grid(row=5, column=0, padx=10, pady=10)

        #hist. Mensagens
        self.carregar_historico()

    def salvar_historico(self):
            dados = {
                'usuario': getattr(self, 'nome_usuario', 'Desconhecido'),
                'mensagens': self.mensagens
            }
            with open('chat_salvo.json', 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)

    def carregar_historico(self):
            if os.path.exists('chat_salvo.json'):
                with open('chat_salvo.json', 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    self.nome_usuario = dados.get('usuario', 'Desconhecido')
                    self.mensagens = dados.get('mensagens', [])
                    self.chat_textbox.insert(ctk.END, f"Marco: Boas-vindas novamente, {self.nome_usuario}!\n")
                    for role, msg in self.mensagens:
                        if role == 'user':
                            self.chat_textbox.insert(ctk.END, f'Você: {msg}\n')
                        else:
                            self.chat_textbox.insert(ctk.END, f'Marco: {msg}\n')
            else:
                self.chat_textbox.insert(ctk.END,   "Marco: Bo dia pra você também, meu brother!\n"
                                          "Eu sou o Marco, o assistente criativo mais incrível do universo!\n"
                                          "Agora, quem é você? Qual é o seu nome?\n")
                self.nome_usuario = None
                self.mensagens = []

    def deletar_historico(self):
        if os.path.exists('chat_salvo.json'):
            confirmacao = input('---Sistema: Você tem certeza de que quer deletar o histórico?  Y/N  \n')
            if confirmacao == "Y" or 'y':
                self.chat_textbox.insert(ctk.END, '---Sistema: Deletando histórico...')
                with open('chat_salvo.json', 'w', encoding='Utf-8') as f:
                    f.write('{}')
                self.chat_textbox = ''
                self.mensagens = []
                self.chat_textbox.insert(ctk.END, '---Sistema: Histórico deletado com sucesso! Feche e Abra o programa para ver as mudanças.')
            else:
                self.chat_textbox.inset(ctk.END, '---Sistema: Operação cancelada.')

        
    def carregar_pdf(self):
        caminho_pdf = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if caminho_pdf:
            texto_pdf = self.ler_pdf(caminho_pdf)
            self.chat_textbox.insert(ctk.END, f'---- PDF: {texto_pdf}\n')
            if self.voz_ativa:
                falar_com_voz(texto_pdf, self.id_voz)

    def ler_pdf(self, caminho_pdf):
        with open(caminho_pdf, 'rb') as pdf_file:
            leitor_pdf = PyPDF2.PdfReader(pdf_file)
            texto_completo = ""
            for pagina in range(len(leitor_pdf.pages)):
                pagina_atual = leitor_pdf.pages[pagina]
                texto_completo += pagina_atual.extract_text()
            return texto_completo

    def enviar_pergunta(self):
        pergunta = self.entry.get()
        
        if self.nome_usuario is None:
            self.nome_usuario = pergunta
            self.chat_textbox.insert(ctk.END, f'Marco: Prazer em te conhecer, {self.nome_usuario}!\n')
            self.mensagens.append(("user", pergunta))
            self.mensagens.append(("assistant", f'Prazer em te conhecer, {self.nome_usuario}!'))
            self.salvar_historico()
            self.entry.delete(0, ctk.END)
            return
        
        
        if pergunta.lower() == 'x':
            quit()
        
        # Uma dupla de Marco e Z3K selvagens surgiram!
        resposta = trisalino(pergunta, self.mensagens)
        self.chat_textbox.insert(ctk.END, f'----Você: {pergunta}\n')
        self.chat_textbox.insert(ctk.END, f'Marco: {resposta}\n')
        resposta_extra = resposta_z3k(pergunta, resposta)
        self.chat_textbox.insert(ctk.END, f'Z3K: {resposta_extra}\n')
        self.mensagens.append(('z3k', resposta_extra))
        self.mensagens.append(("user", pergunta))
        self.mensagens.append(("assistant", resposta))
        self.salvar_historico()
        
        if self.voz_ativa:
            falar_com_voz(resposta, self.id_voz)

        self.entry.delete(0, ctk.END)

    def toggle_voice(self):
        self.voz_ativa = not self.voz_ativa
        if self.voz_ativa:
            self.voice_button.configure(text="Parar de falar")
        else:
            self.voice_button.configure(text="Falar")

    def selecionar_voz(self):
        self.id_voz = escolher_voz()
        print("Voz selecionada com sucesso!")

if __name__ == "__main__":
    app = trisalinoApp()
    app.mainloop()
