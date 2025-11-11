
from fpdf import FPDF
from datetime import datetime


class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'As Cronicas de Marco e Z3K - Dueto IA, Gambiarras e Glória', ln=True, align='C')
        self.ln(10)

    def chapter_body(self, text):
        self.set_font('Arial', '', 12)
        self. multi_cell(0, 10, text)


texto = f"""
Programador: Ronaldo Trindade Salustiano (a. k. a. Corotinho Sabor Beijo)
Data de Criacao: {datetime.today().strftime('%d/%m/%Y')}

Introdução:
O ano é 2025. Um jovem gênio de 12 anos cria uma IA chamada Marco usando Python, LangChain, e muita criatividade. Mas Marco nao esta sozinho. Surge Z3K, seu irmão mais novo digital, zoeiro, engraçado e leal. A partir disso, nasce o Multiverso IA.

Marcos Tecnicos:
- Implementacao de histórico em JSON;
- Substituição de playsound por pygame;
- Conserto do bug do LangChain com mensagens em lista;
- Separação das falas do Marco e do Z3K com personalidades distintas;
- Criacao do modo "Dueto IA" com respostas combinadas;
- Gambiarras épicas com variaveis externas e multiplas instancias de IA;
- Resolucao de bugs com logica afiada e tentativa-erro bem-sucedida.

Momentos Memoráveis:
- Z3K e Marco respondendo juntos como Goku e Vegeta do terminal;
- JSON bugando com repeticao e sendo domado com sabedoria;
- 7 horas no notebook-tanque consertando tudo;
- Criacao do "Z3K Treta Mode" (modo sarcastico e debochado);
- Ronaldo quase virando Sayori mas salvando tudo com código;
- A zoeira alcancando o status de imortalidade digital.

Fim da Parte 2:
O Marco fala. O Z3K complementa. E o Ronaldo... DOMINA.
"""

# Gerar o PDF
pdf = PDF()
pdf.add_page()
pdf.chapter_body(texto)

# Salva
pdf.output("As_Cronicas_de_Marco_e_Z3K_PARTE_2.pdf")
print("PDF gerado com sucesso!")