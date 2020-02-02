from django.contrib import admin
from .models import Dough, ToppingGroup, Topping


admin.site.register(Dough)
admin.site.register(ToppingGroup)
admin.site.register(Topping)
