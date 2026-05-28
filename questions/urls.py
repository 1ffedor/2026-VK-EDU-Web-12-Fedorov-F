from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('tag/<slug:tag>/', views.tag, name='tag'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask, name='ask'),
    path('api/question/vote/', views.vote_question, name='vote_question'),
    path('api/answer/vote/', views.vote_answer, name='vote_answer'),
    path('api/answer/correct/', views.mark_correct_answer, name='mark_correct_answer'),
    path('api/search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('api/centrifugo/token/', views.centrifugo_token, name='centrifugo_token'),
    path('api/question/<int:pk>/answer/<int:answer_id>/card/', views.answer_card, name='answer_card'),
]
