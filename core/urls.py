# encrypt_inc/apps/core/urls.py
from django.urls import path
from .views import ProposalSubmitView, ProposalQueueView

# API Routing Table

urlpatterns = [
    path('proposals/submit/', ProposalSubmitView.as_view(), name='proposal-submit'),
    path('proposals/queue/', ProposalQueueView.as_view(), name='proposal-queue'),
]