from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View

from blog.models import Post
from spaces.models import Space
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView
from .models import Profile, Category, User
# from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

def follow_unfollow_profile(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)
        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
    return redirect('profiles:profile-list')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            selected_categories = form.cleaned_data.get('categories')
            user.profile.categories.set(selected_categories)
            user.profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

class ProfileListView(ListView):
    model = Profile
    template_name = 'users/user_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/user_detail.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False
        context["follow"] = follow
        return context


def recommend_users(request):
    # Get the categories checked by the user
    selected_categories = request.user.profile.categories.all()

    # Filter spaces which have these categories
    users = Profile.objects.filter(categories__in=selected_categories)

    # For each space, get all posts and calculate the total posts' amount and average likes
    """relevant_users = []
    first_encounter = []
    for user in users:
        if user in first_encounter and user not in relevant_users and user.id != request.user.id:
            relevant_users.append(user)
        else:
            first_encounter.append(user)"""

    counts = {}
    relevant_users = []

    for user in users:
        counts[user] = counts.get(user, 0) + 1

        if counts[user] >= 2 and user not in relevant_users and user.id != request.user.id:
            relevant_users.append(user)

    # Pass the relevant spaces to the template
    return render(request, 'users/recommendations.html', {'users': relevant_users})

