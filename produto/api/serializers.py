from rest_framework import serializers

# Responsabilidade: Receber os dados da requisição HTTP, traduzir para Python,
# validar tipos, checar obrigatoriedade e entregar para o Service.

class ProdutoInputSerializer(serializers.Serializer):
    nome = serializers.CharField(max_length=100)
    descricao = serializers.CharField(max_length=100, allow_blank=True)
    precoCusto = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = serializers.IntegerField()

    def validate_nome(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Nome deve ter pelo menos 3 caracteres")
        return value

    def validate_quantidade_estoque(self, value):
        if value < 0:
            raise serializers.ValidationError("Estoque não pode ser negativo")
        return value

    def validate_precoCusto(self, value):
        if value <= 0:
            raise serializers.ValidationError("Preço de custo deve ser maior que zero")
        return value


# Responsabilidade: Serializar o DTO de saída para enviar como JSON ao cliente.
# precoVenda é calculado pelo Service (não vem do cliente).
class ProdutoOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField()
    precoVenda = serializers.DecimalField(max_digits=10, decimal_places=2)
    descricao = serializers.CharField()