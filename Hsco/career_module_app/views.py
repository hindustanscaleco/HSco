from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.shortcuts import render, redirect
from .forms import Career_moduleForm
from .models import Career_module
from datetime import datetime

def career_module_list(request):
    career_list = Career_module.objects.all().order_by('-id')
    paginator = Paginator(career_list, 25)  # Show 25 contacts per page
    page = request.GET.get('page')
    career_list = paginator.get_page(page)
    context = {
        'career_list': career_list,
    }
    if request.method == 'POST':
        total_stages = Career_module.objects.all().values('current_stage').annotate(dcount=Count('current_stage'))
        for i in total_stages:
            x = i
            if x['current_stage'] == 'Called for interview, interview is not taken':
                called_nointerview = x['dcount']
                context2 = {
                    'called_nointerview': called_nointerview,
                }
                context.update(context2)
            if x['current_stage'] == 'Applied but not call for interview':
                applied_nocall = x['dcount']
                context5 = {
                    'applied_nocall': applied_nocall,
                }
                context.update(context5)
            if x['current_stage'] == 'Interview in Progress':
                interview_progress = x['dcount']
                context6 = {
                    'interview_progress': interview_progress,
                }
                context.update(context6)
            if x['current_stage'] == 'Interview is taken, not selected':
                interview_notselected = x['dcount']
                context7 = {
                    'interview_notselected': interview_notselected,
                }
                context.update(context7)
            if x['current_stage'] == 'Interview is done and rejected':
                interview_rejected = x['dcount']
                context8 = {
                    'interview_rejected': interview_rejected,
                }
                context.update(context8)
            if x['current_stage'] == 'Interview is done and preserved for Future':
                interview_preserved = x['dcount']
                context9 = {
                    'interview_preserved': interview_preserved,
                }
                context.update(context9)
        if 'sort_submit' in request.POST:
            YEAR = request.POST.get('YEAR')
            MONTH = request.POST.get('MONTH')

            career_list = Career_module.objects.filter(entry_timedate__month=MONTH, entry_timedate__year=YEAR).order_by('-id')

            career_list_count = Career_module.objects.filter(entry_timedate__month=MONTH, entry_timedate__year=YEAR).count()
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
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
            career_list = Career_module.objects.filter( current_stage='Called for interview, interview is not taken',)
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context2 = {
                'career_list': career_list,
            }
            context.update(context2)
            return render(request, 'career_module/career_module_list.html', context)
        if 'submit2' in request.POST:
            career_list = Career_module.objects.filter(current_stage='Applied but not call for interview', )
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context3 = {
                'career_list': career_list,
            }
            context.update(context3)

            return render(request, 'career_module/career_module_list.html', context)
        if 'submit3' in request.POST:
            career_list = Career_module.objects.filter(current_stage='Interview in Progress', )
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context4 = {
                'career_list': career_list,
            }
            context.update(context4)

            return render(request, 'career_module/career_module_list.html', context)
        if 'submit4' in request.POST:
            career_list = Career_module.objects.filter(current_stage='Interview is taken, not selected', )
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context5 = {
                'career_list': career_list,
            }
            context.update(context5)

            return render(request, 'career_module/career_module_list.html', context)
        if 'submit5' in request.POST:
            career_list = Career_module.objects.filter(current_stage='Interview is done and rejected', )
            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context6 = {
                'career_list': career_list,
            }
            context.update(context6)

            return render(request, 'career_module/career_module_list.html', context)
        if 'submit6' in request.POST:
            career_list = Career_module.objects.filter(current_stage='Interview is done and preserved for Future', )
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
            career_list = Career_module.objects.filter(phone_no=contact).order_by('-id')

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
            career_list = Career_module.objects.filter(candidate_email=email).order_by('-id')

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
            career_list = Career_module.objects.filter(candidate_name=candidate_name).order_by('-id')

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
            career_list = Career_module.objects.filter(company_name=company).order_by('-id')

            paginator = Paginator(career_list, 25)  # Show 25 contacts per page
            page = request.GET.get('page')
            career_list = paginator.get_page(page)
            context2 = {
                'career_list': career_list,
                'search_msg': 'Search result for Company Name: ' + company,
            }
            context.update(context2)


    total_stages = Career_module.objects.all().values('current_stage').annotate(dcount=Count('current_stage'))
    for i in total_stages:
        x = i
        if x['current_stage'] == 'Called for interview, interview is not taken':
            called_nointerview = x['dcount']
            context2 = {
                'called_nointerview': called_nointerview,
            }
            context.update(context2)
        if x['current_stage'] == 'Applied but not call for interview':
            applied_nocall = x['dcount']
            context5 = {
                'applied_nocall': applied_nocall,
            }
            context.update(context5)
        if x['current_stage'] == 'Interview in Progress':
            interview_progress = x['dcount']
            context6 = {
                'interview_progress': interview_progress,
            }
            context.update(context6)
        if x['current_stage'] == 'Interview is taken, not selected':
            interview_notselected = x['dcount']
            context7 = {
                'interview_notselected': interview_notselected,
            }
            context.update(context7)
        if x['current_stage'] == 'Interview is done and rejected':
            interview_rejected = x['dcount']
            context8 = {
                'interview_rejected': interview_rejected,
            }
            context.update(context8)
        if x['current_stage'] == 'Interview is done and preserved for Future':
            interview_preserved = x['dcount']
            context9 = {
                'interview_preserved': interview_preserved,
            }
            context.update(context9)

    return render(request,'career_module/career_module_list.html',context)

def career_module_form(request):
    career_form = Career_moduleForm()
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
        work_expirance_details = request.POST.get('work_expirance_details')
        designation = request.POST.get('designation')
        date_of_birth = request.POST.get('date_of_birth')



        is_sales_candidate = True if choose_position == 'Sales Position' else False
        is_technical_candidate = True if choose_position == 'Technical Position' else False


        item = Career_module()

        item.current_stage = current_stage
        item.application_no = application_no
        item.phone_no = phone_no
        item.candidate_name = candidate_name
        item.choose_position = choose_position
        item.candidate_email = candidate_email
        item.address = address
        item.institute_name = institute_name
        item.course = course
        item.date_of_birth = date_of_birth
        item.year_of_completion = year_of_completion
        item.percentage = percentage
        item.company_name = company_name
        item.is_technical_candidate = is_technical_candidate
        item.is_sales_candidate = is_sales_candidate
        if work_expirance_from != '':
            item.work_expirance_from = work_expirance_from
        if work_expirance_to != '':
            item.work_expirance_to = work_expirance_to
        if work_expirance_details != '':
            item.work_expirance_details = work_expirance_details
        item.designation = designation

        item.save()

        return redirect('/career_module_list/')

    context = {
        'career_form':career_form
    }
    return render(request,'career_module/career_module_form.html',context)

def update_career_module_from(request,id):
    career_module_id = Career_module.objects.get(id=id)
    career_module_initial_data = {
        'current_stage': career_module_id.current_stage,
        'application_no': career_module_id.application_no,
        'phone_no': career_module_id.phone_no,
        'candidate_name': career_module_id.candidate_name,
        'choose_position': career_module_id.choose_position,
        'candidate_email': career_module_id.candidate_email,
        'address': career_module_id.address,
        'institute_name': career_module_id.institute_name,
        'course': career_module_id.course,
        'year_of_completion': career_module_id.year_of_completion,
        'percentage': career_module_id.percentage,
        'company_name': career_module_id.company_name,
        'work_expirance_from': career_module_id.work_expirance_from,
        'work_expirance_to': career_module_id.work_expirance_to,
        'date_of_birth': career_module_id.date_of_birth,
        'work_expirance_details': career_module_id.work_expirance_details,
        'designation': career_module_id.designation,
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



    career_form = Career_moduleForm(initial=career_module_initial_data)


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





        item = Career_module.objects.get(id=id)
        item.current_stage = current_stage
        item.application_no = application_no
        item.phone_no = phone_no
        item.candidate_name = candidate_name
        item.choose_position = choose_position
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
        item.save(update_fields=['current_stage','application_no','phone_no','candidate_name','choose_position','candidate_email',
                                 'address','institute_name','course','year_of_completion','percentage','company_name','work_expirance_from',
                                 'work_expirance_to','work_expirance_details','designation','current_salary','aadhar_card','pan_card_availabe',
                                 'bank_account','say_yourself','confidance','without_job_with_reason','reason_for_last_job_before','working_from_10_to_8_and',
                                 'any_question_yes','comfortable_english','how_good_english','comfortable_marathi','working_from_10_to_8',
                                 'weighting_scale_manufactures_mumbai','excel_formate','sum_in_excel','time_taken','take_out_60',
                                 'time_to_disorder_wire_pcb','time_to_solder_wire_back','soldering_strong','value_of_resister','open_and_short_circuit','date_of_birth',])

        return redirect('/update_career_module_from/'+str(id))

    context = {
        'career_form':career_form,
        'career_module_id':career_module_id,
    }
    return render(request,'career_module/update_career_module_from.html',context)