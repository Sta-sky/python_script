from django.urls import path
from . import views

handler403 = views.permission_denied
handler404 = views.page_not_found
handler500 = views.server_error


urlpatterns = [
    path('student/', views.index),
    path('student/<int:number>', views.test),
    path('student/<int:number>/<str:test>', views.url_test),
]






