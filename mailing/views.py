from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from mailing.forms import MailingForm, BlogForm
from mailing.models import Mailing, Client, Message, Blog


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['total_mailings'] = Mailing.objects.count()
            context['active_mailings'] = Mailing.objects.filter(status='active').count()
            context['total_clients'] = Client.objects.count()
            context['total_messages'] = Message.objects.count()
            context['latest_blogs'] = Blog.objects.order_by('-creation_date')[:3]
        for i in Blog.objects.order_by('-creation_date')[:3]:
            i.views += 1
            i.save()
        return context


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing/list.html'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing/detail.html'

    def has_permission(self):
        user = self.request.user
        product_owner = self.get_object().owner
        if user == product_owner:
            return True
        return False


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing/form.html'
    success_url = reverse_lazy('mailing:list_mailing')

    def has_permission(self):
        user = self.request.user
        product_owner = self.get_object().owner
        if user == product_owner:
            return True
        return False


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing/form.html'
    success_url = reverse_lazy('mailing:list_mailing')

    def has_permission(self):
        user = self.request.user
        product_owner = self.get_object().owner
        if user == product_owner:
            return True
        return False


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing/delete.html'
    success_url = reverse_lazy('mailing:list_mailing')

    def has_permission(self):
        user = self.request.user
        product_owner = self.get_object().owner
        if user == product_owner:
            return True
        return False


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailing/client/list.html'

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    template_name = 'mailing/client/detail.html'

    def has_permission(self):
        user = self.request.user
        product_owner = self.get_object().owner
        if user == product_owner:
            return True
        return False


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'mailing/client/form.html'
    fields = ['email', 'full_name', 'commentary']
    success_url = reverse_lazy('mailing:list_client')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    template_name = 'mailing/client/form.html'
    fields = ['email', 'full_name', 'commentary']
    success_url = reverse_lazy('mailing:list_client')

    def has_permission(self):
        user = self.request.user
        product_owner = self.get_object().owner
        if user == product_owner:
            return True
        return False


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    template_name = 'mailing/client/delete.html'
    success_url = reverse_lazy('mailing:list_client')

    def has_permission(self):
        user = self.request.user
        product_owner = self.get_object().owner
        if user == product_owner:
            return True
        return False


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message/list.html'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message/detail.html'

    def has_permission(self):
        user = self.request.user
        product_owner = self.get_object().owner
        if user == product_owner:
            return True
        return False


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = 'mailing/message/form.html'
    fields = ['theme', 'text']
    success_url = reverse_lazy('mailing:list_message')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    template_name = 'mailing/message/form.html'
    fields = ['theme', 'text']
    success_url = reverse_lazy('mailing:list_message')

    def has_permission(self):
        user = self.request.user
        product_owner = self.get_object().owner
        if user == product_owner:
            return True
        return False


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailing/message/delete.html'
    success_url = reverse_lazy('mailing:list_message')

    def has_permission(self):
        user = self.request.user
        product_owner = self.get_object().owner
        if user == product_owner:
            return True
        return False


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'
    success_url = reverse_lazy('index')
    permission_required = 'mailing.add_blog'
    raise_exception = True
