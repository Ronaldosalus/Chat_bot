import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import YoutubeLoader
import PyPDF2
from tkinter import filedialog, Tk
from api_key import api_key

# Configuração da chave da API
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.1-70b-versatile')

# Função para carregar vídeos do YouTube
def carregar_video(url):
    loader = YoutubeLoader.from_youtube_url(url, language=['pt'])
    return loader.load()

# Função para ler PDF
def ler_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as pdf_file:
        leitor_pdf = PyPDF2.PdfReader(pdf_file)
        texto_completo = ""
        for pagina in range(len(leitor_pdf.pages)):
            pagina_atual = leitor_pdf.pages[pagina]
            texto_completo += pagina_atual.extract_text() or ""  # Adiciona tratamento se a página não contiver texto
        return texto_completo

# Função para selecionar arquivo PDF
def selecionar_pdf():
    root = Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter
    caminho_pdf = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    return caminho_pdf

# Carregar informações do vídeo
url = 'https://www.youtube.com/watch?v=jaqFabeVDUc&list=PLpdAy0tYrnKznoeLzn06M-izJJpoEyzHC&index=131'
lista_documentos = carregar_video(url)
documento = ''.join([doc.page_content for doc in lista_documentos])

# Pergunta ao usuário sobre abrir um PDF
selecao = input('Quer abrir um arquivo PDF? (s/n) ')
if selecao.lower() == 's':
    print('(Mova a tela do vs.)')
    caminho_pdf = selecionar_pdf()  # Chama a função para selecionar o PDF
    if caminho_pdf:  # Verifica se um arquivo foi selecionado
        texto_pdf = ler_pdf(caminho_pdf)
        documento += texto_pdf  # Adiciona o texto do PDF ao documento

# Limita o tamanho do documento
max_tokens = 6000  # Define o limite de tokens
documento_resumido = documento[:max_tokens]  # Pega apenas os primeiros 6000 caracteres


texto_selecao = '''
Digite 1 se você quiser conversar com um vídeo
'''
selecao = input(texto_selecao)


template = ChatPromptTemplate.from_messages([
    ('system', 'Você é um assistente que possui as seguintes informações: {informacoes}'),
    ('user', '{input}'),
])
chain = template | chat

if selecao == '1':
    input_usuario = 'O que ele ensina no Video?'  
else:
    print("Seleção inválida.")
    exit()


resposta = chain.invoke({'informacoes': documento_resumido, 'input': input_usuario}).content
print(resposta)
