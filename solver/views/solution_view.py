from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Concept, Equation, Equation
from ..serializers import ConceptSerializer, EquationSerializer, EquationSerializer
import sympy
from .. import kernel

@api_view(['GET'])
def concept_solution(request, concept_id):
    """
    Retrieve, update or delete a code concept.
    """
    # Functions of request.query_params: https://kite.com/python/docs/django.http.QueryDict
    hypothesis_str = request.query_params.get('hypothesis')
    goal_str = request.query_params.get('goal')

    try:
        concept = Concept.objects.get(pk=concept_id)
    except Concept.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    local_vars = {}
    for attribute in concept.attributes.get_queryset():
        symbol = attribute.symbol
        local_vars[symbol] = sympy.symbols(symbol)
    
    equations = sympy.FiniteSet()
    for eq in concept.equations.get_queryset():
        equations += sympy.FiniteSet(sympy.sympify(eq.syntax,local_vars))

    hypothesis = sympy.FiniteSet(*sympy.sympify(hypothesis_str, locals=local_vars))
    goal = sympy.FiniteSet(*sympy.sympify(goal_str, locals=local_vars))

    known, solution, giaThuyet = kernel.SuyDienTien(hypothesis, goal, TapDangThuc=equations)

    return Response({
        "hypothesis": hypothesis_str,
        "goal": goal_str,
        "solution": [{
            step[0]:str(step[1]),
            step[2]:str(step[3]),
            step[4]:str(step[5])
        } for step in solution]
    })