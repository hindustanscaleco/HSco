from email.mime.text import MIMEText

from django.core.mail import send_mail, EmailMessage

from Hsco import settings
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Q
from django.shortcuts import render, redirect

from lead_management.email_content import user
from .forms import Career_moduleForm, EducationForm, WorkExpForm
from .models import Career_module, EducationalDetails, WorkExperience, Position
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json

@login_required(login_url='/')
def career_module_list(request):
    career_list = Career_module.objects.all().order_by('-id')
    paginator = Paginator(career_list, 100)  # Show 25 contacts per page
    page = request.GET.get('page')
    career_list = paginator.get_page(page)
    context = {
        'career_list': career_list,
    }
    try:
        called_nointerview = Career_module.objects.filter(current_stage='Called for Interview').count()
        context2 = {
            'called_nointerview': called_nointerview,
        }
        context.update(context2)
    except:
        pass
    try:
        applied_nocall = Career_module.objects.filter(current_stage='Applied but Not called for Interview').count()
        context5 = {
            'applied_nocall': applied_nocall,
        }
        context.update(context5)
    except:
        pass
    try:
        interview_progress = Career_module.objects.filter(current_stage='Selection in Progress').count()
        context6 = {
            'interview_progress': interview_progress,
        }
        context.update(context6)
    except:
        pass
    try:
        interview_notselected =Career_module.objects.filter(current_stage='Selected').count()
        context7 = {
            'interview_notselected': interview_notselected,
        }
        context.update(context7)
    except:
        pass
    try:
        interview_rejected = Career_module.objects.filter(current_stage='Rejected').count()
        context8 = {
            'interview_rejected': interview_rejected,
        }
        context.update(context8)
    except:
        pass
    try:
        interview_preserved = Career_module.objects.filter(current_stage='Future Reference').count()
        context9 = {
            'interview_preserved': interview_preserved,
        }
        context.update(context9)
    except:
        pass
    try:
        did_not_joined = Career_module.objects.filter(current_stage='Did not Joined').count()
        context10 = {
            'did_not_joined': did_not_joined,
        }
        context.update(context10)
    except:
        pass
    if request.method == 'POST':



        if 'sort_submit' in request.POST:
            YEAR = request.POST.get('YEAR')
            MONTH = request.POST.get('MONTH')

            career_list = Career_module.objects.filter(entry_timedate__month=MONTH, entry_timedate__year=YEAR).order_by('-id')

            career_list_count = Career_module.objects.filter(entry_timedate__month=MONTH, entry_timedate__year=YEAR).count()
            paginator = Paginator(career_list, 50)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context1 = {
                 'career_list':career_list,
                'lead_list_count': True if career_list_count != 0 else False,
                'lead_lis': False if career_list_count != 0 else True,
            }
            context.update(context1)
            return render(request, 'career_module/career_module_list.html', context)
        if 'submit1' in request.POST:
            career_list = Career_module.objects.filter( current_stage='Called for Interview',)
            paginator = Paginator(career_list, 50)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context2 = {
                'career_list': career_list,
            }
            context.update(context2)
            return render(request, 'career_module/career_module_list.html', context)
        if 'submit2' in request.POST:
            career_list = Career_module.objects.filter(current_stage='Applied but Not called for Interview', )
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context3 = {
                'career_list': career_list,
            }
            context.update(context3)

            return render(request, 'career_module/career_module_list.html', context)
        if 'submit3' in request.POST:
            career_list = Career_module.objects.filter(current_stage='Selection in Progress', )
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context4 = {
                'career_list': career_list,
            }
            context.update(context4)

            return render(request, 'career_module/career_module_list.html', context)
        if 'submit4' in request.POST:
            career_list = Career_module.objects.filter(current_stage='Selected', )
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context5 = {
                'career_list': career_list,
            }
            context.update(context5)

            return render(request, 'career_module/career_module_list.html', context)
        if 'submit5' in request.POST:
            career_list = Career_module.objects.filter(current_stage='Rejected', )
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context6 = {
                'career_list': career_list,
            }
            context.update(context6)

            return render(request, 'career_module/career_module_list.html', context)
        if 'submit6' in request.POST:
            career_list = Career_module.objects.filter(current_stage='Future Reference', )
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context7 = {
                'career_list': career_list,
            }
            context.update(context7)

            return render(request, 'career_module/career_module_list.html', context)
        if 'submit7' in request.POST:
            career_list = Career_module.objects.filter(current_stage='Did not Joined', )
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context7 = {
                'career_list': career_list,
            }
            context.update(context7)

            return render(request, 'career_module/career_module_list.html', context)
        if 'sub1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')

            career_list = Career_module.objects.filter(entry_timedate__range=[start_date, end_date]).order_by('-id')

            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context2 = {
                'career_list': career_list,
                'search_msg': 'Search result for date range: ' + start_date + ' TO ' + end_date,
            }
            context.update(context2)

        elif 'sub2' in request.POST:
            contact = request.POST.get('contact')
            career_list = Career_module.objects.filter(phone_no__icontains=contact).order_by('-id')

            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context2 = {
                'career_list': career_list,
                'search_msg': 'Search result for Customer Contact No: ' + contact,
            }
            context.update(context2)

        elif 'sub3' in request.POST:
            email = request.POST.get('email')
            career_list = Career_module.objects.filter(candidate_email__icontains=email).order_by('-id')

            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context2 = {
                'career_list': career_list,
                'search_msg': 'Search result for Customer Email ID: ' + email,
            }
            context.update(context2)

        elif 'sub4' in request.POST:
            candidate_name = request.POST.get('candidate_name')
            career_list = Career_module.objects.filter(candidate_name__icontains=candidate_name).order_by('-id')

            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context2 = {
                'career_list': career_list,
                'search_msg': 'Search result for Candidate Name: ' + candidate_name,
            }
            context.update(context2)


        elif 'sub5' in request.POST:
            company = request.POST.get('company')
            career_list = Career_module.objects.filter(company_name__icontains=company).order_by('-id')

            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context2 = {
                'career_list': career_list,
                'search_msg': 'Search result for Company Name: ' + company,
            }
            context.update(context2)




    return render(request,'career_module/career_module_list.html',context)

@login_required(login_url='/')
def career_module_form(request):
    if Career_module.objects.all().count() == 0:
        application_number = 166353
    else:
        application_number = Career_module.objects.latest('id').application_no + 1
    initial_data = {
        'application_no': application_number,
    }

    career_form = Career_moduleForm(initial=initial_data)
    education_form = EducationForm()
    workexp_form = WorkExpForm()
    if request.method == 'POST' or request.method == 'FILES':
        current_stage = request.POST.get('current_stage')
        phone_no = request.POST.get('phone_no')
        candidate_name = request.POST.get('candidate_name')
        choose_position = request.POST.get('choose_position')
        candidate_email = request.POST.get('candidate_email')
        address = request.POST.get('address')
        institute_name = request.POST.get('institute_name')
        course = request.POST.get('course')
        year_of_completion = request.POST.get('year_of_completion')
        percentage = request.POST.get('percentage')
        company_name = request.POST.get('company_name')
        work_expirance_from = request.POST.get('work_expirance_from')
        work_expirance_to = request.POST.get('work_expirance_to')
        work_expirance_details = request.POST.get('work_expirance_details')
        designation = request.POST.get('designation')
        date_of_birth = request.POST.get('date_of_birth')
        achievements = request.POST.get('achievements')
        candidate_resume = request.FILES.get('candidate_resume')
        maxedu_id = request.POST.get('maxedu_id')
        maxwork_exp = request.POST.get('maxwork_exp')

        if Career_module.objects.filter(phone_no=phone_no).count() > 0:
            messages.error(request, "You have already applied! Our Team Will Get In Touch With You Soon!!!")
            return redirect('/career_module_form/')

        is_sales_candidate = True if choose_position == 'Sales Position' else False
        is_technical_candidate = True if choose_position == 'Technical Position' else False

        item = Career_module()
        item.candidate_resume = candidate_resume
        item.current_stage = current_stage
        item.application_no = application_number
        item.phone_no = phone_no
        item.candidate_name = candidate_name
        item.choose_position = Position.objects.get(position=choose_position)
        item.candidate_email = candidate_email
        item.address = address
        item.institute_name = institute_name
        item.course = course
        if date_of_birth != '':
            item.date_of_birth = date_of_birth
        item.year_of_completion = year_of_completion
        item.percentage = percentage
        item.is_technical_candidate = is_technical_candidate
        item.is_sales_candidate = is_sales_candidate


        item.save()

        edu_detail = EducationalDetails()
        edu_detail.institute_name = institute_name
        edu_detail.course = course
        edu_detail.year_of_completion = year_of_completion
        edu_detail.percentage = percentage
        edu_detail.achievements = achievements
        edu_detail.career_id = Career_module.objects.get(id=item.id)

        edu_detail.save()

        if int(maxedu_id) > 1:
            for i in range(2, int(maxedu_id)+1 ):
                institute_name = request.POST.get('institute_name'+str(i))
                course = request.POST.get('course'+str(i))
                year_of_completion = request.POST.get('year_of_completion'+str(i))
                percentage = request.POST.get('percentage'+str(i))
                achievements = request.POST.get('achievements'+str(i))

                edu_detail = EducationalDetails()

                edu_detail.institute_name = institute_name
                edu_detail.course = course
                edu_detail.year_of_completion = year_of_completion
                edu_detail.percentage = percentage
                edu_detail.achievements = achievements
                edu_detail.career_id = Career_module.objects.get(id=item.id)
                edu_detail.save()

        work_exp = WorkExperience()
        if work_expirance_from != '':
            work_exp.work_expirance_from = work_expirance_from
        if work_expirance_to != '':
            work_exp.work_expirance_to = work_expirance_to
        if work_expirance_details != '':
            work_exp.work_expirance_details = work_expirance_details
        work_exp.designation = designation
        work_exp.company_name = company_name
        work_exp.career_id =  Career_module.objects.get(id=item.id)
        work_exp.save()

        if int(maxwork_exp) > 1:
            for i in range(2, int(maxwork_exp)+1 ):
                company_name = request.POST.get('company_name'+str(i))
                work_expirance_from = request.POST.get('work_expirance_from'+str(i))
                work_expirance_to = request.POST.get('work_expirance_to'+str(i))
                work_expirance_details = request.POST.get('work_expirance_details'+str(i))
                designation = request.POST.get('designation'+str(i))

                work_exp = WorkExperience()

                if work_expirance_from != '':
                    work_exp.work_expirance_from = work_expirance_from
                if work_expirance_to != '':
                    work_exp.work_expirance_to = work_expirance_to
                if work_expirance_details != '':
                    work_exp.work_expirance_details = work_expirance_details
                work_exp.designation = designation
                work_exp.company_name = company_name
                work_exp.career_id = Career_module.objects.get(id=item.id)
                work_exp.save()

        msg = "Thank You For Interest, Your application no is "+str(application_number)+". Our Team Will Get In Touch With You Soon!!!"

        try:

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + phone_no + "&message=" + msg + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text
            email_send = EmailMessage('HSCo - Career, Form Submitted Successfully!!! ',
                                      '', settings.EMAIL_HOST_USER,
                      [candidate_email, ])
            part1 = MIMEText(msg, 'plain')
            part2 = MIMEText(user(request), 'html')
            email_send.attach(part1)
            email_send.attach(part2)
            email_send.send()
        except:
            print("exception occured!!")
            pass
        return redirect('/career_module_list/')


    positions = Position.objects.all()
    context = {
        'career_form':career_form,
        'education_form':education_form,
        'workexp_form':workexp_form,
        'positions':positions,
    }
    return render(request,'career_module/career_module_form.html',context)

@login_required(login_url='/')
def career_module_form_hsc(request):
    if Career_module.objects.all().count() == 0:
        application_number = 166353
    else:
        application_number = Career_module.objects.latest('id').application_no + 1
    initial_data = {
        'application_no': application_number,
    }
    education_form = EducationForm()
    workexp_form = WorkExpForm()
    career_form = Career_moduleForm(initial=initial_data)
    positions = Position.objects.all()

    context = {
        'career_form': career_form,
        'education_form': education_form,
        'workexp_form': workexp_form,
        'positions': positions
    }
    if request.method == 'POST' or request.method == 'FILES':
        phone_no = request.POST.get('phone_no')
        candidate_name = request.POST.get('candidate_name')
        choose_position = request.POST.get('choose_position')
        candidate_email = request.POST.get('candidate_email')
        address = request.POST.get('address')
        institute_name = request.POST.get('institute_name')
        course = request.POST.get('course')
        year_of_completion = request.POST.get('year_of_completion')
        percentage = request.POST.get('percentage')
        company_name = request.POST.get('company_name')
        work_expirance_from = request.POST.get('work_expirance_from')
        work_expirance_to = request.POST.get('work_expirance_to')
        work_expirance_details = request.POST.get('work_expirance_details')
        designation = request.POST.get('designation')
        date_of_birth = request.POST.get('date_of_birth')
        maxedu_id = request.POST.get('maxedu_id')
        maxwork_exp = request.POST.get('maxwork_exp')
        candidate_resume = request.FILES.get('candidate_resume')
        if Career_module.objects.filter(phone_no=phone_no).count()>0:
            messages.error(request, "You have already applied! Our Team Will Get In Touch With You Soon!!!")
            return redirect('http://139.59.76.87/career.hindustanscale.com/')
        is_sales_candidate = True if choose_position == 'Sales Position' else False
        is_technical_candidate = True if choose_position == 'Technical Position' else False

        item = Career_module()

        item.current_stage = 'Applied but Not called for Interview'
        item.application_no = application_number
        item.phone_no = phone_no
        item.candidate_name = candidate_name
        item.choose_position = Position.objects.get(position=choose_position)
        item.candidate_email = candidate_email
        item.address = address
        item.institute_name = institute_name
        item.course = course
        if date_of_birth != '':
            item.date_of_birth = date_of_birth
        item.year_of_completion = year_of_completion
        item.percentage = percentage
        item.is_technical_candidate = is_technical_candidate
        item.is_sales_candidate = is_sales_candidate
        item.candidate_resume = candidate_resume

        item.save()

        edu_detail = EducationalDetails()
        edu_detail.institute_name = institute_name
        edu_detail.course = course
        edu_detail.year_of_completion = year_of_completion
        edu_detail.percentage = percentage
        edu_detail.career_id = Career_module.objects.get(id=item.id)
        edu_detail.save()

        if int(maxedu_id) > 1:
            for i in range(2, int(maxedu_id) + 1):
                institute_name = request.POST.get('institute_name' + str(i))
                course = request.POST.get('course' + str(i))
                year_of_completion = request.POST.get('year_of_completion' + str(i))
                percentage = request.POST.get('percentage' + str(i))
                achievements = request.POST.get('achievements'+str(i))

                edu_detail = EducationalDetails()

                edu_detail.institute_name = institute_name
                edu_detail.course = course
                edu_detail.year_of_completion = year_of_completion
                edu_detail.percentage = percentage
                edu_detail.achievements = achievements
                edu_detail.career_id = Career_module.objects.get(id=item.id)
                edu_detail.save()

        work_exp = WorkExperience()
        if work_expirance_from != '':
            work_exp.work_expirance_from = work_expirance_from
        if work_expirance_to != '':
            work_exp.work_expirance_to = work_expirance_to
        if work_expirance_details != '':
            work_exp.work_expirance_details = work_expirance_details
        work_exp.designation = designation
        work_exp.company_name = company_name
        work_exp.career_id = Career_module.objects.get(id=item.id)
        work_exp.save()

        if int(maxwork_exp) > 1:
            for i in range(2, int(maxwork_exp) + 1):
                company_name = request.POST.get('company_name' + str(i))
                work_expirance_from = request.POST.get('work_expirance_from' + str(i))
                work_expirance_to = request.POST.get('work_expirance_to' + str(i))
                work_expirance_details = request.POST.get('work_expirance_details' + str(i))
                designation = request.POST.get('designation' + str(i))

                work_exp = WorkExperience()

                if work_expirance_from != '':
                    work_exp.work_expirance_from = work_expirance_from
                if work_expirance_to != '':
                    work_exp.work_expirance_to = work_expirance_to
                if work_expirance_details != '':
                    work_exp.work_expirance_details = work_expirance_details
                work_exp.designation = designation
                work_exp.company_name = company_name
                work_exp.career_id = Career_module.objects.get(id=item.id)
                work_exp.save()
                messages.success(request, "Thank You For Interest, Your application no is " + str(application_number) + ". Our Team Will Get In Touch With You Soon!!!")

        msg = "Thank You For Interest, Your application no is "+str(application_number)+". Our Team Will Get In Touch With You Soon!!!"


        try:

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + phone_no + "&message=" + msg + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text

            email_send = EmailMessage('HSCo - Career, Form Submitted Successfully!!! ',
                                      '', settings.EMAIL_HOST_USER,
                                      [candidate_email, ])
            part1 = MIMEText(msg, 'plain')
            part2 = MIMEText(user(request), 'html')
            email_send.attach(part1)
            email_send.attach(part2)
            email_send.send()
        except:
            print("exception occured!!")
            pass


        context = {
        'career_form': career_form,
        'education_form': education_form,
        'workexp_form': workexp_form
    }

    return render(request, 'career_module/career_module_form_hsc.html',context)

@login_required(login_url='/')
def update_career_module_from(request,id):

    career_module_id = Career_module.objects.get(id=id)
    work_exp_list = WorkExperience.objects.filter(career_id=id).order_by('id')
    edu_details_list = EducationalDetails.objects.filter(career_id=id).order_by('id')

    work_exp_list_id = WorkExperience.objects.filter(career_id=id).values('id')
    edu_details_list_id = EducationalDetails.objects.filter(career_id=id).values('id')

    career_module_initial_data = {
        'notes': career_module_id.notes,
        'current_stage': career_module_id.current_stage,
        'application_no': career_module_id.application_no,
        'phone_no': career_module_id.phone_no,
        'candidate_name': career_module_id.candidate_name,
        'candidate_email': career_module_id.candidate_email,
        'address': career_module_id.address,
        'date_of_birth': career_module_id.date_of_birth,
        'current_salary': career_module_id.current_salary,
        'aadhar_card': career_module_id.aadhar_card,
        'pan_card_availabe': career_module_id.pan_card_availabe,
        'bank_account': career_module_id.bank_account,
        'say_yourself': career_module_id.say_yourself,
        'confidance': career_module_id.confidance,
        'without_job_with_reason': career_module_id.without_job_with_reason,
        'reason_for_last_job_before': career_module_id.reason_for_last_job_before,
        'working_from_10_to_8_and': career_module_id.working_from_10_to_8_and,
        'any_question': career_module_id.any_question,
        'any_question_yes': career_module_id.any_question_yes,
        'comfortable_english': career_module_id.comfortable_english,
        'how_good_english': career_module_id.how_good_english,
        'comfortable_marathi': career_module_id.comfortable_marathi,
        'working_from_10_to_8': career_module_id.working_from_10_to_8,
        'weighting_scale_manufactures_mumbai': career_module_id.weighting_scale_manufactures_mumbai,
        'excel_formate': career_module_id.excel_formate,
        'sum_in_excel': career_module_id.sum_in_excel,
        'time_taken': career_module_id.time_taken,
        'take_out_60': career_module_id.take_out_60,
        'time_to_disorder_wire_pcb': career_module_id.time_to_disorder_wire_pcb,
        'time_to_solder_wire_back': career_module_id.time_to_solder_wire_back,
        'soldering_strong': career_module_id.soldering_strong,
        'value_of_resister': career_module_id.value_of_resister,
        'open_and_short_circuit': career_module_id.open_and_short_circuit,
    }

    latest_work_exp_id = WorkExperience.objects.filter(career_id=id).latest('id').id
    latest_edu_details_id = EducationalDetails.objects.filter(career_id=id).latest('id').id


    career_form = Career_moduleForm(initial=career_module_initial_data)
    # education_form = EducationForm(initial=education_initial_data)
    # workexp_form = WorkExpForm(initial=workexp_initial_data)

    if request.method == 'POST' or request.method == 'FILES':
        current_stage = request.POST.get('current_stage')
        application_no = request.POST.get('application_no')
        phone_no = request.POST.get('phone_no')
        candidate_name = request.POST.get('candidate_name')
        choose_position = request.POST.get('choose_position')
        candidate_email = request.POST.get('candidate_email')
        address = request.POST.get('address')
        institute_name = request.POST.get('institute_name')
        course = request.POST.get('course')
        year_of_completion = request.POST.get('year_of_completion')
        percentage = request.POST.get('percentage')
        company_name = request.POST.get('company_name')
        work_expirance_from = request.POST.get('work_expirance_from')
        work_expirance_to = request.POST.get('work_expirance_to')
        date_of_birth = request.POST.get('date_of_birth')
        work_expirance_details = request.POST.get('work_expirance_details')
        designation = request.POST.get('designation')
        current_salary = request.POST.get('current_salary')
        aadhar_card = request.POST.get('aadhar_card')
        pan_card_availabe = request.POST.get('pan_card_availabe')
        bank_account = request.POST.get('bank_account')
        say_yourself = request.POST.get('say_yourself')
        confidance = request.POST.get('confidance')
        without_job_with_reason = request.POST.get('without_job_with_reason')
        reason_for_last_job_before = request.POST.get('reason_for_last_job_before')
        working_from_10_to_8_and = request.POST.get('working_from_10_to_8')
        any_question_yes = request.POST.get('any_question_yes')
        comfortable_english = request.POST.get('comfortable_english')
        how_good_english = request.POST.get('how_good_english')
        comfortable_marathi = request.POST.get('comfortable_marathi')
        working_from_10_to_8 = request.POST.get('working_from_10_to_8')
        weighting_scale_manufactures_mumbai = request.POST.get('weighting_scale_manufactures_mumbai')
        excel_formate = request.POST.get('excel_formate')
        sum_in_excel = request.POST.get('sum_in_excel')
        time_taken = request.POST.get('time_taken')
        take_out_60 = request.POST.get('take_out_60')
        time_to_disorder_wire_pcb = request.POST.get('time_to_disorder_wire_pcb')
        time_to_solder_wire_back = request.POST.get('time_to_solder_wire_back')
        soldering_strong = request.POST.get('soldering_strong')
        value_of_resister = request.POST.get('value_of_resister')
        open_and_short_circuit = request.POST.get('open_and_short_circuit')
        notes = request.POST.get('notes')
        maxedu_id = request.POST.get('maxedu_id')
        maxwork_exp = request.POST.get('maxwork_exp')
        candidate_resume = request.FILES.get('candidate_resume')


        item = Career_module.objects.get(id=id)
        item.candidate_resume = candidate_resume
        item.current_stage = current_stage
        item.application_no = application_no
        item.phone_no = phone_no
        item.candidate_name = candidate_name
        item.choose_position = Position.objects.get(position=choose_position)
        item.candidate_email = candidate_email
        item.address = address
        item.institute_name = institute_name
        item.course = course
        item.year_of_completion = year_of_completion
        item.percentage = percentage
        item.company_name = company_name
        item.work_expirance_from = work_expirance_from
        item.work_expirance_to = work_expirance_to
        item.date_of_birth = date_of_birth
        item.work_expirance_details = work_expirance_details
        item.designation = designation
        item.current_salary = current_salary
        item.aadhar_card = aadhar_card
        item.pan_card_availabe = pan_card_availabe
        item.bank_account = bank_account
        item.say_yourself = say_yourself
        item.confidance = confidance
        item.without_job_with_reason = without_job_with_reason
        item.reason_for_last_job_before = reason_for_last_job_before
        item.working_from_10_to_8 = working_from_10_to_8_and
        item.any_question_yes = any_question_yes
        item.comfortable_english = comfortable_english
        item.how_good_english = how_good_english
        item.comfortable_marathi = comfortable_marathi
        item.working_from_10_to_8 = working_from_10_to_8
        item.weighting_scale_manufactures_mumbai = weighting_scale_manufactures_mumbai
        item.excel_formate = excel_formate
        item.sum_in_excel = sum_in_excel
        item.time_taken = time_taken
        item.take_out_60 = take_out_60
        item.time_to_disorder_wire_pcb = time_to_disorder_wire_pcb
        item.time_to_solder_wire_back = time_to_solder_wire_back
        item.soldering_strong = soldering_strong
        item.value_of_resister = value_of_resister
        item.open_and_short_circuit = open_and_short_circuit
        item.notes = notes
        item.save(update_fields=['candidate_resume','current_stage','application_no','phone_no','candidate_name','choose_position','candidate_email',
                                 'address','current_salary','aadhar_card','pan_card_availabe',
                                 'bank_account','say_yourself','confidance','without_job_with_reason','reason_for_last_job_before','working_from_10_to_8_and',
                                 'any_question_yes','comfortable_english','how_good_english','comfortable_marathi','working_from_10_to_8',
                                 'weighting_scale_manufactures_mumbai','excel_formate','sum_in_excel','time_taken','take_out_60',
                                 'time_to_disorder_wire_pcb','time_to_solder_wire_back','soldering_strong','value_of_resister','open_and_short_circuit','date_of_birth','notes'])

        if int(maxwork_exp) > latest_work_exp_id:
            for i in range(latest_work_exp_id, int(maxwork_exp) ):
                company_name = request.POST.get('company_name'+str(i))
                work_expirance_from = request.POST.get('work_expirance_from'+str(i))
                work_expirance_to = request.POST.get('work_expirance_to'+str(i))
                work_expirance_details = request.POST.get('work_expirance_details'+str(i))
                designation = request.POST.get('designation'+str(i))

                work_exp = WorkExperience()

                if work_expirance_from != '':
                    work_exp.work_expirance_from = work_expirance_from
                if work_expirance_to != '':
                    work_exp.work_expirance_to = work_expirance_to
                if work_expirance_details != '':
                    work_exp.work_expirance_details = work_expirance_details
                work_exp.designation = designation
                work_exp.company_name = company_name
                work_exp.career_id = Career_module.objects.get(id=id)
                work_exp.save()

        if int(maxedu_id) > latest_edu_details_id:
            for i in range(latest_edu_details_id, int(maxedu_id) ):

                institute_name = request.POST.get('institute_name'+str(i))
                course = request.POST.get('course'+str(i))
                year_of_completion = request.POST.get('year_of_completion'+str(i))
                percentage = request.POST.get('percentage'+str(i))
                achievements = request.POST.get('achievements'+str(i))

                edu_detail = EducationalDetails()

                edu_detail.institute_name = institute_name
                edu_detail.course = course
                edu_detail.year_of_completion = year_of_completion
                edu_detail.percentage = percentage
                edu_detail.achievements = achievements
                edu_detail.career_id = Career_module.objects.get(id=id)
                edu_detail.save()


        for i in work_exp_list_id:
            company_name = request.POST.get('company_name' + str(i['id']))
            work_expirance_from = request.POST.get('work_expirance_from' + str(i['id']))
            work_expirance_to = request.POST.get('work_expirance_to' + str(i['id']))
            work_expirance_details = request.POST.get('work_expirance_details' + str(i['id']))
            designation = request.POST.get('designation' + str(i['id']))

            work_exp = WorkExperience.objects.get(id=i['id'])

            if work_expirance_from != '':
                work_exp.work_expirance_from = work_expirance_from
            if work_expirance_to != '':
                work_exp.work_expirance_to = work_expirance_to
            if work_expirance_details != '':
                work_exp.work_expirance_details = work_expirance_details
            work_exp.designation = designation
            work_exp.company_name = company_name
            work_exp.save(update_fields=['work_expirance_from', 'work_expirance_to', 'work_expirance_details', 'designation','company_name'])
        for i in edu_details_list_id:

            institute_name = request.POST.get('institute_name' +str(i['id']))
            course = request.POST.get('course' + str(i['id']))
            year_of_completion = request.POST.get('year_of_completion' + str(i['id']))
            percentage = request.POST.get('percentage' + str(i['id']))
            achievements = request.POST.get('achievements' + str(i['id']))

            edu_detail = EducationalDetails.objects.get(id=i['id'])

            edu_detail.institute_name = institute_name
            edu_detail.course = course
            edu_detail.year_of_completion = year_of_completion
            edu_detail.percentage = percentage
            edu_detail.achievements = achievements
            edu_detail.save(update_fields=['institute_name', 'course', 'year_of_completion', 'percentage','achievements'])
        return redirect('/update_career_module_from/'+str(id))
    positions = Position.objects.filter(~Q(position=career_module_id.choose_position.position))

    context = {
        'career_form':career_form,
        'work_exp_list':work_exp_list,
        'edu_details_list':edu_details_list,
        'career_module_id':career_module_id,
        'latest_work_exp_id':latest_work_exp_id,
        'latest_edu_details_id':latest_edu_details_id,
        'positions':positions,
    }
    return render(request,'career_module/update_career_module_from.html',context)