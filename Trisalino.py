import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate


api_key = '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'
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.1-70b-versatile')


def resposta_bot(mensagens):
        mensagens_modelo = [('system', 'Você é um assistente amigavél chamado Trisalino, criado pelo Ronaldo, o Ronaldo é uma criança de 11 anos aprendendo Python, e ajudante da Rokathi.')]
        mensagens_modelo += mensagens
        template = ChatPromptTemplate.from_messages(mensagens_modelo)
        chain = template | chat
        return chain.invoke({}).content

print('--------------------------- Bem vindo ao Trinsalino ------------------------------')
print('Para sair escreva x e aperte enter.')
mensagens = []

while True:
    pergunta = input('user:  ')
    if pergunta.lower() == 'x':
        break
    mensagens.append(('user', pergunta))
    resposta = resposta_bot(mensagens)
    mensagens.append(('assistant', resposta))
    print(f'Trisalino: {resposta}')

print('Tenha um bom dia!')
