from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from .forms import UserRegistrationForm, UserAddressForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()

            login(self.request, user)
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:deposit_money')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name='accounts/user_login.html'
    redirect_authenticated_user = True


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class UserDetails(LoginRequiredMixin, ListView):
    template_name = 'accounts/user_details.html'
    form_data = {}

    def get(self, request, *args, **kwargs):
        # import pdb
        # pdb.set_trace()
        c_user = self.request.user
        
        # form = TransactionDateRangeForm(request.GET or None)
        # if form.is_valid():
        #     self.form_data = form.cleaned_data
        args = {}
        args['name'] = c_user.first_name + ' ' + c_user.last_name
        args['email'] = c_user
        args['phone'] = "20111435465"
        args['bdate'] = c_user.account.birth_date
        args['acc_no'] = c_user.account.account_no
        args['card'] = "22344532212"
        args['balance'] = c_user.account.balance
        return render(request, 'accounts/user_details.html', args)
    



    
    # def get_queryset(self):
    #     queryset = super().get_queryset().filter(
    #         account=self.request.user.account
    #     )

    #     daterange = self.form_data.get("daterange")

    #     if daterange:
    #         queryset = queryset.filter(timestamp__date__range=daterange)

    #     return queryset.distinct()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context.update({
    #         'account': self.request.user.account,
    #         'form': TransactionDateRangeForm(self.request.GET or None)
    #     })