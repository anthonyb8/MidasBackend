from rest_framework import viewsets
from .models import RegressionAnalysis
from .serializers import RegressionAnalysisSerializer

class RegressionAnalysisViewSet(viewsets.ModelViewSet):
    queryset = RegressionAnalysis.objects.all()
    serializer_class = RegressionAnalysisSerializer
