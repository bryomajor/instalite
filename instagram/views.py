from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignupForm

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(reuest)
            mail_subject = 'Activate Your Instagram Account'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.''<a href="/accounts/login/"> Click here </a>')
    else:
        return HttpResponse('Activation link is invalid!''<br> If you have an account <a href="/accounts/login/"> Log in here </a>')

@login_required(login_url='/accounts/login/')
def timeline(request):
    images = Image.get_all_images()
    likes = Likes.objects.all()
    profiles = Profile.objects.all()
    comments = Comments.objects.all()
    profile_pic = User.objects.all()
    following = Follow.objects.following(request.user)
    form = CommentForm()
    id = request.user.id
    liked_images = Likes.objects.filter(user_id=id)
    mylist = [i.image_id for i in liked_images]
    title = 'Home'
    return render(request, 'index.html', {'title':title, 'images':images, 'profile_pic':profile_pic, 'following': following, 'form':form, 'comments':comments, 'profiles':profiles, 'likes':likes, 'list':mylist})
