from django.urls import path

import solver.views as views

app_name = "concepts"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('knowledgebase/concepts', views.concept_list),
    path('knowledgebase/concepts/<str:concept_id>', views.concept_detail),
    path('knowledgebase/concepts/<str:concept_id>/attributes', views.attribute_list),
    path('knowledgebase/concepts/<str:concept_id>/attributes/<str:attribute_id>', views.attribute_detail),
    path('knowledgebase/concepts/<str:concept_id>/equations', views.equation_list),
    path('knowledgebase/concepts/<str:concept_id>/equations/<str:equation_id>', views.equation_detail),
    path('inference-engine/concepts/<str:concept_id>/solution', views.concept_solution),
]