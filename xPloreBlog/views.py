from django.shortcuts import render, redirect
from . models import Post, Project, Tag, Author, PostComment, Reply, Category, Status
from .utils import generate_chart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
import smtplib
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from itertools import chain
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from itertools import chain
from django.views.generic import ListView
# ######User Authentication ##########
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.utils.encoding import force_bytes, force_str as force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.template import RequestContext
from .forms import NewUserForm, SetPasswordForm, PasswordResetForm, UserLoginForm, AuthenticationForm, PasswordChangeForm, PostForm
from django.db.models.query_utils import Q
from .decorators import user_not_authenticated

# ####################################
import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe
# ##########GRAVATAR #################
import datetime

current_date = datetime.date.today()

EMAIL_HOST_USER, EMAIL = 'appstechemail@gmail.com', 'appstechemail@gmail.com'
EMAIL_HOST_PASSWORD, EMAIL_PASSWORD = 'skkwkacxjplesoak', 'skkwkacxjplesoak'
EMAIL_HOST, SMTP_ADDRESS = 'smtp.gmail.com', 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Gravatar###########################

register = template.Library()

# return only the URL of the gravatar
# TEMPLATE USE:  {{ email|gravatar_url:150 }}


@register.filter
def gravatar_url(email='appstechemail@gmail.com', size=40):
    default = "https://example.com/static/images/defaultavatar.jpg"
    return "https://www.gravatar.com/avatar/%s?%s" % (hashlib.md5(email.lower().encode('utf-8')).hexdigest(), urllib.parse.urlencode({'d': default, 's': str(size)}))

# return an image tag with the gravatar
# TEMPLATE USE:  {{ email|gravatar:150 }}


@register.filter
def gravatar(email='appstechemail@gmail.com', size=40):
    url = gravatar_url(email, size)
    return mark_safe('<img src="%s" width="%d" height="%d">' % (url, size, size))

# ##########GRAVATAR #################


# Create your views here.

def send_mail(from_email, to_email, subject, html_content, logo="xPloreBlog/static/img/pmlogo.png"):
    html_content = html_content

    # Create a multipart message container
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    # print(f"msg: {msg}")

    # Attach the HTML content to the email
    html_message = MIMEText(html_content, 'html')
    # print(f"html_message: {html_message}")
    msg.attach(html_message)

    # Image Embedded
    # This example assumes the image is in the current directory
    # fp = open('C:/MyFolder/Python/pythonProject/PMHut-Blog/static/assets/img/pmlogo.png', 'rb')
    fp = open(logo, 'rb')
    msg_image = MIMEImage(fp.read())
    fp.close()

    # Define the image's ID as referenced in password-change.html
    msg_image.add_header('Content-ID', '<image1>')
    msg_image.add_header('Content-Disposition', 'inline',
                         filename='pmlhutlogo.png')
    msg.attach(msg_image)

    with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        connection.login(EMAIL, EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=msg['From'], to_addrs=msg['To'], msg=msg.as_string())

# Register New User ##############################


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user:
                # to get the domain of the current
                UID = urlsafe_base64_encode(force_bytes(user.pk))
                TOKEN = account_activation_token.make_token(user)
                # print(f"UID and Token: {UID} - {TOKEN}")
                current_site = get_current_site(request)
                mail_subject = 'Activation link has been sent to your email id'

                html_content = render_to_string('xPloreBlog/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': UID,
                    'token': TOKEN,
                })

                to_email = user.email
                full_name = f"{user.first_name}-{user.last_name}"

                send_mail(from_email=EMAIL, to_email=to_email, subject=mail_subject, html_content=html_content,
                          logo='xPloreBlog/static/img/pmlogo.png')

                return redirect('account-activation-sent')

                # messages.success(
                #     request, "<p class='h6, text-success'>Welcome aboard! Your registration is complete.</p>")
                # return redirect("")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
        # messages.error(
        #     request, "<p class='h6 text-danger'>We're sorry, but we couldn't complete your registration. Please ensure that the information you provided is correct and try again.</p>")
    form = NewUserForm()
    return render(request=request, template_name="xPloreBlog/signup/register.html", context={"register_form": form})

# User Sign In ###################################


def ulogin(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # log in user
            user = form.get_user()
            login(request, user)
            return redirect('all-posts')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    form = UserLoginForm()
    return render(request, 'xPloreBlog/signup/login.html', {"login_form": form})

# User Authentication #############################


def account_activation_sent(request):
    return render(request, 'xPloreBlog/account_activation_sent.html')


def invalid_login(request):
    return render(request, 'xPloreBlog/invalid_login.html')


def log_out(request):
    logout(request)
    return render(request, 'xPloreBlog/logout.html')


def activate(request, uidb64, token):
    # User = settings.AUTH_USER_MODEL
    User = get_user_model()

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print(f"UID: {uid}")
        user = User.objects.get(pk=uid)
        print(f"User: {user}")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account-activation-complete')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def account_activation_complete(request):
    return render(request, 'xPloreBlog/account_activation_complete.html')


# Reset Password #################################################################################

def chg_password(request):
    return render(request, 'xPloreBlog/reset/chg_password.html')

# User to enter new Password and New password confirmation


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'xPloreBlog/reset/password_reset_confirm.html', {'form': form})

# 1. Reset Password form invoked from Forgotten password on login screen


@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                html_content = render_to_string("xPloreBlog/reset/password_reset_request_mail.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })

                to_email = associated_user.email
                full_name = f"{
                    associated_user.first_name}-{associated_user.last_name}"

                try:
                    send_mail(from_email=EMAIL, to_email=to_email, subject=subject, html_content=html_content,
                              logo='xPloreBlog/static/img/pmlogo.png')

                    messages.success(request,
                                     """
                        <h5>Password reset sent</h5><hr>
                        <p class='fs-1 text-success'>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered.
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address
                            you registered with, and check your spam folder.
                        </p>
                        """
                                     )
                except:
                    messages.error(
                        request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")
            else:
                messages.error(
                    request, "<p class='fs-1 text-danger'>Please enter a valid email address.</p>")

            return redirect('password-reset-request')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(
                    request, """<p class='fs-1 text-danger'>You must pass the reCAPTCHA test</p>""")
                continue

    form = PasswordResetForm()
    return render(
        request=request,
        template_name="xPloreBlog/reset/password_reset.html",
        context={"form": form}
    )


# 2. Reset Password Confirmation


def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(
                    request, "<p class='h6, text-success'>Your password has been set. You may go ahead and <b>log in </b> now.</p>")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'xPloreBlog/reset/password_reset_confirm.html', {'form': form})
    else:
        messages.error(
            request, "<p class='h6 text-danger'>Sorry, this link has expired. Please try again or request a new link.</p>")

    messages.error(
        request, "<p class='h6 text-danger'>Something went wrong, redirecting back to Password reset request</p>")
    return redirect('password-reset-request')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # To keep the user logged in
            update_session_auth_hash(request, user)
            return redirect('password-change-done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'xPloreBlog/reset/change_password.html', {'update_password_form': form})


@login_required
def password_change_done(request):
    return render(request, 'xPloreBlog/reset/password_change_done.html')
# User Authentication Ends #############################


@register.filter
def truncatechars_filled(value, arg):
    """
    Truncates a string after a certain number of characters and fills remaining space with gaps.
    Usage: {{ value|truncatechars_filled:50 }}
    """
    try:
        length = int(arg)
    except ValueError:
        return value  # Invalid argument, return the original string

    if len(value) > length:
        return value[:length] + '...'
    else:
        return value + ' ' * (length - len(value))


def get_all_posts(request):
    if request.method == 'GET' and 'searchbtn' in request.GET:
        query = request.GET.get('query', None)
        if query is not None:
            blog_results = Post.objects.search(query)
            model = blog_results.model
            model_name = model.__name__
            # author_results = Author.objects.search(query)
            # Category_results = Category.objects.search(query)
            # tag_results = Tag.objects.search(query)

            # combine querysets
            queryset_chain = chain(
                blog_results,
                # author_results,
                # Category_results,
                # tag_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            q_count = len(qs)  # since qs is actually a list
            # print(f"querysets: {qs}")
            # print(f"q_count: {q_count}")

            page = request.GET.get('page', 1)
            # print(f"pageno: {page}")
            paginator = Paginator(qs, 5)  # paginate_by 5
            try:
                qs = paginator.page(page)
                # print(f"Try Qs pageno: {qs}")
            except PageNotAnInteger:
                qs = paginator.page(1)
                # print(f"Except pageno: {qs}")
            except EmptyPage:
                qs = paginator.page(paginator.num_pages)
                # print(f"Empty pageno: {qs}")

            return render(request, 'xPloreBlog/search/search_view.html', {'page': page, 'query': query, 'qs': qs, 'q_count': q_count, 'object_name': model_name})
        return Post.objects.none()  # just an empty queryset as default

    posts = Post.objects.all()
    page = request.GET.get('page', 1)
    # print(f"Posts pageno: {page}")
    paginator = Paginator(posts, 4)  # paginate_by 5
    try:
        posts = paginator.page(page)
        # print(f"Try post pageno: {posts}")
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'xPloreBlog/index.html', {'page': page, 'posts': posts, 'current_date': current_date})


def get_all_posts_category(request, category):
    # print(f"CATEGORY: {category}")
    # category_id = Post.objects.get(category__name=category).id
    # print(f"Category Id: {category_id}")
    posts = Post.objects.all().filter(
        category__name=category)

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 2)  # paginate_by 5
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'xPloreBlog/posts_category.html', {'page': page, 'posts': posts})


def top_rated_posts(request):

    top_3_posts = (Post.objects.annotate(avg_rating=Avg(
        'cposts__rating')).order_by('-avg_rating')[:3])
    top_1_post = top_3_posts[0]
    top_2_post = top_3_posts[1]
    top_3_post = top_3_posts[2]

    return render(request, 'xPloreBlog/welcome.html', {'top_1_post': top_1_post, 'top_2_post': top_2_post, 'top_3_post': top_3_post, })


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, 'xPloreBlog/read_later_posts.html', context)

    def post(self, request):
        # Don't use request.session["stored_posts"]. It fails if exists or have no value
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        else:
            stored_posts.remove(post_id)
            request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect("/")


def single_post(request, slug):
    stored_posts = request.session.get("stored_posts")
    # print(f"stored posts: {stored_posts}")
    post = get_object_or_404(Post, slug=slug)
    comments = Post.objects.get(
        id=post.id).cposts.all().order_by('-created_on', '-id')

    comment_ids = [comment.id for comment in comments]
    replies = Reply.objects.filter(
        r_comment__id__in=comment_ids).order_by('-created_on')
    # Related Posts #################
    related_posts = Post.objects.all().filter(
        category=post.category).exclude(id=post.id).order_by('-created_on')[:3]
    # for Categories ################
    # category_list = Post.objects.order_by().values_list('category').distinct()
    category_list = Post.objects.order_by().values_list(
        'category__name', flat=True).distinct().order_by('category__name')
    # print(f"Category: {category_list}")
    categories = list(map(''.join, category_list))
    # for post tag ##################
    post_tags = post.tag.all().order_by('tag_title')
    tags = []
    for post_tag in post_tags:
        tags.append(post_tag.tag_title)
    # print(tags)
    tag = " . ".join(tags)
    # for Gravatar #################
    if request.user.is_authenticated:
        p_gravatar_url = gravatar_url(email=request.user.email)
        print(f"Gravatar: {p_gravatar_url}")
    else:
        p_gravatar_url = gravatar_url()
    # p_gravatar_url = gravatar_url()
    print(p_gravatar_url)

    # print(f"Current Users: {request.user.email}")

    # Comment Form #################################
    if request.method == 'POST' and 'commentbtnform' in request.POST and request.user.is_authenticated:
        reader = User.objects.get(username=request.user)
        rating = request.POST['rating']
        comment = request.POST['message']

        # Create a new Comment in the database using the PostComment model
        PostComment.objects.create(
            comment=comment, post=post, reader=reader, rating=rating, created_on=current_date)
        # Repopulate comments to refresh
        comments = Post.objects.get(
            id=post.id).cposts.all().order_by('-created_on', '-id')

    elif request.method == 'POST' and 'replybtnform' in request.POST and request.user.is_authenticated:
        reader = User.objects.get(username=request.user)
        # Remember:
        # commentId field should be of type = 'hidden' and no disabled property
        # The disabled input field is kept for display purposes only, but its value won't be submitted with the form.
        # With this change, the commentId value will be included in the form submission, allowing you to retrieve it in your Django view using request.POST.get('commentId').

        comment_id = request.POST.get('commentId')
        r_text = request.POST['message']
        r_comment = PostComment.objects.get(id=comment_id)
        Reply.objects.create(r_text=r_text, r_comment=r_comment,
                             reader=reader, created_on=current_date)

    return render(request, "xPloreBlog/post.html", {'post': post, 'comments': comments, 'replies': replies, 'gravatar_url': p_gravatar_url, 'tags': post_tags, 'categories': categories, 'related_posts': related_posts, 'stored_posts': stored_posts})

    # def get_context_data(self, **kwargs):
    #     context = super(NewPostView, self).get_context_data(**kwargs)
    #     context['created_by'] = self.request.user

    #     return context


def posts_by_tag(request, tag_title):
    tag = get_object_or_404(Tag, tag_title=tag_title)
    posts = Post.objects.filter(tag=tag).order_by('-created_on', '-id')

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 2)  # paginate_by 5
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'xPloreBlog/posts_by_tag.html', {'page': page, 'tag': tag, 'posts': posts})


class NewPostView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'xPloreBlog/post_creation_edit/new_blog_post.html', {'new_form': form})

    def post(self, request, post_id=None):
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.created_by = request.user
            post.updated_by = request.user
            form.save()
            action_mode = "new"

            # Redirect to a URL with query parameters
            return redirect('new-post-success', action_mode='new')

        return render(request, 'xPloreBlog/post_creation_edit/new_blog_post.html', {'new_form': form})


class EditPostView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        if post_id:
            post = get_object_or_404(Post, id=post_id)
            form = PostForm(instance=post)
            return render(request, 'xPloreBlog/post_creation_edit/edit_blog_post.html', {'edit_form': form, 'post': post})

    def post(self, request, post_id):

        post = get_object_or_404(Post, id=post_id)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.updated_by = request.user
            form.save()

            # Redirect to a URL with query parameters
            # return \Redirect::route('new_post_success', $id)->with('message', 'State saved correctly!!!');
            return redirect('new-post-success', action_mode='update')

        return render(request, 'xPloreBlog/post_creation_edit/edit_blog_post.html', {'edit_form': form, 'post': post})


@login_required
def new_post_success(request, action_mode):
    message = ''
    print(f"Action Mode: {action_mode}")
    if action_mode == 'new':
        message = 'Success! Your new blog/record has been created.'
    elif action_mode == 'update':
        message = 'Your blog post has been updated successfully..'

    return render(request, 'xPloreBlog/post_creation_edit/new_post_success.html', {'message': message})


# Welcome Function
def welcome(request):
    return render(request, 'xPloreBlog/welcome.html')

# About Function


def about(request):
    about = Project.objects.get(id=1)
    return render(request, "xPloreBlog/about.html", {'about': about})


@ csrf_exempt
def contact(request):

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        html_content = render_to_string('xPloreBlog/contact-mail.html', {
                                        'msg_body': message, 'name': name, 'subject': subject, 'email': email})
        send_mail(from_email=email, to_email=EMAIL, subject=subject, html_content=html_content,
                  logo='xPloreBlog/static/img/pmlogo.png')

        return render(request, "xPloreBlog/contact.html", {'info': "Successfully sent your message"})
    else:
        return render(request, "xPloreBlog/contact.html")

    # views.py


def filter_zero_values(data):
    filtered_data = {
        'labels': [],
        'values': []
    }
    for label, value in zip(data['labels'], data['values']):
        if value > 0:
            filtered_data['labels'].append(label)
            filtered_data['values'].append(value)
    return filtered_data


def dashboard_view(request):
    # Aggregate data for the dashboard
    top_rated_posts = (
        Post.objects.annotate(avg_rating=Avg('cposts__rating'))
        .order_by('-avg_rating')[:5]
    )
    category_wise_posts = (
        Category.objects.annotate(post_count=Count('categories'))
        .order_by('-post_count')
    )
    author_wise_posts = (
        Author.objects.annotate(post_count=Count('posts'))
        .order_by('-post_count')
    )
    recent_posts = Post.objects.filter(
        created_on__gte=timezone.now() - timedelta(days=7)
    ).order_by('-created_on')
    tag_wise_posts = (
        Tag.objects.annotate(post_count=Count('post'))
        .order_by('-post_count')
    )

    # Prepare data for charts
    top_rated_posts_data = {
        'labels': [post.title for post in top_rated_posts],
        'values': [post.avg_rating for post in top_rated_posts]
    }
    top_rated_posts_data = filter_zero_values(top_rated_posts_data)

    category_wise_posts_data = {
        'labels': [category.name for category in category_wise_posts],
        'values': [category.post_count for category in category_wise_posts]
    }
    category_wise_posts_data = filter_zero_values(category_wise_posts_data)

    author_wise_posts_data = {
        'labels': [author.user.first_name for author in author_wise_posts],
        'values': [author.post_count for author in author_wise_posts]
    }
    author_wise_posts_data = filter_zero_values(author_wise_posts_data)

    recent_posts_data = {
        'labels': [post.created_on for post in recent_posts],
        # Representing each new post with a value of 1
        'values': [1 for post in recent_posts]
    }
    recent_posts_data = filter_zero_values(recent_posts_data)

    tag_wise_posts_data = {
        'labels': [tag.tag_title for tag in tag_wise_posts],
        'values': [tag.post_count for tag in tag_wise_posts]
    }
    tag_wise_posts_data = filter_zero_values(tag_wise_posts_data)

    # Generate charts
    top_rated_posts_chart = generate_chart(
        top_rated_posts_data, 'bar', 'top_rated_posts')
    category_wise_posts_chart = generate_chart(
        category_wise_posts_data, 'pie', 'category_wise_posts')
    author_wise_posts_chart = generate_chart(
        author_wise_posts_data, 'bar', 'author_wise_posts')
    recent_posts_chart = generate_chart(
        recent_posts_data, 'recent_posts', 'recent_posts')
    tag_wise_posts_chart = generate_chart(
        tag_wise_posts_data, 'doughnut', 'tag_wise_posts')

    context = {
        'top_rated_posts_chart': top_rated_posts_chart,
        'category_wise_posts_chart': category_wise_posts_chart,
        'author_wise_posts_chart': author_wise_posts_chart,
        'recent_posts_chart': recent_posts_chart,
        'tag_wise_posts_chart': tag_wise_posts_chart,
    }

    return render(request, 'xPloreBlog/dashboard.html', context)
