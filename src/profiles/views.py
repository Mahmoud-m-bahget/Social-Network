from django.shortcuts import render , redirect ,get_object_or_404
from .models import Profile , Relationship
from .forms import ProfileModelForm  
from django.views.generic import ListView ,DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None , instance=profile)
    confirm = False

    if request.method =='POST':
        if form.is_valid():
            form.save
            confirm = True
    context = {
        'profile' : profile,
        'form' : form,
        'confirm' : confirm,
    }

    return render(request , 'profiles/myprofile.html' , context)

@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)
    reuslt = list(map(lambda x: x.sender,qs))
    is_empty = False
    if len(reuslt)==0:
        is_empty =True

    context = {
        'qs':reuslt,
        'is_empty' : is_empty,
    }

    return render(request , 'profiles/my_invites.html',context)

@login_required
def accept_invatations(request):
    if request.method =='POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        recevier = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship ,sender = sender , recevier = recevier)
        if rel.status =='send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')

@login_required
def reject_invatations(request):
    if request.method =='POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        recevier = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship ,sender = sender , recevier = recevier)
        rel.delete()
        return redirect('profiles:my-invites-view')


    

@login_required
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {
        'qs':qs
    }

    return render(request , 'profiles/to_invite_list.html',context)

@login_required
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {
        'qs':qs
    }

    return render(request , 'profiles/profile_list.html',context)

class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'profiles/detail.html'
    

    def get_object(self ,slug =None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug = slug)
        return profile
    
    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact = self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(recevier=profile)
        rel_receiver = []
        rel_sender = []
        
        for item in rel_r:
            rel_receiver.append(item.recevier.user)
        for item in rel_s:
            rel_receiver.append(item.sender.user)
      
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['posts'] = self.get_object().get_all_authors_postss()
        context['len_posts'] = True if len(self.get_object().get_all_authors_postss()) > 0 else False
        return context






class ProfileListView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    context_object_name = 'qs'

    def get_queryset(self):
            qs = Profile.objects.get_all_profiles(self.request.user)
            return qs


    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact = self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(recevier=profile)
        rel_receiver = []
        rel_sender = []
        
        for item in rel_r:
            rel_receiver.append(item.recevier.user)
        for item in rel_s:
            rel_receiver.append(item.sender.user)
      
        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False

        if len(self.get_queryset()) == 0:
            context['is_empty'] = True


     
        return context

@login_required
def send_invatations(request):
    if request.method =='POST':
        pk = request.POST.get('profile_pk')
        user = request.user 
        sender = Profile.objects.get(user=user)
        receiver =Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender= sender , recevier=receiver , status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile_view')


@login_required
def remove_from_friends(request):
    if request.method =='POST':
        pk = request.POST.get('profile_pk')
        user = request.user 
        sender = Profile.objects.get(user=user)
        receiver =Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(Q(sender = sender) & Q(recevier = receiver) | Q (sender = receiver) & Q(recevier = sender))
        rel.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my_profile_view')




