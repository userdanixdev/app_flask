from flask import Flask

app = Flask(__name__)

@app.route("/users/<usuario>/<int:idade>/<float:altura>")
def usuario_info(usuario,idade,altura):
    return{
        "Usuário": usuario,
        "Idade": idade,
        "Altura": altura,
    }

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Home - Projeto Flask</title>

            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }

                .container {
                    width: 80%;
                    margin: auto;
                    padding: 40px;
                }

                .card {
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                }

                h1 {
                    color: #2c3e50;
                }

                h2 {
                    color: #34495e;
                    margin-top: 30px;
                }

                p {
                    color: #555;
                    line-height: 1.7;
                }

                ul {
                    color: #555;
                    line-height: 1.8;
                }

                .footer {
                    margin-top: 40px;
                    text-align: center;
                    color: gray;
                    font-size: 14px;
                }

                .button {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 12px 20px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }

                .button:hover {
                    background-color: #2980b9;
                }
            </style>
        </head>

        <body>

            <div class="container">

                <div class="card">

                    <h1>🚀 Bem-vindo ao Projeto Flask</h1>

                    <p>
                        Esta aplicação foi desenvolvida utilizando Flask,
                        um dos frameworks Python mais populares para
                        desenvolvimento web e construção de APIs.
                    </p>

                    <p>
                        O objetivo deste projeto é demonstrar conceitos
                        fundamentais de backend, organização de rotas,
                        estruturação de aplicações web e integração
                        com tecnologias modernas do ecossistema Python.
                    </p>

                    <h2>📌 Funcionalidades</h2>

                    <ul>
                        <li>Criação de rotas com Flask</li>
                        <li>Desenvolvimento de APIs REST</li>
                        <li>Integração com banco de dados</li>
                        <li>Renderização de páginas HTML</li>
                        <li>Estruturação de aplicações backend</li>
                    </ul>

                    <h2>🛠 Tecnologias Utilizadas</h2>

                    <ul>
                        <li>Python</li>
                        <li>Flask</li>
                        <li>HTML5</li>
                        <li>CSS3</li>
                        <li>Git e GitHub</li>
                    </ul>

                    <h2>🎯 Objetivo</h2>

                    <p>
                        Este projeto foi criado para fins de aprendizado,
                        prática de desenvolvimento backend e construção
                        de portfólio profissional.
                    </p>

                    <a class="button" href="/hello_world">
                        Acessar Página Hello World
                    </a>

                </div>

                <div class="footer">
                    Desenvolvido com Flask + Python
                </div>

            </div>

        </body>
    </html>
    """
@app.route("/intro")
def index():
    return """
    <html>

        <head>
            <title>Introdução Flask</title>

            <style>

                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    padding: 40px;
                }

                .container {
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
                    max-width: 700px;
                    margin: auto;
                }

                h1 {
                    color: #2c3e50;
                }

                p {
                    color: #555;
                    line-height: 1.7;
                }

                .button {
                    display: block;
                    width: 250px;
                    margin-top: 15px;
                    padding: 12px;
                    background-color: #3498db;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    text-align: center;
                    font-weight: bold;
                }

                .button:hover {
                    background-color: #2980b9;
                }

            </style>

        </head>

        <body>

            <div class="container">

                <h1>📘 Página Inicial</h1>

                <p>
                    Bem-vindo à rota de introdução da aplicação Flask.
                </p>

                <p>
                    Utilize as rotas disponíveis abaixo para navegar pelo projeto:
                </p>

                <a class="button" href="/">
                    🏠 Home
                </a>

                <a class="button" href="/hello_world">
                    👋 Hello World
                </a>

                <a class="button" href="/intro">
                    📘 Introdução
                </a>

            </div>

        </body>

    </html>
    """

@app.route("/hello_world")
def hello_world():
    return """
    <html>
        <head>
            <title>Projeto Flask</title>
        </head>
        <body>
            <h1>🚀 Bem-vindo ao Projeto Flask</h1>

            <p>
                Esta aplicação foi desenvolvida utilizando o framework Flask em Python,
                com o objetivo de demonstrar a criação de APIs e aplicações web de forma
                simples, rápida e organizada.
            </p>

            <p>
                O Flask é um microframework extremamente popular no ecossistema Python,
                muito utilizado em projetos de engenharia de dados, desenvolvimento web,
                automações e construção de microsserviços.
            </p>

            <h2>📌 Funcionalidades do Projeto</h2>

            <ul>
                <li>Criação de rotas web</li>
                <li>Estruturação de APIs REST</li>
                <li>Integração com bancos de dados</li>
                <li>Processamento de dados com Python</li>
                <li>Possibilidade de deploy em nuvem</li>
            </ul>

            <h2>🛠 Tecnologias Utilizadas</h2>

            <ul>
                <li>Python</li>
                <li>Flask</li>
                <li>HTML</li>
                <li>Git e GitHub</li>
            </ul>

            <p>
                Este projeto serve como base para estudos e evolução de aplicações
                backend utilizando Python moderno.
            </p>

            <p>
                Desenvolvido para fins de aprendizado e portfólio profissional.
            </p>
        </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)