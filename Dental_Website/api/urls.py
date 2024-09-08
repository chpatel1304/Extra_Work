from django.urls import path
from .views import SaveDataView, SearchFormDataView

urlpatterns = [
    path('save-data/', SaveDataView.as_view(), name='save_data'),
    path('search/', SearchFormDataView.as_view(), name='search_data'),
]
