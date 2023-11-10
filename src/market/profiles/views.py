from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import UserRegistrationForm
from .models import Profile


@login_required
def dashboard(request):
    return render(request, 'profiles/dashboard.html')


def register(request):
    if request.method =='POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'profiles/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'profiles/register.html', {'new_user': new_user})
