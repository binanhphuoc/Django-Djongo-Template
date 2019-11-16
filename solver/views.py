from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Concept
from .serializers import ConceptSerializer

@api_view(['GET', 'POST'])
def concept_list(request):
    """
    List all code concepts, or create a new concept.
    """
    if request.method == 'GET':
        concepts = Concept.objects.all()
        serializer = ConceptSerializer(concepts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ConceptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def concept_detail(request, pk):
    """
    Retrieve, update or delete a code concept.
    """
    try:
        concept = Concept.objects.get(pk=pk)
    except Concept.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ConceptSerializer(concept)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ConceptSerializer(concept, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        concept.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
