from django.contrib import admin
from .models import UsersData,vendor,feedbacks_of_product,product,Sub_category,Cart,category,Offer,Order,Wishlist,Orderitem,Area,feedback,Payment,order_table,owner_order_table,Owner_Payment

# Register your models here.
class UsersDataAdmin(admin.ModelAdmin):
    list_display=('u_name','email_id','password','contact')
admin.site.register(UsersData,UsersDataAdmin)

class vendorAdmin(admin.ModelAdmin):
    list_display=('v_gstno','Shop_name','contact')
admin.site.register(vendor,vendorAdmin)

class productAdmin(admin.ModelAdmin):
    list_display=('p_name','p_discription','p_price','size_id')

admin.site.register(product,productAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display=('venders','c_name','c_image')
admin.site.register(category,categoryAdmin)

class Sub_categoryAdmin(admin.ModelAdmin):
    list_display=('venders','C_id','name','Sc_image')
admin.site.register(Sub_category,Sub_categoryAdmin)

class OfferAdmin(admin.ModelAdmin):
    list_display=('Start_date','End_date','P_id','descr')
#admin.site.register(Offer,OfferAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=('U_id','P_id')
#admin.site.register(Cart,CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=('U_id','V_id','Order_date','Contact_no')
#admin.site.register(Order,OrderAdmin)

class OrderitemAdmin(admin.ModelAdmin):
    list_display=('P_id','Quantity','Amount')
#admin.site.register(Orderitem,OrderitemAdmin)

class WishlistAdmin(admin.ModelAdmin):
    list_display=('U_id','P_id')
admin.site.register(Wishlist,WishlistAdmin)

class AreaADmin(admin.ModelAdmin):
    list_display=('name','Pincode')
#admin.site.register(Area,AreaADmin)

class feedbackAdmin(admin.ModelAdmin):
    list_display=('U_id','P_id','f_id','f_date','f_messge')
#admin.site.register(feedback,feedbackAdmin)

#admin.site.register(Payment)
admin.site.register(order_table)
#admin.site.register(Owner_Payment)
admin.site.register(feedbacks_of_product)


from django.contrib.auth.models import Group
admin.site.unregister(Group)
admin.site.site_header = 'cleaning Service Administration'
admin.site.index_title = 'Cleaning Services Admin Panel'               
admin.site.site_title = 'cleaning Service Administration'