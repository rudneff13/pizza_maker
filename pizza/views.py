from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail, get_connection
from .models import Dough, ToppingGroup, Topping
from .forms import OrderForm


class IndexView(TemplateView):
    template_name = 'pizza/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dough'] = Dough.objects.all()
        context['topping_group'] = ToppingGroup.objects.prefetch_related('toppings').all()
        return context

    @staticmethod
    def post(request):

        if request.POST.get('dough', False):
            dough = request.POST['dough']
            total = 0
            for topping in Topping.objects.all():
                amount = int(request.POST.get(topping.name))
                if amount:
                    total += topping.price*amount
            total = round(total, 2)
            request.session['total'] = total
            request.session['dough'] = dough

            return HttpResponseRedirect(reverse('order'))


class OrderView(FormView):
    template_name = 'pizza/order_form.html'
    form_class = OrderForm
    success_url = '/thanks'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dough'] = self.request.session.get('dough')
        context['total'] = self.request.session.get('total')
        return context

    def form_valid(self, form):
        cd = form.cleaned_data
        con = get_connection('django.core.mail.backends.console.EmailBackend')
        send_mail(
            'Заказ пиццы',
            f"""
            Ваше имя: {cd.get('name')}.
            Ваш телефон: {cd.get('phone')}.
            Ваш email: {cd.get('email')}.
            Вы заказали пиццу на тесте: {self.request.session.get('dough')}.
            Заказ на общую сумму: {self.request.session.get('total')}$.
            """,
            'best-pizza-ever@django.com',
            [f"{cd.get('email')}"],
            connection=con
        )
        return super().form_valid(form)


def thank_you(request):
    return render(request, 'pizza/thanks.html')
