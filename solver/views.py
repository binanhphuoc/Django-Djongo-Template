from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Concept, Attribute, Equation
from .serializers import ConceptSerializer, AttributeSerializer, EquationSerializer
from . import kernel
from sympy import sympify

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
def concept_detail(request, concept_id):
    """
    Retrieve, update or delete a code concept.
    """
    try:
        concept = Concept.objects.get(pk=concept_id)
    except concept.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ConceptSerializer(concept)
        return Response(serializer.data)

    elif request.method == 'PUT':
        others = {}
        if 'attributes' in request.data:
            others['attributes'] = request.data['attributes']
            request.data.pop('attributes', None)
        serializer = ConceptSerializer(concept, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        concept.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def attribute_list(request, concept_id):
    """
    Retrieve, update or delete a code attribute.
    """
    try:
        concept = Concept.objects.get(pk=concept_id)
    except concept.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AttributeSerializer(concept.attributes, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not isinstance(request.data, list):
            data = [request.data]
        else:
            data = request.data
        for i in range(len(data)):
            data[i]['parent_concept'] = concept
        # https://stackoverflow.com/questions/43435247/creating-multiple-objects-with-one-request-in-django-and-django-rest-framework/43469079
        attribute_serializer = AttributeSerializer(data=data, many=True)
        if attribute_serializer.is_valid():
            attributes = {
                "attributes": {
                    "add": attribute_serializer.save()
                }
            }
            concept_serializer = ConceptSerializer(concept,data=attributes, partial=True)
            if concept_serializer.is_valid():
                concept_serializer.save()
                return Response(attribute_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(concept_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(attribute_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def reasonOnConcept(request, name):
    """
    Retrieve, update or delete a code concept.
    """
    # Functions of request.query_params: https://kite.com/python/docs/django.http.QueryDict
    hypothesis_str = request.query_params.get('hypothesis')
    goal_str = request.query_params.get('goal')
    concept_str = request.query_params.get('concept')
    try:
        concept = Concept.objects.get(name=concept_str)
    except Concept.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # print(concept.attributes)
    # known, solution, giaThuyet = kernel.SuyDienTien(GiaThuyet, KetLuan)
    return Response({
        "hypothesis": hypothesis_str,
        "goal": goal_str,
        "concept": concept_str
    })
    # try:
    #     concept = Concept.objects.get(pk=pk)
    # except Concept.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    # if request.method == 'GET':
    #     serializer = ConceptSerializer(concept)
    #     return Response(serializer.data)

    # elif request.method == 'PUT':
    #     serializer = ConceptSerializer(concept, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     concept.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
