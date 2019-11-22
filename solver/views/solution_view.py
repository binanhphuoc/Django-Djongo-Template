from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Concept, Equation, Equation
from ..serializers import ConceptSerializer, EquationSerializer, EquationSerializer

@api_view(['GET'])
def concept_solution(request, name):
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