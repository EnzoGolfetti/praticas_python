from flask import Flask, render_template, request, redirect

app = Flask(__name__)

#para criarmos rotas em nosso aplicação basta chamar .route()

@app.route('/')
#essa rota vai executar uma função
def index():
    """Essa função está renderizando nosso template que é um arquivo HTML"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) #o parametro debug = True recarrega automaticamente porque está em ambiente de teste
