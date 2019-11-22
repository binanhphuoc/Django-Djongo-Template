from rest_framework import serializers
from .models import Concept, Attribute, Equation

# SERIALIZERS

class AttributeSerializer(serializers.ModelSerializer):
    _id = serializers.MongoIdField(read_only=True)
    parent_concept = serializers.MongoIdField()
    class Meta:
        model = Attribute
        fields = ['_id','symbol','parent_concept','description']

class EquationSerializer(serializers.ModelSerializer):
    _id = serializers.MongoIdField(read_only=True)
    parent_concept = serializers.MongoIdField()
    class Meta:
        model = Equation
        fields = ['_id','parent_concept','syntax', 'name','description']

class ConceptSerializer(serializers.ModelSerializer):
    _id = serializers.MongoIdField(read_only=True)
    equations = serializers.MongoArrayReferenceField(serializer=EquationSerializer)
    attributes = serializers.MongoArrayReferenceField(serializer=AttributeSerializer)

    class Meta:
        model = Concept
        fields = ['_id','name','attributes','equations']