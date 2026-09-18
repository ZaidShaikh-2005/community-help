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
                {'error': 'Please enter a valid 6-digit PIN.'}
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
            {'error': 'Incorrect PIN. Please try again.'}
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
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        area = request.POST.get('area')
        pin_code = request.POST.get('pin_code')

        family = Family.objects.create(
            family_name=family_name,
            contact_number=contact_number,
            address=address,
            area=area,
            pin_code=pin_code
        )

        return redirect('family_detail', family_id=family.id)

    return render(request, 'add_family.html')


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
    family = get_object_or_404(Family, id=family_id)
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
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        relation = request.POST.get('relation')
        family_id = request.POST.get('family')

        family = get_object_or_404(Family, id=family_id)

        Member.objects.create(
            name=name,
            age=age,
            gender=gender,
            relation=relation,
            family=family
        )

        return redirect('family_detail', family_id=family.id)

    return render(
        request,
        'add_member.html',
        {
            'families': families,
        }
    )


@login_required
def member_list(request):
    search = request.GET.get('search', '')

    members = Member.objects.select_related('family').all().order_by('name')

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
    member = get_object_or_404(Member, id=member_id)

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
        member.age = request.POST.get('age')
        member.gender = request.POST.get('gender')
        member.relation = request.POST.get('relation')

        family_id = request.POST.get('family')

        if family_id:
            member.family = get_object_or_404(
                Family,
                id=family_id
            )

        member.save()

        return redirect(
            'member_detail',
            member_id=member.id
        )

    families = Family.objects.all().order_by('family_name')

    return render(
        request,
        'member_detail.html',
        {
            'member': member,
            'families': families,
            'edit_mode': True,
        }
    )