from django.contrib import admin
from .models.location import SavedAddress
from .models.payment import PaymentRecord
from .models.point import PointRecord
from .models.create_call import CreateCall


class SavedAddressAdmin(admin.ModelAdmin):
    list_display = ('user_ref', 'address', 'district', 'pincode', 'state', 'country', 'locality')
    search_fields = ('address', 'district', 'state', 'country', 'locality')
    list_filter = ('state', 'country')


admin.site.register(SavedAddress, SavedAddressAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user_ref','payment_id','transaction_date','transaction_amount', 'status')


admin.site.register(PaymentRecord, PaymentAdmin)


class PointAdmin(admin.ModelAdmin):
    list_display = ('user_ref', 'receiver','details','type_subscription','left_call','date','last_subscription_amount')


admin.site.register(PointRecord, PointAdmin)


class CreateCallAdmin(admin.ModelAdmin):
    list_display = ('id','sender', 'receiver','message','meetingtime')


admin.site.register(CreateCall, CreateCallAdmin)