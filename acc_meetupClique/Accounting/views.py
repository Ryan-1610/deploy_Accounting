from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages  # Ensure you import messages
from django.urls import reverse
from Accounting.models import Student, Event, Attendance, Feedback, Suggestion
from django.shortcuts import render, redirect
from django.db.models import Max
from django.contrib.auth import update_session_auth_hash

@login_required
def Home(request):
    return render (request,"Home.html")

#--------------------------------------Log In Page---------------------------------------
def Accounting_Society(request):
    if request.method == 'POST':
        ID = request.POST['ID']
        password = request.POST['password']
        find = Student.objects.filter(StudID=ID).values()
        if find.exists():
            if find[0]['StudPass'] == password:
                dict = {"user": find[0]['StudID']}
                request.session['user_id'] = find[0]['StudID'] 
                return redirect('Home')
            else:
                dict = {"message":" WRONG PASSWORD !! "}
                return render(request, 'Main.html', dict)
        else:
            dict = {"message": " WRONG USERNAME "}
            return render(request, 'Main.html', dict)

    return render(request, 'Main.html')

#--------------------------------------Log Out Page---------------------------------------
def Log_out (request):
    return HttpResponseRedirect(reverse("Accounting_Society"))

#----------------------------------------Attendance Page-----------------------------------------
@login_required
def attendance(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "User not found. Please log in again.")
        return redirect('Accounting_Society')
    
    try:
        current_user = Student.objects.get(StudID=user_id)
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('Accounting_Society')
    
    all_attendance = Attendance.objects.filter(StudID=current_user).select_related('EventID', 'StudID')
    
    dict = {
        'all_attendance': all_attendance if all_attendance.exists() else None,
        'data': all_attendance.exists(),  # 0 or 1 based on existence
        'current_user': current_user
    }
    return render(request, "Attendance.html", dict)

def returnhome(request):
    return HttpResponseRedirect(reverse("Home"))



#---------------------------------Attendance Status Update------------------------------------------- 
@login_required
def update_attendance_status(request):
    user_id = request.session.get('user_id')  #Get the logged-in user's ID from the session
    event_id = request.GET.get('event_id')  #Get event ID from the query parameter
    
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        attendance_status = request.POST.get('attendance_status')

        #Find and update attendance record for the current user
        try:
            attendance = Attendance.objects.get(EventID=event_id, StudID=user_id)
            attendance.AttStatus = attendance_status
            attendance.save()
        except Attendance.DoesNotExist:
            return HttpResponse("Attendance record not found", status=404)

        return HttpResponseRedirect (reverse("attendance"))  #Redirect to the attendance page after update

    #Fetch event details and current attendance status for pre-selection in the form
    try:
        current_attendance = Attendance.objects.get(EventID=event_id, StudID=user_id)
        current_status = current_attendance.AttStatus
    except Attendance.DoesNotExist:
        return HttpResponse("Attendance record not found", status=404)

    return render(request, 'update_attendance.html', {
        'current_status': current_status,
        'event_id': event_id  #Pass event_id to the template for form submission
    })

#----------------------------------Delete attendance ---------------------------------------
def delete_attendance(request, a_id):
    data = Attendance.objects.get(AttendanceID=a_id)
    data.delete()
    return HttpResponseRedirect(reverse("attendance"))

def delete_event(request, z_id):
    try:
        # Ensure you're handling cases where EventID might not exist
        z_id = "" #delete for event there is no id
        data = Attendance.objects.filter(AttendanceID=z_id)
        data.delete()
        messages.success(request, "Event attendance records deleted successfully.")
    except Attendance.DoesNotExist:
        messages.error(request, "Event attendance record not found.")
    return HttpResponseRedirect(reverse("attendance"))


#----------------------------------------Book Event-----------------------------------------
@login_required
def EventPage(request):
    all_feedback = Feedback.objects.all()  # Fetch feedback with related student details
    if request.method == 'GET' and 'event_id' in request.GET:
        event_id = request.GET['event_id']
        selected_event = Event.objects.get(EventID=event_id)

    # Pass feedback to the template
    context = {
        'all_feedback': all_feedback
    }
    return render(request, "Event.html", context)

@login_required
def Event_Table(request):
    # Get the current user from session
    user_id = request.session.get('user_id')
    current_user = Student.objects.get(StudID=user_id)

    # Fetch all available events and the user's registered events
    all_events = Event.objects.filter(EventStatus="Upcoming")
    user_attendance = Attendance.objects.filter(StudID=current_user)
    event_registered_ids = user_attendance.values_list('EventID', flat=True)

    # Handle event booking
    if request.method == 'GET' and 'event_id' in request.GET:
        event_id = request.GET['event_id']
        selected_event = Event.objects.get(EventID=event_id)

        # Check if the user is already registered for this event
        if selected_event.EventID not in event_registered_ids:
            # Generate new attendance ID
            new_id = generate_new_attendance_id()

            # Create new attendance record
            Attendance.objects.create(
                AttendanceID=new_id,
                StudID=current_user,
                EventID=selected_event,
                AttStatus='Attend',
            )
            messages.success(request, f"You have successfully joined the event: {selected_event.EventName}")
        else:
            messages.warning(request, f"You are already registered for the event: {selected_event.EventName}")

        return redirect('Book_Event')

    context = {
        'all_events': all_events,
        'event_registered_ids': event_registered_ids,
    }

    return render(request, 'Book_Event.html', context)



#---------------------------------Join Event------------------------------------------- 
@login_required
def update_join_event(request, event_id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "User not found. Please log in again.")
        return redirect('Accounting_Society')

    try:
        current_user = Student.objects.get(StudID=user_id)
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('Accounting_Society')

    all_events = Event.objects.exclude(EventStatus='Completed')
    event_registered_ids = Attendance.objects.filter(StudID=current_user).values_list('EventID', flat=True)
    
    # Handle event booking
    if request.method == 'GET' and 'event_id' in request.GET:
        event_id = request.GET['event_id']
        
        try:
            selected_event = Event.objects.get(EventID=event_id)
        except Event.DoesNotExist:
            messages.error(request, "Event not found.")
            return redirect('Book_Event')
        
        already_joined = Attendance.objects.filter(EventID=selected_event, StudID=current_user).exists()

        if not already_joined:
            while Attendance.objects.filter(AttendanceID=new_id).exists():
                new_id = generate_new_attendance_id()  # Use the function to generate a new ID
            
            Attendance.objects.create(
                AttendanceID=new_id,
                StudID=current_user,
                EventID=selected_event,
                AttStatus='Attend',
            )
            messages.success(request, f"You have successfully joined the event: {selected_event.EventName}")
        else:
            messages.warning(request, f"You are already registered for the event: {selected_event.EventName}")
        
        return redirect('Book_Event')
    
    context = {
        'all_events': all_events,
        'event_registered_ids': event_registered_ids,
    }
    
    return render(request, 'Book_Event.html', context)

def generate_new_attendance_id():
    latest_attendance = Attendance.objects.order_by('-AttendanceID').first()

    if latest_attendance:
        latest_id = latest_attendance.AttendanceID
        latest_num = int(latest_id.replace('ATT', '')) + 1
        new_id = f"ATT{latest_num:04d}"  # Ensure the new ID is incremented and formatted correctly
    else:
        new_id = "ATT1001"  # Default starting ID if none exist

    return new_id


#---------------------------------Feedback------------------------------------------- 
@login_required
def update_attendance_status(request):
    user_id = request.session.get('user_id')  #Get the logged-in user's ID from the session
    event_id = request.GET.get('event_id')  #Get event ID from the query parameter
    
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        attendance_status = request.POST.get('attendance_status')

        #Find and update attendance record for the current user
        try:
            attendance = Attendance.objects.get(EventID=event_id, StudID=user_id)
            attendance.AttStatus = attendance_status
            attendance.save()
        except Attendance.DoesNotExist:
            return HttpResponse("Attendance record not found", status=404)

        return HttpResponseRedirect (reverse("attendance"))  #Redirect to the attendance page after update

    #Fetch event details and current attendance status for pre-selection in the form
    try:
        current_attendance = Attendance.objects.get(EventID=event_id, StudID=user_id)
        current_status = current_attendance.AttStatus
    except Attendance.DoesNotExist:
        return HttpResponse("Attendance record not found", status=404)

    return render(request, 'update_attendance.html', {
        'current_status': current_status,
        'event_id': event_id  #Pass event_id to the template for form submission
    })


@login_required
def feedback_update(request):
    StudID_id = request.session.get('user_id')
    EventID_id = request.GET.get('event_id')
    
    event = get_object_or_404(Event, EventID=EventID_id)

    try:
        feedback = Feedback.objects.get(StudID=StudID_id, EventID=EventID_id)
    except Feedback.DoesNotExist:
        # Generate new FeedbackID
        last_feedback = Feedback.objects.order_by('-FeedbackID').first()
        if last_feedback:
            new_feedback_id = f"FB{int(last_feedback.FeedbackID[2:]) + 1:03d}"
        else:
            new_feedback_id = "FB001"  # For the first feedback in the system

        # Create new feedback
        feedback = Feedback.objects.create(
            FeedbackID=new_feedback_id,
            StudID_id=StudID_id,
            EventID=event,
            EventRating=0,
            Comment="",
        )

    current_rating = feedback.EventRating
    current_comment = feedback.Comment
    event_name = event.EventName

    if request.method == 'POST':
        updated_rating = request.POST.get('rating')
        updated_comment = request.POST.get('comment')

        if updated_rating.isdigit() and 1 <= int(updated_rating) <= 10:
            feedback.EventRating = int(updated_rating)
        else:
            return HttpResponse("Invalid rating value. Must be between 1 and 10.", status=400)

        if len(updated_comment.split()) <= 100:
            feedback.Comment = updated_comment
        else:
            return HttpResponse("Comment exceeds 100 words.", status=400)

        feedback.save()

        messages.success(request, "Your feedback has been submitted or updated.")
        return HttpResponseRedirect(reverse("attendance") + f"?event_id={EventID_id}&feedback_id={feedback.FeedbackID}")

    return render(request, "feedback.html", {
        'current_rating': current_rating,
        'current_comment': current_comment,
        'event_name': event_name,
        'event_id': EventID_id,
        'feedback_id': feedback.FeedbackID,
        'rating_range': range(1, 11),
    })


#-------------------------------------------Profile------------------------------------------- 
@login_required
def profile(request):
    user_id = request.session.get('user_id')
    user = Student.objects.get(StudID=user_id)

    if request.method == 'POST':
        # Update name and phone number
        user.StudName = request.POST.get('name')
        user.StudPhoneNo = request.POST.get('phone')
    return render(request, 'profile.html', {'user': user})

@login_required
def profile_view(request):
    user_id = request.session.get('user_id')
    user = Student.objects.get(StudID=user_id)

    if request.method == 'POST':
        # Update name and phone number
        user.StudName = request.POST.get('name')
        user.StudPhoneNo = request.POST.get('phone')

        # Check and update password
        old_password = request.POST.get('old_password')
        if user.StudPass == old_password:
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.StudPass = new_password
                messages.success(request, 'Profile updated successfully.')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'Old password is incorrect.')

        user.save()
        return HttpResponseRedirect(reverse("User_profile"))
    return render(request, 'Edit_Profile.html', {'user': user})

@login_required
def backtohomeprofile(request):
    return HttpResponseRedirect(reverse("Home"))

@login_required
def backActivities(request):
    return HttpResponseRedirect(reverse("User_profile"))

@login_required
def backEditProfile(request):
    return HttpResponseRedirect(reverse("User_profile"))

@login_required
def delete_User(request, s_id):
    try:
        user = Student.objects.get(StudID=s_id)
        Feedback.objects.filter(StudID=user).delete()
        Attendance.objects.filter(StudID=user).delete()
        Suggestion.objects.filter(StudID=user).delete()
        user.delete()
        messages.success(request, "Your account has been deleted successfully.")
        return HttpResponseRedirect(reverse("Accounting_Society")) 
    except Student.DoesNotExist:
        messages.error(request, "User not found.")
        return HttpResponseRedirect(reverse("Accounting_Society"))


#-------------------------------------------Suggestion Public--------------------------------------------- 
@login_required
def suggestion_list(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "User not found. Please log in again.")
        return redirect('Accounting_Society')

    try:
        current_user = Student.objects.get(StudID=user_id)
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('Accounting_Society')
    
    all_suggestion = Suggestion.objects.all()

    dict = {
        'all_suggestion': all_suggestion if all_suggestion.exists() else None,
        'data': all_suggestion.exists(),  # 0 or 1 based on existence
    }
    return render(request,'suggestions.html', dict)


#--------------------------------Suggestion in Profile only for register student--------------------------------------- 
@login_required
def suggestion_personal(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "User not found. Please log in again.")
        return redirect('Accounting_Society')

    try:
        current_user = Student.objects.get(StudID=user_id)
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('Accounting_Society')
    
    all_suggestion = Suggestion.objects.filter(StudID=current_user)

    dict = {
        'all_suggestion': all_suggestion if all_suggestion.exists() else None,
        'data': all_suggestion.exists(),  # 0 or 1 based on existence
        'current_user': current_user
    }
    return render(request,'suggestion_profile.html', dict)


def delete_suggestion(request, suggestion_id):
    data = Suggestion.objects.get(SuggestionID=suggestion_id)
    data.delete()
    return HttpResponseRedirect(reverse("suggestion_personal"))

@login_required
def update_suggestion_comment(request):
    StudID_id = request.session.get('user_id')  
    SuggestionID_id = request.GET.get('suggestion_id')
    
    try:
        suggestion = Suggestion.objects.get(StudID=StudID_id)
    except Suggestion.DoesNotExist:
        messages.error(request, "Suggestion not found.")
        return redirect('suggestion_personal')
    current_suggestion = suggestion.Details  
    
    if request.method == 'POST':
        updated_suggestion = request.POST.get('suggestion')
        suggestion.Details = updated_suggestion
        suggestion.save()
        messages.success(request, "You have updated your suggestion.")
        return HttpResponseRedirect(reverse("suggestion_personal") + f"?suggestion_id={SuggestionID_id}")
    return render(request, "edit_suggestions.html", {
        'current_suggestion': current_suggestion,
        'suggestion_id': suggestion.SuggestionID,  # Use the suggestion instance
    })


@login_required
def add_suggestion(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "User not found. Please log in again.")
        return redirect('Accounting_Society')

    try:
        current_user = Student.objects.get(StudID=user_id)
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
        return redirect('Accounting_Society')

    if request.method == 'POST':
        details = request.POST.get('details')  # Get the suggestion details from the form
        
        if details:
            # Generate new SuggestionID
            latest_suggestion = Suggestion.objects.order_by('-SuggestionID').first()  # Get the last suggestion
            
            # If there are no suggestions yet, start with SG001
            if latest_suggestion:
                latest_id = latest_suggestion.SuggestionID
                new_id_num = int(latest_id.replace('SG', '')) + 1
                new_suggestion_id = f'SG{new_id_num:03d}'  # Format as SG00X
            else:
                new_suggestion_id = 'SG101'  # Start with the first ID

            # Create and save the new suggestion
            new_suggestion = Suggestion(
                SuggestionID=new_suggestion_id,
                StudID=current_user,
                Details=details
            )
            new_suggestion.save()  # Save the new suggestion to the database
            
            messages.success(request, "Your suggestion has been submitted successfully.")
            return redirect('suggestion_personal')  # Redirect to a success page or wherever you want
        else:
            messages.error(request, "Please enter your suggestion.")

    return render(request, 'add_suggestion.html')
