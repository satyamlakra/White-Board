from rest_framework import serializers
from intro.models import boardobject

class boardSerializer(serializers.ModelSerializer):
   class Meta:
      model = boardobject
      fields ='__all__'