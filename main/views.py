from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Course, Enrollment, EventRegistration

# Home Page
def home(request):
    courses = Course.objects.all()  # Dynamically fetch courses from the database
    return render(request, 'home.html', {'courses': courses})

# User Registration
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Check if username or email is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Oops! Username already taken. Try another.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered. One account is enough!")
        elif len(password) < 6:
            messages.error(request, "Password too weak! Try something stronger.")
        else:
            # Create new user and save to the database
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account created successfully! Now go and log in.")
            return redirect('login')

    return render(request, 'register.html')

# User Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'login.html')

# User Logout
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

# Dashboard
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Courses Page (Login Required)
@login_required(login_url="/#authModal")
def courses(request):
    courses = Course.objects.all()  # Dynamically fetch courses from the database
    return render(request, 'courses.html', {'courses': courses})

# Events Page (Login Required)
@login_required(login_url="/#authModal")
def events(request):
    events = EventRegistration.objects.all()  # Get all event registrations (if needed)
    return render(request, 'events.html', {'events': events})

# Contact Page (Login Required)
@login_required(login_url="/#authModal")
def contact(request):
    return render(request, 'contact.html')

# Course Enrollment
@login_required
def enroll(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")

        if not course_id:
            messages.error(request, "Course ID is missing!")
            return redirect("courses")

        try:
            course = Course.objects.get(id=course_id)  # Fetch course from DB
        except Course.DoesNotExist:
            messages.error(request, "No course found with the given ID!")
            return redirect("courses")

        if Enrollment.objects.filter(user=request.user, course=course).exists():
            messages.warning(request, "You are already enrolled in this course!")
        else:
            Enrollment.objects.create(user=request.user, course=course)
            messages.success(request, f"You have successfully enrolled in {course.name}!")

        return redirect("dashboard")

    return redirect("home")  # If accessed via GET request, redirect to home

# Edit Profile
@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username", user.username)
        user.email = request.POST.get("email", user.email)
        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("dashboard")

    return render(request, "edit_profile.html")

from .models import Event, EventRegistration
from django.shortcuts import render, redirect
from django.contrib import messages

def event_register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        event_id = request.POST['event']  # Get the event ID from the form

        if not name or not email or not event_id:
            messages.error(request, "All fields are required!")
            return redirect('events')

        # Fetch the event object using the event_id
        try:
            event = Event.objects.get(id=event_id)  # Assuming event_id is passed and corresponds to an existing event
        except Event.DoesNotExist:
            messages.error(request, "The selected event does not exist.")
            return redirect('events')

        # Save the event registration to the database
        EventRegistration.objects.create(name=name, email=email, event=event)
        messages.success(request, "You have successfully registered for the event!")
        return redirect('events')  # Redirect back to events page

    return render(request, 'event_register.html')


# News Page (Unchanged)
def news(request):
    return render(request, 'news.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt  # Only use csrf_exempt if needed for testing

# If you're using a model (see below), import it:
# from .models import NewsletterSubscriber

@csrf_exempt  # Use this only if you don’t have {% csrf_token %} in your form
def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            # Uncomment this part if using a model to save emails:
            # NewsletterSubscriber.objects.create(email=email)

            print(f"Newsletter subscription from: {email}")
            messages.success(request, "Thanks for subscribing!")
        else:
            messages.error(request, "Please enter a valid email.")
        return redirect('home')
    else:
        return redirect('home')


from django.shortcuts import render

def ai_trends(request):
    return render(request, 'blog/ai-trends-2025.html')

def fullstack_blog(request):
    return render(request, 'blog/fullstack-importance.html')

def cybersecurity_blog(request):
    return render(request, 'blog/cybersecurity-essentials.html')

from django.shortcuts import render

def blog_home(request):
    return render(request, 'blog_home.html')  # Replace with your actual template

from django.shortcuts import render

course_info = {
    'artificial-intelligence': {
        'title': 'Artificial Intelligence',
        'description': 'This course introduces you to AI concepts, techniques, and real-world applications.',
        'topics': ['Machine Learning', 'Neural Networks', 'NLP', 'Computer Vision'],
        'slug': 'artificial-intelligence',
        'image': 'images/ai.png'
    },
    'python-programming': {
        'title': 'Python Programming',
        'description': 'Learn Python from basics to advanced with hands-on projects and practical applications.',
        'topics': ['Syntax & Semantics', 'OOP in Python', 'Web Development', 'Data Science'],
        'slug': 'python-programming',
        'image': 'images/python.png'
    },
    'cyber-security': {
        'title': 'Cyber Security',
        'description': 'Understand cybersecurity fundamentals and how to protect systems and data.',
        'topics': ['Network Security', 'Ethical Hacking', 'Cryptography', 'Incident Response'],
        'slug': 'cyber-security',
        'image': 'images/cs.png'
    },
    'web-development': {
        'title': 'Web Development',
        'description': 'Master front-end and back-end development to build dynamic web applications.',
        'topics': ['HTML, CSS, JS', 'React & Django', 'APIs & Databases', 'Deployment'],
        'slug': 'web-development',
        'image': 'images/web.png'
    },
}


def course_detail(request, slug):
    course = course_info.get(slug)
    if not course:
        return render(request, '404.html', status=404)
    return render(request, 'course_detail.html', {'course': course})


def enroll_course(request, slug):
    course = course_info.get(slug)
    if not course:
        return render(request, '404.html', status=404)
    return render(request, 'enroll.html', {'course': course})

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            message = """Hi there,

Thank you for subscribing to our newsletter!

We're excited to have you on board. You’ll now receive the latest updates, course announcements, and exclusive content directly to your inbox.

If you ever wish to unsubscribe, you can do so at any time from the link at the bottom of our emails.

Stay tuned!

Best regards,  
Ajit Rawat
"""
            send_mail(
                subject='Newsletter Subscription',
                message=message,
                from_email='ajit74043@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, "Subscription successful! Check your inbox.")
        except Exception as e:
            messages.error(request, f"Failed to send email: {str(e)}")
    return redirect('home')


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import openai
import json

openai.api_key = settings.OPENAI_API_KEY

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for student academic queries."},
                {"role": "user", "content": user_message}
            ]
        )

        answer = response['choices'][0]['message']['content'].strip()
        return JsonResponse({'reply': answer})

    return JsonResponse({'error': 'Invalid request method'}, status=405)

from django.shortcuts import render

def chatbot_view(request):
    return render(request, 'chatbot.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_msg = data.get('message', '').lower()

        # Extensive keyword-response mapping
        if any(word in user_msg for word in ['hello', 'hi', 'hey']):
            response = "Hello! Welcome to NeuroVertex Academy. How can I assist you today?"
        elif 'python' in user_msg:
            response = (
                "Our Python course covers basics, intermediate, and advanced topics, "
                "including data analysis, web development with Django, and automation."
            )
        elif 'ai' in user_msg or 'artificial intelligence' in user_msg:
            response = (
                "The AI course includes machine learning, deep learning, "
                "natural language processing, and real-world AI projects."
            )
        elif 'machine learning' in user_msg or 'ml' in user_msg:
            response = (
                "Our Machine Learning course focuses on supervised and unsupervised learning, "
                "algorithms like regression, classification, clustering, and model evaluation."
            )
        elif 'data science' in user_msg:
            response = (
                "The Data Science course includes data wrangling, visualization, "
                "statistics, and working with Python libraries like pandas and matplotlib."
            )
        elif 'price' in user_msg or 'cost' in user_msg or 'fee' in user_msg:
            response = (
                "Course prices start at $199. We also offer discounts for early sign-ups and bundles."
            )
        elif 'duration' in user_msg or 'length' in user_msg or 'how long' in user_msg:
            response = (
                "Most of our courses run for 8 to 12 weeks with flexible timing options."
            )
        elif 'certificate' in user_msg:
            response = (
                "We provide a certificate of completion after successfully finishing each course."
            )
        elif 'enroll' in user_msg or 'register' in user_msg:
            response = (
                "You can enroll through our website's Courses page or contact support for assistance."
            )
        elif 'support' in user_msg or 'help' in user_msg:
            response = (
                "For support, please contact us via the Contact page or email support@neurovertex.com."
            )
        elif 'schedule' in user_msg or 'timing' in user_msg:
            response = (
                "Our courses offer both weekday and weekend batches. Check the Courses page for details."
            )
        elif 'projects' in user_msg:
            response = (
                "Many of our courses include hands-on projects to build your portfolio."
            )
        elif 'refund' in user_msg:
            response = (
                "Refund policies are available on our Terms & Conditions page. Generally, refunds "
                "are available within the first week of enrollment."
            )
        elif 'thanks' in user_msg or 'thank you' in user_msg:
            response = "You're welcome! Feel free to ask if you have more questions."
        else:
            response = (
                "Sorry, I couldn't understand that. You can ask me about courses, pricing, duration, "
                "certificates, enrollment, or support."
            )

        return JsonResponse({"response": response})
    return JsonResponse({"response": "Invalid request"}, status=400)
