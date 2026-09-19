from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Family, Member


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':

        pin = request.POST.get('pin', '').strip()

        if len(pin) != 6 or not pin.isdigit():
            return render(
                request,
                'login.html',
                {
                    'error': 'Please enter a valid 6-digit PIN.'
                }
            )

        user = authenticate(
            request,
            username='asha',
            password=pin
        )

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        return render(
            request,
            'login.html',
            {
                'error': 'Incorrect PIN. Please try again.'
            }
        )

    return render(request, 'login.html')


@login_required
def logout_view(request):

    logout(request)

    return redirect('login')


@login_required
def dashboard(request):

    total_families = Family.objects.count()
    total_members = Member.objects.count()

    return render(
        request,
        'dashboard.html',
        {
            'total_families': total_families,
            'total_members': total_members,
        }
    )


@login_required
def add_family(request):

    if request.method == 'POST':

        family_name = request.POST.get('family_name')
        village = request.POST.get('village')
        house_number = request.POST.get('house_number')
        family_number = request.POST.get('family_number')

        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        area = request.POST.get('area')
        pin_code = request.POST.get('pin_code')

        family = Family.objects.create(
            family_name=family_name,
            village=village,
            house_number=house_number,
            family_number=family_number,
            contact_number=contact_number,
            address=address,
            area=area,
            pin_code=pin_code
        )

        # After saving family, directly open Add Member page
        # and send the newly created family ID.
        return redirect(
            f'/add-member/?family_id={family.id}'
        )

    return render(
        request,
        'add_family.html'
    )


@login_required
def family_list(request):

    search = request.GET.get('search', '')

    families = Family.objects.all().order_by('-created_at')

    if search:
        families = families.filter(
            family_name__icontains=search
        )

    return render(
        request,
        'family_list.html',
        {
            'families': families,
            'search': search,
        }
    )


@login_required
def family_detail(request, family_id):

    family = get_object_or_404(
        Family,
        id=family_id
    )

    members = family.members.all().order_by('id')

    return render(
        request,
        'family_detail.html',
        {
            'family': family,
            'members': members,
        }
    )


@login_required
def add_member(request):
    families = Family.objects.all().order_by('family_name')

    if request.method == 'POST':

        family_id = request.POST.get('family')
        family = get_object_or_404(Family, id=family_id)

        name = request.POST.get('name')
        gender = request.POST.get('gender')
        blood_group = request.POST.get('blood_group')
        relation = request.POST.get('relation')

        currently_pregnant = (
            request.POST.get('currently_pregnant') == 'Yes'
        )

        date_of_birth = request.POST.get('date_of_birth')
        religion = request.POST.get('religion')
        caste = request.POST.get('caste')

        bpl = request.POST.get('bpl') == 'Yes'

        mobile_number = request.POST.get('mobile_number')
        bpl_number = request.POST.get('bpl_number')

        ayushman_card_number = request.POST.get(
            'ayushman_card_number'
        )

        aadhaar_number = request.POST.get(
            'aadhaar_number'
        )

        abha_number = request.POST.get(
            'abha_number'
        )

        profile_photo = request.FILES.get(
            'profile_photo'
        )

        ayushman_card_file = request.FILES.get(
            'ayushman_card_file'
        )

        aadhaar_card_file = request.FILES.get(
            'aadhaar_card_file'
        )

        abha_card_file = request.FILES.get(
            'abha_card_file'
        )

        disease = request.POST.get('disease')
        alive_status = request.POST.get('alive_status')
        remarks = request.POST.get('remarks')

        member = Member.objects.create(
            family=family,
            name=name,
            profile_photo=profile_photo,
            gender=gender,
            blood_group=blood_group,
            relation=relation,
            currently_pregnant=currently_pregnant,
            date_of_birth=date_of_birth,
            religion=religion,
            caste=caste,
            bpl=bpl,
            mobile_number=mobile_number,
            bpl_number=bpl_number,
            ayushman_card_number=ayushman_card_number,
            aadhaar_number=aadhaar_number,
            abha_number=abha_number,
            ayushman_card_file=ayushman_card_file,
            aadhaar_card_file=aadhaar_card_file,
            abha_card_file=abha_card_file,
            disease=disease,
            alive_status=alive_status,
            remarks=remarks
        )

        return redirect(
            'family_detail',
            family_id=family.id
        )

    return render(
        request,
        'add_member.html',
        {'families': families}
    )


@login_required
def member_list(request):

    search = request.GET.get(
        'search',
        ''
    )

    members = (
        Member.objects
        .select_related('family')
        .all()
        .order_by('name')
    )

    if search:
        members = members.filter(
            name__icontains=search
        )

    return render(
        request,
        'member_list.html',
        {
            'members': members,
            'search': search,
        }
    )


@login_required
def member_detail(request, member_id):

    member = get_object_or_404(
        Member,
        id=member_id
    )

    return render(
        request,
        'member_detail.html',
        {
            'member': member,
            'edit_mode': False,
        }
    )


@login_required
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':

        member.name = request.POST.get('name')
        member.gender = request.POST.get('gender')
        member.blood_group = request.POST.get('blood_group')
        member.relation = request.POST.get('relation')

        member.currently_pregnant = (
            request.POST.get('currently_pregnant') == 'Yes'
        )

        member.date_of_birth = request.POST.get(
            'date_of_birth'
        )

        member.religion = request.POST.get('religion')
        member.caste = request.POST.get('caste')

        member.bpl = (
            request.POST.get('bpl') == 'Yes'
        )

        member.mobile_number = request.POST.get(
            'mobile_number'
        )

        member.bpl_number = request.POST.get(
            'bpl_number'
        )

        member.ayushman_card_number = request.POST.get(
            'ayushman_card_number'
        )

        member.aadhaar_number = request.POST.get(
            'aadhaar_number'
        )

        member.abha_number = request.POST.get(
            'abha_number'
        )

        member.disease = request.POST.get('disease')
        member.alive_status = request.POST.get(
            'alive_status'
        )

        member.remarks = request.POST.get('remarks')

        family_id = request.POST.get('family')

        if family_id:
            member.family = get_object_or_404(
                Family,
                id=family_id
            )

        if request.FILES.get('profile_photo'):
            member.profile_photo = request.FILES.get(
                'profile_photo'
            )

        if request.FILES.get('ayushman_card_file'):
            member.ayushman_card_file = request.FILES.get(
                'ayushman_card_file'
            )

        if request.FILES.get('aadhaar_card_file'):
            member.aadhaar_card_file = request.FILES.get(
                'aadhaar_card_file'
            )

        if request.FILES.get('abha_card_file'):
            member.abha_card_file = request.FILES.get(
                'abha_card_file'
            )

        member.save()

        return redirect(
            'member_detail',
            member_id=member.id
        )

    families = Family.objects.all().order_by(
        'family_name'
    )

    return render(
        request,
        'member_detail.html',
        {
            'member': member,
            'families': families,
            'edit_mode': True
        }
    )