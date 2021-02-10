from tasks.models import Task
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail

def run():
    """Sends email to users who have task's deadline is tomorrow and sends email when deadline is now"""
    the_day_before_tasks = Task.objects.all().filter(deadline_date__date=datetime.today() + relativedelta(days=1)) # filtering tasks with deadline date = tomorrow (today + 1 day using relativedelta) 
    identical_time = datetime.strptime(str(datetime.today()),"%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S") # getting datetime of today and changing its value format to 2010-11-4 10:30:00 instead of 2010-11-4 10:30:00.15181
    deadline_day_tasks = Task.objects.all().filter(deadline_date__date=identical_time) # filtering tasks with deadline of today
    if the_day_before_tasks: # if there're any filtered tasks have deadline of tomorrow
        for task1 in the_day_before_tasks:
            """Sending email to each user of these tasks"""
            completed_date = datetime.strptime(str(task1.deadline_date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %I:%M:%S %p') # changing deadline format from 2010-11-4 10:30:00 to 2010-11-4 10:30:00 AM/PM
            if not task1.completed: # if the user hasn't completed the task yet:
                send_mail(subject=f"'{task1.title}' Task",
                          message=f"Dear {task1.user.username},\n[+] The deadline of your task is tomorrow at '{completed_date}'",
                          from_email="todotasks4000@gmail.com", recipient_list=[task1.user.email], fail_silently=False)
    if deadline_day_tasks: # if there're any filtered tasks that their deadline is today
        for task2 in deadline_day_tasks:
            """Sending email to each user of these tasks"""
            well_formatted_date = datetime.strptime(str(task2.deadline_date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %I:%M:%S %p')
            if not task2.completed: # if the user hasn't completed the task yet:
                send_mail(subject=f"'{task2.title}' Task",
                          message=f"Dear {task2.user.username},\n[+] You missed completing your task '{task2.title}'"
                                  f" whose deadline is '{well_formatted_date}'",
                          from_email="todotasks4000@gmail.com", recipient_list=[task2.user.email], fail_silently=False)