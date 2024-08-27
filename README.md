# APS 1 de Natural Language Processing

## Feito por 🧑‍🤝‍🧑:
- Henrique Martinelli Frezzatti

## Bibliotecas necessárias:
Todas as bibliotecas que forem obrigatórias para a execução do programa se encontram no arquivo **requirements.txt** que podem ser instaladas com os comandos abaixo:
```bash
pip install -r requirements.txt
```

## Como rodar? 🖥️
Para executar e rodar a API basta abrir o terminal dentro da pasta principal do repositório da APS e rodar o comando abaixo:

```bash
python3 app.py
```

Ao executar o comando acima, o servidor da API será aberto em dois endereços, um privado (localhost) e outro para acesso público, ambos nas portas 5006:
```
http://127.0.0.1:5006
http://10.103.0.28:5006
```

Acessando algum dos endereços acima, é possível adicionar a extensão `/query?query=[STRING DE BUSCA]` à URL acima, onde `[STRING DE BUSCA]` se refere a uma string qualquer escolhida pelo usuário para classificar os documentos em ordem de relevância de acordo com a sua busca em um total de 10 documentos.
Exemplo:
```
http://10.103.0.28:5006/query?query=painting
```
---
# Introdução da APS 💡:
A APS consiste em efetuar a criação de um classificador TFIDF para determinar a relevância de determinadas palavras em documentos de determinado banco de dados. Sendo assim, é necessário a criação de um banco de dados único que, nessa APS, foi criado com a utilização de uma API externa

## Banco de dados 📂:
O banco de dados para essa APS foi criado com a utilização da API do _Art Institute of Chicago_ e, a sua utilização, foi motivada pela necessidade de encontrar artistas, obras e pinturas que remetem a um determinado estilo/palavra determinada pelo usuário. Logo, se o usuário quiser encontrar as obras de arte referentes ao movimento surrealista, ele poderia realizar essa busca e encontrar as artes que mais condizem com o que deseja ver, podendo obter informações extras sobre aquela obra como o artista que a pintou, o ano em que foi pintada e sua descrição.

Para a criação desse banco de dados, foi utilizado o código localizado em `db_creation.py` e, o resultado de sua execução, irá criar um `.csv` com 10 mil itens dessa API localizado em `art-db.csv`.

## API e configurações de rede 📪:
A API criada para esse trabalho foi feita utilizando a biblioteca Flask para Python. Para iniciar a sua implementação foi utilizado o repositório: https://github.com/alessitomas/flask_server_template

Além disso, foi necessário alterar a porta de execução padrão dessa API para uma nova e não utilizada por outra pessoa que compartilhasse da mesma máquina remota no Insper e, para isso, foi adicionado o parâmetro abaixo em `app.py`:
```python
app.run(host='0.0.0.0', port=5006)
```
Sendo assim, sempre que for executada, irá ser na porta 5006 definida. No entanto, também é necessário abrir essa porta na máquina acessada via SSH no Insper e, para isso, foi utilizado o comando abaixo:
```bash
sudo ufw allow 5006
```

## Rubrica e pontos realizados 🟢:
- [X] Criação e configuração da API via Flask ou FastAPI
- [X] Escolha da API para geração do banco de dados
- [X] Criação do banco de dados
- [X] Criação do classificador de relevância
- [X] Completar o README.md
