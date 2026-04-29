from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .infrastructure.repositories import ProdutoRepository
from .application.services import ProdutoService
from .api.serializers import ProdutoInputSerializer, ProdutoOutputSerializer

class CriarProdutoView(APIView):
    
    def post(self, request):
       
       # A view recebe o objeto 'request' e usa o Serializer para validar os dados em JSON
       serializer_input = ProdutoInputSerializer(data=request.data)
       serializer_input.is_valid(raise_exception=True)
       
    
       #Injeção de dependência manualmente (Repository -> Service)
       repo = ProdutoRepository()
       service = ProdutoService(repository=repo)
       
       dto_saida = service.registrar_novo_produto(
           **serializer_input.validated_data 
       )

       # Serializa o DTO de saída para JSON antes de enviar de volta
       serializer_output = ProdutoOutputSerializer(dto_saida)
       return Response(serializer_output.data, status=status.HTTP_201_CREATED)