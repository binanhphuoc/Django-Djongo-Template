from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Concept, Equation, Equation
from ..serializers import ConceptSerializer, EquationSerializer, EquationSerializer

@api_view(['GET','POST'])
def equation_list(request, concept_id):
    """
    Retrieve, update or delete a code equation.
    """
    try:
        concept = Concept.objects.get(pk=concept_id)
    except Concept.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EquationSerializer(concept.equations, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not isinstance(request.data, list):
            data = [request.data]
        else:
            data = request.data
        for i in range(len(data)):
            data[i]['parent_concept'] = concept
        # https://stackoverflow.com/questions/43435247/creating-multiple-objects-with-one-request-in-django-and-django-rest-framework/43469079
        equation_serializer = EquationSerializer(data=data, many=True)
        if equation_serializer.is_valid():
            equations = {
                "equations": {
                    "add": equation_serializer.save()
                }
            }
            concept_serializer = ConceptSerializer(concept,data=equations, partial=True)
            if concept_serializer.is_valid():
                concept_serializer.save()
                return Response(equation_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(concept_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(equation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def equation_detail(request, concept_id, equation_id):
    """
    Retrieve, update or delete a code equation.
    """
    try:
        concept = Concept.objects.get(pk=concept_id)
    except Concept.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    try:
        equation = Equation.objects.get(pk=equation_id)
    except Equation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not equation.parent_concept == concept:
        return Response("Equation({:s}) does not belong to Concept({:s})"\
            .format(equation_id, concept_id),\
            status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = EquationSerializer(equation)
        return Response(serializer.data)

    elif request.method == 'PUT' or request.method == 'PATCH':
        partial = True if request.method == 'PATCH' else False
        serializer = EquationSerializer(equation, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        equation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
