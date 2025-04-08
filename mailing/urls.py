from django.urls import path
from django.views.decorators.cache import cache_page
from mailing.views import (
    IndexView, MailingListView, MailingDetailView, MailingCreateView,
    MailingUpdateView, MailingDeleteView, ClientListView, ClientDetailView,
    ClientCreateView, ClientUpdateView, ClientDeleteView, MessageListView,
    MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView
)

app_name = 'mailing'

urlpatterns = [
    path('', cache_page(60)(IndexView.as_view()), name='index'),

    path('mailings/', MailingListView.as_view(), name='list_mailing'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='detail_mailing'),
    path('mailing/create/', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing/update/<int:pk>/', MailingUpdateView.as_view(), name='update_mailing'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='delete_mailing'),

    path('clients/', ClientListView.as_view(), name='list_client'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='detail_client'),
    path('client/create/', ClientCreateView.as_view(), name='create_client'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

    path('messages/', MessageListView.as_view(), name='list_message'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='detail_message'),
    path('message/create/', MessageCreateView.as_view(), name='create_message'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),


]
