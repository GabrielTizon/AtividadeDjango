# 🛍️ Atividade Django

Projeto simples em **Django** para prática em sala de aula.

## Funcionalidades
- Listagem de produtos
- Página de detalhes
- Carrinho de compras (adicionar, atualizar, remover, esvaziar)

## Como rodar
1. Clone o repositório:
   git clone https://github.com/GabrielTizon/AtividadeDjango.git
   cd AtividadeDjango
   
Crie e ative o ambiente virtual:
  py -m venv venv
  .\venv\Scripts\activate

Instale as dependências:
  pip install django

Rode as migrações:
  py manage.py migrate

Inicie o servidor:
  py manage.py runserver

Acesse em:

http://127.0.0.1:8000/ → Loja

http://127.0.0.1:8000/carrinho/ → Carrinho

http://127.0.0.1:8000/admin/ → Admin
