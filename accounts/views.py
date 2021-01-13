from __future__ import print_function

from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.text import slugify
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView, TemplateView
from django.views.generic.edit import FormMixin
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django_countries import countries
from django_countries.fields import Country
from rest_framework import status

from amjuLoans import email_settings
from amjuLoans.cloudinary_settings import cloudinary_upload_preset, cloudinary_url
from amjuLoans.utils import random_string_generator
from banks.models import BankCode
from borrowers.models import Borrower
from company.models import Company
from loans.models import LoanRequests
from mincore.models import PlanDetails, SupportTickets
from amjuLoans.mixins import NextUrlMixin, RequestFormAttachMixin
from .forms import LoginForm, RegisterForm, GuestForm, ReactivateEmailForm, UserDetailChangeForm, UserUpdateForm
from .models import EmailActivation, Profile, User


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'

    def get_object(self):
        return self.request.user


class AccountEmailActivateView(FormMixin, View):
    success_url = '/login/'
    form_class = ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "Your email has been confirmed. Proceed to login!")
                return redirect("login")
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("account-password:password_reset")
                    msg = """Your email has already been confirmed
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect("login")
        context = {'form': self.get_form(), 'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = """Activation link sent, please check your email."""
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {'form': form, "key": self.key}
        return render(self.request, 'registration/activation-error.html', context)


class GuestRegisterView(NextUrlMixin, RequestFormAttachMixin, CreateView):
    form_class = GuestForm
    default_next = '/register/'

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)


class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'accounts/login.html'
    default_next = '/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)

    def render_to_response(self, context, **response_kwargs):
        if context and self.request.user.is_authenticated:
            profile_obj = Profile.objects.get(user=self.request.user)
            try:
                company_obj = Company.objects.get(user=profile_obj)
            except Company.MultipleObjectsReturned:
                company_qs = Company.objects.filter(user=profile_obj)
                company_obj = company_qs.first()
            return redirect(reverse('company-url:dashboard', kwargs={'slug': company_obj.slug}))
        return super(LoginView, self).render_to_response(context, **response_kwargs)


class RegisterView(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'
    success_message = "An Email Has Been Sent To You For Confirmation, Please Activate Your Email"


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'accounts/detail-update-view.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Your Account Details'
        return context

    def post(self, *args, **kwargs):
        form = UserDetailChangeForm(self.request.POST or None, instance=self.get_object())
        user_profile_obj = Profile.objects.get(user=self.get_object())
        phone = self.request.POST.get("phone")
        full_name = self.request.POST.get("full_name")
        if form.is_valid():
            user_profile_obj.phone = phone
            user_profile_obj.save()
            self.get_object().full_name = full_name
            form.save()
            messages.success(self.request, "Successfully Completed Account Activation")
            return redirect(reverse('success'))
        else:
            messages.error(self.request, "Please Validate Fields, Check If Phone is In +234XXXXXXXX format")
        return render(self.request, 'accounts/detail-update-view.html', {'form': form})

    def get_success_url(self):
        return reverse("account:profile-detail", kwargs={'slug': self.get_object().profile.slug})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-detail.html'

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['user_comp_qs'] = self.object.user.profile.company_set.all()
        context['user_plan'] = self.object.user.profile.get_plan_display()  # .plan #get_modelfield_display()
        context['works_for'] = self.object.user.profile.working_for.all()
        staffs_ = [staff_obj for staff_obj in self.object.user.profile.company_set.all()]
        context['staff_count'] = (len(staffs_))
        full_name = str(self.request.user.full_name)
        first_name = full_name.split()[0]
        last_name = full_name.split()[1]

        Borrower.objects.get_or_create(
            user=self.get_object(),
            first_name=first_name,
            last_name=last_name,
            email=self.request.user.email,
            phone=self.request.user.profile.phone
        )
        context['current_borrower'] = Borrower.objects.get_or_create(user=self.request.user.profile)

        if timezone.now() <= self.object.user.profile.trial_days:
            context["plan_title"] = "ACTIVE"
        else:
            context["plan_title"] = "EXPIRED"
        try:
            context['plan_info_obj'] = PlanDetails.objects.get(name__iexact=self.object.user.profile.get_plan_display())
        except:
            context['plan_info_obj'] = "No Fee Plan"

        user_code = [code_obj.keycode for code_obj in Profile.objects.all()]
        context["userKeyCode"] = user_code
        context['userTickets_qs'] = SupportTickets.objects.filter(user__exact=self.object)[:10]
        return context

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        thisBorrower = Borrower.objects.get(user=self.request.user.profile)
        LoanRequests.objects.create(
            borrower=thisBorrower,
            amount=self.request.POST.get('amount'),
            request_status='Still Processing',
            duration_figure=int(self.request.POST.get('durationFigure')),
            duration=self.request.POST.get('durationPeriod'),
            repayment_interval=self.request.POST.get('repaymentInterval'),
            slug=slugify("{borrower}-{amount}-{primaryKey}".format(
                borrower=thisBorrower, amount=self.request.POST.get('amount'), primaryKey=random_string_generator(6)
            ))
        )
        # Send an Email Saying Loan Application Was Made By A User
        html_ = "The User ({loanUser}), just applied for a loan, validate user account and process loan application".format(
            loanUser=thisBorrower)
        subject = 'New Loan Application From {loanUser}'.format(loanUser=thisBorrower)
        from_email = email_settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email]

        from django.core.mail import EmailMessage
        message = EmailMessage(
            subject, html_, from_email, recipient_list
        )
        message.fail_silently = False
        message.send()
        return JsonResponse({'message': 'Successful'}, status=200)


class SystemUserProfile(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Profile
    template_name = 'accounts/system-user-profile.html'
    success_message = "User profile has Been Updated Successfully!"

    def get_context_data(self, **kwargs):
        context = super(SystemUserProfile, self).get_context_data(**kwargs)
        print(kwargs, self.kwargs)
        company_obj = Company.objects.get(slug=self.kwargs.get('company_slug'))
        loans_done_by_staff = company_obj.loan_set.filter(account_officer=kwargs.get('object'))
        context['userCompany_qs'] = company_obj.user.company_set.all()
        context['current_company_plan'] = company_obj.user.plan
        context['works_for'] = self.object.working_for.all()
        context.update({
            'company': company_obj,
            'object': company_obj,
            'loans_conducted': loans_done_by_staff,
            'form': UserUpdateForm(instance=self.get_object())
        })
        return context

    def post(self, *args, **kwargs):
        company_obj = Company.objects.get(slug=self.kwargs.get('company_slug'))
        user_form = UserUpdateForm(self.request.POST or None, self.request.FILES or None, instance=self.get_object())
        if user_form.is_valid():
            user_form.save()
            return redirect(reverse('account:company-user-detail',
                                    kwargs={'company_slug': company_obj.slug, 'slug': self.get_object().slug}))
        return JsonResponse({'message': 'An error during submission!'})


class RequestBorrowerProfile(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Profile
    template_name = 'accounts/borrower-profile.html'
    success_message = "User profile has Been Updated Successfully!"

    def get_context_data(self, **kwargs):
        context = super(RequestBorrowerProfile, self).get_context_data(**kwargs)
        try:
            user_borrower = Borrower.objects.get(user=self.get_object())
        except Borrower.DoesNotExist:
            user_borrower = None
            return user_borrower
        full_name = str(self.request.user.full_name)
        first_name = full_name.split()[0]
        last_name = full_name.split()[1]
        context['banks'] = BankCode.objects.all()
        context['country_qs'] = countries
        context['cloudinary_upload_preset'] = cloudinary_upload_preset
        context['cloudinary_url'] = cloudinary_url
        context.update({
            "first_name": first_name,
            "last_name": last_name,
            "borrower": user_borrower
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        if context:
            if self.request.user.profile != self.get_object():
                return reverse('404_')
        return super(RequestBorrowerProfile, self).render_to_response(context, **response_kwargs)

    def post(self, *args, **kwargs):
        print(self.request.POST)
        bank_inst = BankCode.objects.get(name__exact=self.request.POST.get('bank'))
        print(bank_inst)
        country_inst = Country(code=self.request.POST.get('country'))
        print(country_inst, country_inst.name)
        company = Company.objects.get(name="Amju")
        print(company)
        borrower_instance = Borrower.objects.get(user=self.get_object())
        borrower_instance.registered_to = company
        borrower_instance.first_name = self.request.POST.get('firstName')
        borrower_instance.last_name = self.request.POST.get('lastName')
        borrower_instance.gender = self.request.POST.get('gender')
        borrower_instance.address = self.request.POST.get('address')
        borrower_instance.lga = self.request.POST.get('lga')
        borrower_instance.state = self.request.POST.get('state')
        borrower_instance.country = country_inst
        borrower_instance.title = self.request.POST.get('title')
        borrower_instance.land_line = self.request.POST.get('landPhone')
        borrower_instance.business_name = self.request.POST.get('businessName')
        borrower_instance.working_status = self.request.POST.get('workingStatus')
        borrower_instance.unique_identifier = self.request.POST.get('unique_identifier')
        borrower_instance.bank = bank_inst
        borrower_instance.account_number = self.request.POST.get('accountNumber')
        borrower_instance.bvn = self.request.POST.get('bvn')
        borrower_instance.card_number = self.request.POST.get('cardNumber')
        borrower_instance.expiry_month = self.request.POST.get('expiryMonth')
        borrower_instance.expiry_year = self.request.POST.get('expiryYear')
        borrower_instance.cvv = self.request.POST.get('cvv')
        borrower_instance.date_of_birth = self.request.POST.get('dateOfBirth')
        borrower_instance.slug = slugify("{firstName}-{lastName}-{company}-{primaryKey}".format(
            firstName=self.request.POST.get('firstName'), lastName=self.request.POST.get('lastName'),
            company=self.get_object(), primaryKey=random_string_generator(4)
        ))
        borrower_instance.save()

        thisUser = Profile.objects.get(user=self.request.user)
        thisUser.phone = self.request.POST.get('landPhone')
        thisUser.save()
        return JsonResponse({'message': 'Account completed successfully!'})


class ImageUploadReceiver(View):
    def post(self, *args, **kwargs):
        instance = Borrower.objects.get(user=self.request.user.profile)
        instance.imageUrl = self.request.POST.get("imageUrl")
        instance.save()
        return JsonResponse({'message': 'Profile Image Updated successfully!'})
