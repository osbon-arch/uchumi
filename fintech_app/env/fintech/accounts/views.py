from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import SavingsGroup
from django.contrib.auth.decorators import login_required
from .models import Contribution
from django.shortcuts import get_object_or_404
from .models import FinancialLiteracyResource
from .models import Article, Video, Quiz

@login_required
def landing_page_view(request):
    user_groups = request.user.savings_groups.all()
    total_savings = sum(group.total_savings for group in user_groups)
    recent_activities = []  # Placeholder for activities; implement as needed

    # Retrieve recent activities from groups (e.g., contributions)
    for group in user_groups:
        recent_activities.append({
            'group_name': group.name,
            'recent_update': f'You saved KSh {group.total_savings} in {group.name}.',  # Example activity
        })

    return render(request, 'accounts/landing_page.html', {
        'total_savings': total_savings,
        'recent_activities': recent_activities,
    })



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('landing')  # Replace 'home' with your homepage URL
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'accounts/login.html')
    

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                login(request, user)
                return redirect('home')  # Replace 'home' with your homepage URL
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')


def create_group_view(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        group_description = request.POST['description']
        savings_goal = request.POST['savings_goal']
        new_group = SavingsGroup.objects.create(
            name=group_name,
            description=group_description,
            savings_goal=savings_goal,
        )
        new_group.members.add(request.user)  # Add the creator as a member
        messages.success(request, f'Group "{new_group.name}" created successfully!')
        return redirect('group_list')
    return render(request, 'accounts/create_group.html')

def group_list_view(request):
    user_groups = request.user.savings_groups.all()  # Get groups for the logged-in user
    return render(request, 'accounts/group_list.html', {'groups': user_groups})

def group_detail_view(request, group_id):
    group = get_object_or_404(SavingsGroup, id=group_id)

    if request.method == 'POST':
        goal = request.POST.get('savings_goal')
        payout = request.POST.get('payout_amount')
        
        if goal:
            group.savings_goal = goal
            messages.success(request, f'Savings goal set to KSh {goal} for {group.name}!')
        if payout:
            group.payout_amount = payout
            messages.success(request, f'Payout amount set to KSh {payout} for {group.name}!')
        
        group.save()
        return redirect('group_detail', group_id=group.id)

    contributions = group.contributions.all()
    return render(request, 'accounts/group_detail.html', {
        'group': group,
        'contributions': contributions,
    })


def contribute_to_group_view(request, group_id):
    group = SavingsGroup.objects.get(id=group_id)
    if request.method == 'POST':
        amount = request.POST['amount']
        contribution = Contribution.objects.create(
            group=group,
            member=request.user,
            amount=amount,
        )
        group.total_savings += contribution.amount
        group.save()
        messages.success(request, f'You contributed KSh {contribution.amount} to {group.name}!')
        return redirect('group_detail', group_id=group.id)
    return render(request, 'accounts/contribute_to_group.html', {'group': group})

def group_contributions_view(request, group_id):
    group = SavingsGroup.objects.get(id=group_id)
    contributions = group.contributions.all()
    return render(request, 'accounts/group_contributions.html', {'group': group, 'contributions': contributions})

def payout_view(request, group_id):
    group = get_object_or_404(SavingsGroup, id=group_id)
    
    if group.is_goal_met():
        payout_amount = group.payout()
        messages.success(request, f'Payout of KSh {payout_amount} has been made from {group.name}.')
    else:
        messages.warning(request, f'Savings goal not met for {group.name}. Cannot process payout.')
    
    return redirect('group_detail', group_id=group.id)


def financial_literacy_view(request):
    resources = FinancialLiteracyResource.objects.all()
    return render(request, 'accounts/financial_literacy.html', {'resources': resources})


def article_list_view(request):
    articles = Article.objects.all()
    return render(request, 'accounts/article_list.html', {'articles': articles})

def article_create_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Article.objects.create(title=title, content=content)
        return redirect('article_list')

    return render(request, 'accounts/article_create.html')

def video_list_view(request):
    videos = Video.objects.all()
    return render(request, 'accounts/video_list.html', {'videos': videos})

def video_create_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        url = request.POST['url']
        description = request.POST['description']
        Video.objects.create(title=title, url=url, description=description)
        return redirect('video_list')

    return render(request, 'accounts/video_create.html')

def quiz_list_view(request):
    quizzes = Quiz.objects.all()
    return render(request, 'accounts/quiz_list.html', {'quizzes': quizzes})

def quiz_create_view(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Quiz.objects.create(title=title, description=description)
        return redirect('quiz_list')

    return render(request, 'accounts/quiz_create.html')


