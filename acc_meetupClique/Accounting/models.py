from django.db import models

# Create your models here.

class Student (models.Model):
    StudID = models.CharField(max_length=11, primary_key=True)
    StudName = models.CharField(max_length=25)
    StudPhoneNo = models.CharField(max_length=12)
    StudPass = models.CharField(max_length=20)
    StudStatus = models.CharField(max_length=8)#Active/Inactive
    
class Staff (models.Model):
    StaffID = models.CharField(max_length=11, primary_key=True)
    StaffName = models.CharField(max_length=25)
    StaffPass = models.CharField(max_length=20)

class Event (models.Model):
    StaffID = models.ForeignKey(Staff, on_delete=models.CASCADE)
    EventID = models.CharField(max_length=5, primary_key=True)
    EventName = models.CharField(max_length=30)
    EventDetails = models.CharField(max_length=100)
    EventDate = models.DateField()
    EventTime = models.TimeField()
    EventStatus = models.CharField(max_length=10)#Upcoming/Completed/Canceled
    
class Attendance (models.Model):
    AttendanceID = models.CharField(max_length=7, primary_key=True)
    StudID = models.ForeignKey(Student, on_delete=models.CASCADE)
    EventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    AttStatus = models.CharField(max_length=10)#Attended/Emcee/Absent
    
class Feedback (models.Model):
    FeedbackID = models.CharField(max_length=5, primary_key=True)
    StudID = models.ForeignKey(Student, on_delete=models.CASCADE)
    EventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    EventRating = models.IntegerField()
    Comment = models.CharField(max_length=100)
    
class Suggestion (models.Model):
    SuggestionID = models.CharField(max_length=5, primary_key=True)
    StudID = models.ForeignKey(Student, on_delete=models.CASCADE)
    Details = models.CharField(max_length=1000)


