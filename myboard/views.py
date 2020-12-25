from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from myboard.forms import RegisterForm, NewtaskForm, UpdateAssignForm, UpdateTextForm, UpdateStatusForm
from myboard.models import Task, Profile


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    next_page = '/'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RegisterForm()
        return context

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        credentials = form.cleaned_data
        profile = authenticate(username=credentials['username'],
                               password=credentials['password1'])
        login(self.request, profile)
        return HttpResponseRedirect(reverse_lazy('index'))

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong :(')
        return self.render_to_response(self.get_context_data(form=form))


class LoginUser(LoginView):
    template_name = 'login.html'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    redirect_field_name = 'next'


class Index(ListView):
    template_name = 'index.html'
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'assignees': Profile.objects.all(),
                        'create_form': NewtaskForm,
                        'assign_form': UpdateAssignForm, })
        return context


class CreateTask(LoginRequiredMixin, CreateView):
    form_class = NewtaskForm
    model = Task
    success_url = reverse_lazy('index')
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.created_by:
                obj.created_by = self.request.user
                obj.save()
                messages.success(self.request, 'Created! :)')
                return HttpResponseRedirect(self.success_url)
            messages.error(self.request, 'Owner is needed :(')
            return HttpResponseRedirect('/')

        messages.error(self.request, 'Something went wrong :(')
        return HttpResponseRedirect('/')


class UpdateAssign(LoginRequiredMixin, UpdateView):
    form_class = UpdateAssignForm
    model = Task
    success_url = reverse_lazy('index')
    http_method_names = ['post', ]

    def form_valid(self, form):
        task = Task.objects.get(id=self.kwargs['pk'])
        if self.request.POST.get('assigned_to'):
            if int(self.request.POST.get('assigned_to')) == task.created_by_id or self.request.user.is_superuser:
                user = Profile.objects.get(id=self.request.POST.get('assigned_to'))
                task.assigned_to = user
                obj = form.save(commit=False)
                obj.save()
                messages.success(self.request, 'Assigned! :)')
                return HttpResponseRedirect(self.success_url)

            messages.error(self.request, 'For owners only! ')
            return HttpResponseRedirect('/')
        else:
            user = None
            task.assigned_to = user
            obj = form.save(commit=False)
            obj.save()
            messages.success(self.request, 'Assigned! :)')
            return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, 'Something went wrong :(')
        return HttpResponseRedirect('/')


class UpdateDescription(LoginRequiredMixin, UpdateView):
    form_class = UpdateTextForm
    model = Task
    success_url = reverse_lazy('index')
    http_method_names = ['post', 'get']
    template_name = 'task_update.html'

    def form_valid(self, form):
        task = Task.objects.get(id=self.kwargs['pk'])
        obj = form.save(commit=False)
        if not int(self.request.user.id) == task.created_by_id and not self.request.user.is_superuser:
            messages.error(self.request, 'For owners only!')
            return HttpResponseRedirect('/')
        obj.save()
        messages.success(self.request, 'Updated! :)')
        return HttpResponseRedirect(self.success_url)


class UpdateStatus(LoginRequiredMixin, UpdateView):
    form_class = UpdateStatusForm
    model = Task
    success_url = reverse_lazy('index')
    http_method_names = ['post', 'get']
    template_name = 'index.html'

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if int(self.request.user.id) == task.assigned_to_id and not self.request.user.is_superuser:
            if self.request.POST['action'] == 'left':
                if task.status != 1:
                    task.status -= 1
                    task.save()
                    messages.success(self.request, 'Status Changed! :)')
                    return HttpResponseRedirect(self.success_url)
            if self.request.POST['action'] == 'right':
                if task.status != 4:
                    task.status += 1
                    task.save()
                    messages.success(self.request, 'Status Changed! :)')
                    return HttpResponseRedirect(self.success_url)

            messages.error(self.request, 'Impossible to update :(')
            return HttpResponseRedirect(self.success_url)
        elif self.request.user.is_superuser:
            if self.request.POST['action'] == 'left':
                if task.status == 5:
                    task.status -= 1
                    task.save()
                    messages.success(self.request, 'Status Changed! :)')
                    return HttpResponseRedirect(self.success_url)
            if self.request.POST['action'] == 'right':
                if task.status == 4:
                    task.status += 1
                    task.save()
                    messages.success(self.request, 'Status Changed! :)')
                    return HttpResponseRedirect(self.success_url)
            messages.error(self.request, 'Only done/ready allowed :(')
            return HttpResponseRedirect(self.success_url)
        else:
            messages.error(self.request, 'You are not authorized! :(')
            return HttpResponseRedirect(self.success_url)


class DeleteCard(PermissionRequiredMixin, DeleteView):
    permission_required = 'user.delete_user'
    model = Task
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        if self.request.POST['action'] == 'Confirm':
            messages.info(self.request, 'Deleted! :)')
            task.delete()
            return HttpResponseRedirect(self.success_url)

        messages.error(self.request, 'Something went wrong :(')
        return HttpResponseRedirect(self.success_url)
