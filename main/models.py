from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Course Name")
    price = models.IntegerField(default=6000, verbose_name="Course Price")  # Ensure this is an integer
    short_description = models.TextField(verbose_name="Short Description")
    detailed_description = models.TextField(verbose_name="Detailed Description")
    image = models.ImageField(upload_to='courses/', default='courses/default.jpg', verbose_name="Course Image")  # Default image path

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Event Title")
    description = models.TextField(verbose_name="Event Description")
    date = models.DateField(verbose_name="Event Date")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"


class Inquiry(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    message = models.TextField(verbose_name="Message")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Inquiry"
        verbose_name_plural = "Inquiries"


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments", verbose_name="User")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments", verbose_name="Enrolled Course")
    enrolled_on = models.DateTimeField(auto_now_add=True, verbose_name="Enrollment Date")

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.name}"

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"


class EventRegistration(models.Model):
    name = models.CharField(max_length=255, verbose_name="Registrant Name")
    email = models.EmailField(verbose_name="Registrant Email")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations", verbose_name="Registered Event")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="Registration Date")

    def __str__(self):
        return f"{self.name} registered for {self.event.title}"

    class Meta:
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"

from django.db import models

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
