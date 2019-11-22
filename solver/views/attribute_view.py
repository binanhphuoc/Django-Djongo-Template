from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Concept, Attribute, Equation
from ..serializers import ConceptSerializer, AttributeSerializer, EquationSerializer

@api_view(['GET','POST'])
def attribute_list(request, concept_id):
    """
    Retrieve, update or delete a code attribute.
    """
    try:
        concept = Concept.objects.get(pk=concept_id)
    except Concept.DoesNotExist:
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
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def attribute_detail(request, concept_id, attribute_id):
    """
    Retrieve, update or delete a code attribute.
    """
    try:
        concept = Concept.objects.get(pk=concept_id)
    except Concept.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    try:
        attribute = Attribute.objects.get(pk=attribute_id)
    except Attribute.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not attribute.parent_concept == concept:
        return Response("Attribute({:s}) does not belong to Concept({:s})"\
            .format(attribute_id, concept_id),\
            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = AttributeSerializer(attribute)
        return Response(serializer.data)

    elif request.method == 'PUT' or request.method == 'PATCH':
        partial = True if request.method == 'PATCH' else False
        serializer = AttributeSerializer(attribute, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        attribute.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)