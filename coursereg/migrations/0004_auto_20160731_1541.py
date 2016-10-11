# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-31 15:41
from __future__ import unicode_literals

from django.db import migrations
import re
from datetime import timedelta
from django.utils import timezone

def separate_dept_abbreviation(apps, schema_editor):
    Department = apps.get_model("coursereg", "Department")
    for dept in Department.objects.all():
        combined_name = dept.name
        abbreviation = '-'
        dept_name_without_abbreviation = combined_name
        r = re.match(r'([A-Za-z0-9\s]+[^\s])\s*\((.+)\)\s*$', combined_name)
        if r:
            dept_name_without_abbreviation = r.group(1)
            abbreviation = r.group(2)
        dept.name = dept_name_without_abbreviation
        dept.abbreviation = abbreviation
        dept.is_active = True
        dept.save()

def migrate_term(Term, term, last_reg_date, last_drop_date):
    TERM_AUG = 0
    TERM_JAN = 1
    TERM_SUMMER = 2
    TERM_OTHER = 3

    TERM_CHOICES = (
        (TERM_AUG, "Aug-Dec"),
        (TERM_JAN, "Jan-Apr"),
        (TERM_SUMMER, "Summer"),
        (TERM_OTHER, "Other"),
    )

    name = TERM_CHOICES[term][1]
    year = str(last_reg_date.year)
    new_term = Term.objects.filter(
        name=name,
        year=year,
        last_reg_date=last_reg_date,
        last_drop_date=last_drop_date
    ).first()
    if not new_term:
        new_term = Term.objects.create(
            name=name,
            year=year,
            start_reg_date=last_reg_date - timedelta(days=90),
            last_reg_date=last_reg_date,
            last_adviser_approval_date=last_reg_date,
            last_instructor_approval_date=last_reg_date,
            last_cancellation_date=last_reg_date + timedelta(days=5),
            last_conversion_date=last_drop_date,
            last_drop_date=last_drop_date,
            last_grade_date=last_reg_date + timedelta(days=150),
            is_active=True
        )
    return new_term

def migrate_course_table(apps, schema_editor):
    Course = apps.get_model("coursereg", "Course")
    Term = apps.get_model("coursereg", "Term")
    for course in Course.objects.all():
        course.new_term = migrate_term(Term, course.term, course.last_reg_date, course.last_drop_date)
        course.new_credits = '%s:0' % course.credits
        course.should_count_towards_cgpa = True
        if course.credits == 0:
            course.should_count_towards_cgpa = False
        course.save()

def migrate_grade(Participant, Grade, grade):
    GRADE_NA = 0
    GRADE_S = 1
    GRADE_A = 2
    GRADE_B = 3
    GRADE_C = 4
    GRADE_D = 5
    GRADE_F = 6

    GRADE_CHOICES = (
        (GRADE_NA, 'Not graded'),
        (GRADE_S, 'S grade'),
        (GRADE_A, 'A grade'),
        (GRADE_B, 'B grade'),
        (GRADE_C, 'C grade'),
        (GRADE_D, 'D grade'),
        (GRADE_F, 'F grade'),
    )

    if grade == GRADE_NA:
        return None

    GRADE_POINTS = [0, 8.0, 7.0, 6.0, 5.0, 4.0, 0.0]
    new_grade_name = GRADE_CHOICES[grade][1]
    ng = Grade.objects.filter(name=new_grade_name).first()
    if not ng:
        ng = Grade.objects.create(
            name=new_grade_name,
            should_count_towards_cgpa=True,
            points=GRADE_POINTS[grade],
            is_active=True
        )
    return ng

def migrate_participant_state(Participant, RegistrationType, participant):
    STATE_CREDIT = 1
    STATE_AUDIT = 2

    if participant.state == STATE_AUDIT:
        reg_type = RegistrationType.objects.filter(name='Audit').first()
        if not reg_type:
            reg_type = RegistrationType.objects.create(
                name='Audit',
                should_count_towards_cgpa=False,
                is_active=True
            )
        return reg_type
    else:
        reg_type = RegistrationType.objects.filter(name='Credit').first()
        if not reg_type:
            reg_type = RegistrationType.objects.create(
                name='Credit',
                should_count_towards_cgpa=True,
                is_active=True
            )
        return reg_type

def migrate_participant_table(apps, schema_editor):
    STATE_CREDIT = 1
    STATE_AUDIT = 2
    STATE_DROP = 3

    Participant = apps.get_model("coursereg", "Participant")
    Grade = apps.get_model("coursereg", "Grade")
    RegistrationType = apps.get_model("coursereg", "RegistrationType")
    for participant in Participant.objects.all():
        participant.registration_type = migrate_participant_state(Participant, RegistrationType, participant)
        participant.is_drop = (participant.state == STATE_DROP)
        participant.new_grade = migrate_grade(Participant, Grade, participant.grade)
        participant.should_count_towards_cgpa = participant.course.should_count_towards_cgpa
        participant.created_at = timezone.now()
        participant.updated_at = timezone.now()
        participant.save()


class Migration(migrations.Migration):

    dependencies = [
        ('coursereg', '0003_auto_20160731_1539'),
    ]

    operations = [
        migrations.RunPython(separate_dept_abbreviation),
        migrations.RunPython(migrate_course_table),
        migrations.RunPython(migrate_participant_table)
    ]
