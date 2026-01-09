from django.urls import path
from .views import upload, system_error, graph, pdf_graph, pdf_stats, stats
urlpatterns = [
    path('upload/', upload, name='upload'),
    path('error/', system_error, name='error'),
    path('graph/', graph, name='graph'),
    path('stats/', stats, name='stats'),
    path('pdf_graph/', pdf_graph, name= 'pdf-graph' ),
    path('pdf_stats/', pdf_stats, name= 'pdf-stats' ),
    
]
