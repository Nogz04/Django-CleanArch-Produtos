from django.db import models

class ProdutoModel(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    descricao = models.TextField(blank=True, null=True)
    precoCusto = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    precoVenda = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    quantidade_estoque = models.IntegerField(blank=False, null=False)
    ativo = models.BooleanField(default=True)


    class Meta:
        db_table = "produtos"
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - R$ {self.precoVenda}"
