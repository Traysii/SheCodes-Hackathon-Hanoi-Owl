from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from django.http import HttpResponse
from django.views import View


# Create your views here.

class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main')

class Register(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(Register, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')
        return super(Register, self).get(*args, **kwargs)
    
class Result(View):
    def get(self, request):
        file_path = 'ai.csv'  # Đường dẫn tới tệp dữ liệu của bạn

        count_focus = 0
        count_nonefocus = 0

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    _, label = line.strip().split(',')
                    if label == '0':
                        count_focus += 1
                    elif label == '1':
                        count_nonefocus += 1
        except FileNotFoundError:
            return HttpResponse("File not found.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")

        return render(request, 'main.html', {'count_focus': count_focus, 'count_nonefous': count_nonefocus}) 