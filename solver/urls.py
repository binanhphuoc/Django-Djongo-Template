from django.urls import path

import solver.views as views

app_name = "concepts"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('concepts/', views.concept_list),
    path('concepts/<int:pk>/', views.concept_detail),
]