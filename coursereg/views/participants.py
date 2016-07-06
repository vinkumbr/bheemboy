from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from coursereg import models
import maillib

@login_required
def create(request):
    assert request.method == 'POST'
    course_id = request.POST['course_id']
    user_id = request.POST['user_id']
    reg_type = request.POST['reg_type']

    state = models.Participant.STATE_CREDIT
    if reg_type == 'audit':
        state = models.Participant.STATE_AUDIT

    if not course_id:
        messages.error(request, 'Select a course.')
    else:
        course = models.Course.objects.get(id=course_id)
        if models.Participant.objects.filter(user__id=user_id, course__id=course_id):
            messages.error(request, 'Already registered for %s.' % course)
        elif timezone.now().date() > course.last_reg_date:
            messages.error(request, 'Registration for %s is now closed.' % course)
        else:
            models.Participant.objects.create(
                user_id=user_id,
                course_id=course_id,
                participant_type=models.Participant.PARTICIPANT_STUDENT,
                state=state,
                grade=models.Participant.GRADE_NA,
                is_adviser_approved=request.POST['origin'] == 'adviser',
                is_instructor_approved=False
            )
            messages.success(request, 'Successfully applied for %s.' % course)

    return redirect(request.POST.get('next', reverse('coursereg:index')))

@login_required
def update(request, participant_id):
    participant = models.Participant.objects.get(id=participant_id)
    if request.POST['origin'] == 'instructor':
        if request.POST['action'] == 'approve':
            participant.is_instructor_approved = True
            participant.save()
        elif request.POST['action'] == 'reject':
            msg = 'Rejected application for %s.' % participant.course
            models.Notification.objects.create(user=participant.user,
                                               origin=models.Notification.ORIGIN_INSTRUCTOR,
                                               message=msg)
            participant.delete()
            maillib.send_email(request.user.email, participant.user.email, 'Coursereg notification', msg)
        elif request.POST['action'] == 'grade':
            participant.grade = int(request.POST['grade'])
            participant.save()
    elif request.POST['origin'] == 'adviser':
        if request.POST['action'] == 'state_change':
            participant.state = request.POST['state']
            participant.save()
            student = participant.user
            student.is_dcc_review_pending = True
            student.save()
            maillib.send_email(request.user.email, participant.user.email,
                               'Coursereg notification', 'Registration of %s changed to %s.' %
                               (participant.course, models.Participant.STATE_CHOICES[int(participant.state)][1]))
        elif request.POST['action'] == 'approve':
            participant.is_adviser_approved = True
            participant.save()
            student = participant.user
            student.is_dcc_review_pending = True
            student.save()
        elif request.POST['action'] == 'delete':
            msg = 'Rejected application for %s.' % participant.course
            models.Notification.objects.create(user=participant.user,
                                               origin=models.Notification.ORIGIN_ADVISER,
                                               message=msg)
            participant.delete()
            maillib.send_email(request.user.email, participant.user.email, 'Coursereg notification', msg)
    return redirect(request.POST.get('next', reverse('coursereg:index')))

@login_required
def approve_all(request):
    if request.POST['origin'] == 'adviser':
        student = models.User.objects.get(id=request.POST['student_id'])
        if models.Participant.objects.filter(user=student, is_adviser_approved=False):
            student.is_dcc_review_pending = True
            student.save()
        models.Participant.objects.filter(user=student).update(is_adviser_approved=True)
    elif request.POST['origin'] == 'instructor':
        course = models.Course.objects.get(id=request.POST['course_id'])
        models.Participant.objects.filter(course=course, is_adviser_approved=True).update(is_instructor_approved=True)
    return redirect(request.POST.get('next', reverse('coursereg:index')))

@login_required
def delete(request, participant_id):
    assert request.method == 'POST'
    participant = models.Participant.objects.get(id=participant_id)
    assert str(participant.user.id) == str(request.user.id)
    participant.delete()
    return redirect(request.GET.get('next', reverse('coursereg:index')))
