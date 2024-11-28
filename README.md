# Wiki Mago 🧙‍♂️

> ### TP3: Desenvolvimento Front-End com Python (com Streamlit) [24E3_1]
>
> **Rafael Soares de Oliveira**  
> Infnet - Ciência de Dados | Dezembro 2024  
> [Página do Trabalho](https://lms.infnet.edu.br/moodle/mod/assign/view.php?id=426791)

## Sobre o projeto

O **Wiki Mago** é um chatbot mágico que utiliza dados da 📘 Wikipedia, 📽️ YouTube e da 🌐 Web para responder perguntas sobre qualquer assunto.  
Precisa de ajuda com uma pesquisa? Tem curiosidade sobre algo específico? Ou só quer assistir vídeos de gatinhos brincando?  
**O Wiki Mago sabe de tudo!** (Ou quase tudo... 🪄)

---

## Como iniciar o projeto

### 1. Configurar o ambiente virtual

Execute os comandos abaixo no terminal para criar e ativar um ambiente virtual e instalar as dependências necessárias:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Inicializar o Streamlit

```console
streamlit run src/main.py
```

Acesse o projeto no navegador no endereço http://localhost:8501 (ou no endereço exibido no console).

#### Dica para usuários do VSCode

Após instalar as dependências, você pode executar o projeto diretamente no VSCode usando o atalho Ctrl+F5 (ou um comando equivalente no seu sistema operacional).

### Reflexões sobre o projeto

O LangChain se mostrou uma ferramenta extremamente poderosa, tornando acessível o desenvolvimento de aplicações com funcionalidades incrivelmente complexas.

Ao abstrair grande parte da complexidade de integração e conexão com diversas APIs e fontes de dados, ele permite criar soluções robustas com poucas linhas de código.
Este é o caso do **Wiki Mago**. Apesar de ser uma aplicação relativamente simples, ela oferece funcionalidades altamente úteis para auxílio em projetos e estudos de forma intuitiva e conversacional.

Em outros tempos, uma aplicação como essa representaria uma grande quebra de paradigma, exigindo uma complexidade enorme para conectar e consumir dados de diferentes fontes.
Com o LangChain, o que poderia levar meses para ser desenvolvido foi criado em poucas horas, destacando o potencial de ferramentas modernas para acelerar o desenvolvimento de soluções inovadoras.

---

> 🧙‍♂️ Seja bem-vindo ao mundo do Wiki Mago! Aproveite a jornada mágica de descobertas e conhecimento. ✨
