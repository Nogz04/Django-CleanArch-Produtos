from decimal import Decimal
from ..infrastructure.repositories import ProdutoRepository
from produto.application.dtos import ProdutoOutputDTO

# Responsabilidade: Realiza a lógica e chama o repository para armazenar no banco e transforma em DTO para entregar ao usuário.

class ProdutoService:
    def __init__(self, repository: ProdutoRepository):
        self.repository = repository

    def registrar_novo_produto(self, nome, descricao, precoCusto, quantidade_estoque):
        
        # O SERVICE -> Irá executar a regra de negócio:
        # Preço de venda = Custo + 50% de Margem

        margem = 1.50
        preco_venda_calculado = Decimal(str(precoCusto)) * Decimal(margem)

        # Chama o repositório para salvar no banco
        produto_obj = self.repository.salvar_no_banco(
            nome,
            descricao,
            precoCusto,
            preco_venda_calculado,
            quantidade_estoque
        )

        # Transforma o Model em DTO para devolver para a View
        return ProdutoOutputDTO(
            id=produto_obj.id,
            nome=produto_obj.nome,
            precoVenda=produto_obj.precoVenda,
            descricao=produto_obj.descricao
        )
        