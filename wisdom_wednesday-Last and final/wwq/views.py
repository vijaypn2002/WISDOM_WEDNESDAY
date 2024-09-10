from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Quote, DepartmentPage, QuizQuestion, QuizResult, UserDetail
from .forms import UserDetailForm, BlogForm, QuizQuestionForm
from django.http import JsonResponse
import json
import re
from datetime import datetime

def home(request):
    try:
        latest_quote = Quote.objects.latest('id')
    except Quote.DoesNotExist:
        latest_quote = None  # Or you can set a default value here

    return render(request, 'wwq/home.html', {'latest_quote': latest_quote})

def split_into_paragraphs(text, sentences_per_paragraph=5):
    # Split the text into sentences using regex to match sentence-ending punctuation or line breaks
    sentences = re.split(r'(?<=[.!?])\s+|\n', text)
    # Group sentences into paragraphs of specified number of sentences each
    paragraphs = [' '.join(sentences[i:i + sentences_per_paragraph]) for i in range(0, len(sentences), sentences_per_paragraph)]
    return paragraphs

def blog(request):
    try:
        latest_blog = Blog.objects.latest('published_date')
    except Blog.DoesNotExist:
        latest_blog = None

    volumes = Blog.objects.values('volume').distinct().order_by('volume')

    if latest_blog:
        historical_blogs = Blog.objects.exclude(id=latest_blog.id).order_by('volume', 'part')
        # Split the latest blog content and additional content into paragraphs of 5 sentences each.
        latest_blog.paragraphs = split_into_paragraphs(latest_blog.content)
        if latest_blog.additional_content:
            latest_blog.additional_paragraphs = split_into_paragraphs(latest_blog.additional_content)
        else:
            latest_blog.additional_paragraphs = []
    else:
        historical_blogs = Blog.objects.all().order_by('volume', 'part')

    return render(request, 'wwq/blog.html', {
        'latest_blog': latest_blog,
        'volumes': volumes,
        'historical_blogs': historical_blogs
    })

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'wwq/blog_detail.html', {'blog': blog})

def department_page(request, dept_name):
    page = DepartmentPage.objects.get(name=dept_name)
    return render(request, 'wwq/department_page.html', {'page': page})

def user_details(request):
    if request.method == 'POST':
        form = UserDetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = UserDetailForm()
    return render(request, 'wwq/details.html', {'form': form})

def it_policies(request):
    return render(request, 'wwq/it_policies.html')

def hr_policies(request):
    return render(request, 'wwq/hr_policies.html')

def leave_application_policy(request):
    return render(request, 'wwq/leave_application_policy.html')

def resignation_policy(request):
    return render(request, 'wwq/resignation_policy.html')

def uae_policy(request):
    return render(request, 'wwq/uae_policy.html')

def dress_code(request):
    return render(request, 'wwq/dress_code.html')

def courses(request):
    return render(request, 'wwq/courses.html')

def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = BlogForm()
    return render(request, 'wwq/add_blog.html', {'form': form})

def quiz(request):
    user = UserDetail.objects.latest('submission_date')
    if request.method == 'POST':
        score = int(request.POST.get('score', 0))
        print('Score received:', score)  # Debug statement
        # Explicitly set date_taken to ensure it's recorded
        QuizResult.objects.create(user=user, score=score, date_taken=datetime.now())
        return redirect('quiz_result', score=score)
    else:
        questions = QuizQuestion.objects.order_by('?')[:15]  # Updated to 15 questions
        questions_list = list(questions.values('id', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option'))
        questions_json = json.dumps(questions_list)
        if not questions:
            return render(request, 'wwq/quiz.html', {'error': 'No quiz questions available.'})
        return render(request, 'wwq/quiz.html', {'questions': questions_json})

def quiz_result(request, score):
    user = UserDetail.objects.latest('submission_date')
    percentage_score = (score / 15) * 100  # Adjusted to 15 questions
    show_confetti = score > 10
    print('Show confetti:', show_confetti)  # Debug statement
    return render(request, 'wwq/quiz_result.html', {
        'score': score,
        'percentage_score': percentage_score,
        'user': user,
        'show_confetti': show_confetti
    })

def it_asset_policy(request):
    return render(request, 'wwq/it_asset_policy.html')

def lakshya_commerce_lms(request):
    return render(request, 'wwq/lakshya_commerce_lms.html')

def security_policies(request):
    return render(request, 'wwq/security_policies.html')
