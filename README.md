# 🛒 Django Clean Architecture — API de Produtos

API REST para cadastro de produtos construída com **Django + Django REST Framework**, aplicando os princípios de **Clean Architecture** (separação em camadas: View → Service → Repository).

---

## 🚀 Como executar o projeto

### 1. Clonar o repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd Exemplo-Django-CleanArch-Produtos
```

### 2. Criar e ativar o ambiente virtual

```bash
# Criar o venv no terminal 
python -m venv venv

# Ativar (Windows PowerShell)
venv\Scripts\activate

```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Criar o banco de dados

O projeto usa **SQLite** por padrão — nenhuma configuração extra é necessária.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Iniciar o servidor

```bash
python manage.py runserver
```

O servidor estará disponível em: `http://127.0.0.1:8000`

---
## 🔀 Fluxo do sistema

**1. Usuário Web / Frontend**

> O usuário preenche um formulário no site e faz uma requisição ```HTTP POST``` para a URL `/api/produtos/criar/`.

**2. Roteador (```urls.py```)**

> O Django recebe o link, olha no mapa de rotas (`urls.py`) e diz: *"Essa URL pertence à CriarProdutoView"*. E encaminha a requisição para lá.

**3. View (```api/views.py```)**
 
> A View é a recepcionista. Ela recebe o pedido do usuário (request), mas não tem permissão para ir ao estoque (Banco de Dados), nem tomar decisões (Regras de negócio). O que ela faz? Ela chama o gerente da área específica que ela quer (Service). Exemplo: ```service = ProdutoService(); service.criar_produto(dados)```

**4. Service (```application/services.py```)**

> O Service é o cérebro (Regra de negócio juntamente com os testes). Ele pensa: *"Preciso criar um produto e calcular o preço de venda, mas não sei como falar com o banco de dados"*. O que ele faz? Ele pede para o "estoquista": o **Repository.** Exemplo: ```self.repository.create(produto_entity)```

**5. Repository (```infrastructure/repositories.py```)**

> O Repository é o cara que sabe falar com o banco de dados usando a linguagem do Django ORM. Ele vai no banco (`Produto.objects.create(...)`), salva os dados brutos (Models "sujos" cheios de dependências do banco) e entrega de volta para o Gerente (Service).

**6. Service ```retorno```**

> O Service pega aqueles dados brutos do Repository. Como a regra da Clean Architecture proíbe enviar Models do banco de dados diretamente para fora, ele tira os dados do Model e os coloca em uma caixa limpinha e independente: o DTO (```ProdutoDTO```). O Service então devolve essa caixa limpa (**DTO**) para a Recepcionista (**View**).

**7. View (```retorno```)**

> A View agora está com o ProdutoDTO nas mãos. Mas a internet (o navegador do usuário) não sabe ler objetos do Python (```@dataclass```), ela só entende formato texto (**JSON**). O que a View faz? Ela chama o Tradutor: o ```Serializer```. Exemplo: ```serializer = ProdutoDTOSerializer(produto_dto)```

**8. Serializer (```api/serializers.py```)**

> O Serializer traduz a caixa ```ProdutoDTO``` em um texto JSON estruturado: ```{ "id": 1, "nome": "Notebook Dell", "precoVenda": "3750.00", "descricao": "Notebook com 16GB RAM" }```

**9. View (```finalização```)**

> A View pega esse JSON traduzido, coloca um selo de *"Tudo certo! (Status HTTP 201 Created)"* e envia de volta (Response pela internet.)

**10. Usuário Web / Front-end (```Destino```)**

> O site do usuário recebe o JSON, lê e mostra a confirmação de criação do produto na tela.

### Resumo rápido:

```Browser``` ➔ ```urls.py``` ➔ ```View``` ➔ ```Service``` ➔ ```Repository``` ➔ ```(Banco de Dados)``` ➔ ```Repository``` ➔ ```Service (empacota em DTO)``` ➔ ```View (pede pro Serializer virar JSON)``` ➔ ```Browser```

---

## 📡 Endpoints disponíveis

| Método | URL | Descrição |
|--------|-----|-----------|
| `POST` | `/api/produtos/criar/` | Cria um novo produto |

> **Regra de negócio:** o `precoVenda` **não é enviado pelo cliente** — ele é calculado automaticamente pelo Service com 50% de margem sobre o `precoCusto`.
> `precoVenda = precoCusto × 1.50`

---

## 🧪 Testando com Postman

### ⚙️ Configuração padrão para todas as requisições

| Campo | Valor |
|-------|-------|
| Method | `POST` |
| URL | `http://127.0.0.1:8000/api/produtos/criar/` |
| Header | `Content-Type: application/json` |
| Body | `raw` → `JSON` |

> No Postman: aba **Body** → selecione **raw** → escolha **JSON** no dropdown → cole o body abaixo.

---

## ✅ Cenários de sucesso

### 1. Criar Produto com Sucesso (201)

**Body:**
```json
{
  "nome": "Notebook Dell Inspiron",
  "descricao": "Notebook com 16GB RAM e SSD 512GB",
  "precoCusto": "2500.00",
  "quantidade_estoque": 10
}
```

**Resposta esperada — 201 Created:**
```json
{
  "id": 1,
  "nome": "Notebook Dell Inspiron",
  "precoVenda": "3750.00",
  "descricao": "Notebook com 16GB RAM e SSD 512GB"
}
```
> 💡 `precoVenda` calculado: `2500 × 1.50 = 3750.00`

---

### 2. Criar Produto com Estoque Zero (201)

**Body:**
```json
{
  "nome": "Mouse Sem Fio",
  "descricao": "Mouse wireless 2.4GHz com DPI ajustável",
  "precoCusto": "80.00",
  "quantidade_estoque": 0
}
```

**Resposta esperada — 201 Created:**
```json
{
  "id": 2,
  "nome": "Mouse Sem Fio",
  "precoVenda": "120.00",
  "descricao": "Mouse wireless 2.4GHz com DPI ajustável"
}
```

---

### 3. Criar Produto com Descrição Vazia (201)

**Body:**
```json
{
  "nome": "Teclado Mecânico",
  "descricao": "",
  "precoCusto": "350.00",
  "quantidade_estoque": 25
}
```

**Resposta esperada — 201 Created:**
```json
{
  "id": 3,
  "nome": "Teclado Mecânico",
  "precoVenda": "525.00",
  "descricao": ""
}
```

---

## ❌ Cenários de erro (validações)

### 4. Nome Muito Curto — menos de 3 caracteres (400)

**Body:**
```json
{
  "nome": "AB",
  "descricao": "Produto com nome inválido",
  "precoCusto": "50.00",
  "quantidade_estoque": 5
}
```

**Resposta esperada — 400 Bad Request:**
```json
{
  "nome": [
    "Nome deve ter pelo menos 3 caracteres"
  ]
}
```

---

### 5. Estoque Negativo (400)

**Body:**
```json
{
  "nome": "Produto Inválido",
  "descricao": "Estoque não pode ser negativo",
  "precoCusto": "100.00",
  "quantidade_estoque": -5
}
```

**Resposta esperada — 400 Bad Request:**
```json
{
  "quantidade_estoque": [
    "Estoque não pode ser negativo"
  ]
}
```

---

### 6. Preço de Custo Igual a Zero (400)

**Body:**
```json
{
  "nome": "Produto Gratuito",
  "descricao": "Preço de custo não pode ser zero",
  "precoCusto": "0.00",
  "quantidade_estoque": 10
}
```

**Resposta esperada — 400 Bad Request:**
```json
{
  "precoCusto": [
    "Preço de custo deve ser maior que zero"
  ]
}
```

---

### 7. Campos Obrigatórios Ausentes (400)

**Body:**
```json
{
  "nome": "Produto Incompleto"
}
```

**Resposta esperada — 400 Bad Request:**
```json
{
  "descricao": ["Este campo é obrigatório."],
  "precoCusto": ["Este campo é obrigatório."],
  "quantidade_estoque": ["Este campo é obrigatório."]
}
```

---

### 8. Body Completamente Vazio (400)

**Body:**
```json
{}
```

**Resposta esperada — 400 Bad Request:**
```json
{
  "nome": ["Este campo é obrigatório."],
  "descricao": ["Este campo é obrigatório."],
  "precoCusto": ["Este campo é obrigatório."],
  "quantidade_estoque": ["Este campo é obrigatório."]
}
```

---

### 9. Tipo Inválido no precoCusto (400)

**Body:**
```json
{
  "nome": "Produto Teste",
  "descricao": "Teste de tipo inválido",
  "precoCusto": "abc",
  "quantidade_estoque": 10
}
```

**Resposta esperada — 400 Bad Request:**
```json
{
  "precoCusto": [
    "Um número válido é necessário."
  ]
}
```

---

## 📋 Resumo dos Cenários

| # | Cenário | Status Esperado |
|---|---------|----------------|
| 1 | Produto válido completo | ✅ 201 Created |
| 2 | Estoque igual a zero | ✅ 201 Created |
| 3 | Descrição vazia | ✅ 201 Created |
| 4 | Nome com menos de 3 letras | ❌ 400 Bad Request |
| 5 | Quantidade de estoque negativa | ❌ 400 Bad Request |
| 6 | `precoCusto` igual a 0 | ❌ 400 Bad Request |
| 7 | Campos obrigatórios ausentes | ❌ 400 Bad Request |
| 8 | Body vazio `{}` | ❌ 400 Bad Request |
| 9 | Tipo inválido em `precoCusto` | ❌ 400 Bad Request |
