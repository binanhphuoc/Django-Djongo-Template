from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Concept, Attribute, Equation
from ..serializers import ConceptSerializer, AttributeSerializer, EquationSerializer

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

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def concept_detail(request, concept_id):
    """
    Retrieve, update or delete a code concept.
    """
    try:
        concept = Concept.objects.get(pk=concept_id)
    except Concept.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ConceptSerializer(concept)
        return Response(serializer.data)

    elif request.method == 'PUT' or request.method == 'PATCH':
        partial = True if request.method == 'PATCH' else False
        serializer = ConceptSerializer(concept, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        concept.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
