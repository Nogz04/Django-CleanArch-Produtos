# produto/application/dtos.py

# Responsabilidade: Receber os dados da requisição HTTP, traduzir para Python,
# validar tipos, checar obrigatoriedade e entregar para o Service.

from dataclasses import dataclass
from decimal import Decimal
@dataclass
class ProdutoOutputDTO: # DTO de Saída: O que será entregue ao usuário (Controller)
    id: int
    nome: str
    precoVenda: Decimal
    descricao: str

    # Não enviamos as outras variáveis para o usuário devido
    # à nossa regra de negócio, definida na camada de Use Case.
    # Apenas o que o usuário realmente precisa.
    
    