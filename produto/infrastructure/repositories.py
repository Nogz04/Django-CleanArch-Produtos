# produto/infrastructure/repositories.py
from produto.models import ProdutoModel

class ProdutoRepository:
    def salvar_no_banco(self, nome, descricao, precoCusto, precoVenda, quantidade_estoque) -> ProdutoModel:

        # REPOSITORY -> Cria essa função para ser usada para receber os dados
        # formatados pelo Service e salva no banco

        return ProdutoModel.objects.create(
            nome=nome,
            descricao=descricao,
            precoCusto=precoCusto,
            precoVenda=precoVenda,
            quantidade_estoque=quantidade_estoque,
            ativo=True
        )