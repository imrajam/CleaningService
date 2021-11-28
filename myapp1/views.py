from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .models import UsersData
from django.views import View

#email
import smtplib
import email.message

import json
#time
import time
from datetime import timezone
import pytz
from django.contrib import messages
import datetime
# paytm ids -------------------------
from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse_lazy
from django.urls import reverse

from django.db.models import Q

# Gerate OTP
import random

# SMPT Email Send
import smtplib 
import email.message
# Create your views here.

# Html To Pdf -------------------

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from django.http import HttpResponse
from django.views.generic import View

import pdfkit

# Html To Pdf ------------------- 


# Excel ----------------------------

# pip install xlwt
# pip install xlutils    # Required when reading excel file
# pip install xlrd       # Required when reading excel file
import xlwt
# Excel ----------------------------

# pip install pycryptodome

MERCHANT_KEY = '@BLNEQSVwvSAf36N'
MERCHANT_ID = 'DSpKiN27217000419407'
# Create your views here.

def login(request):
    if request.POST:
        em = request.POST['username']
        pas = request.POST['pass']
        try:
            valid = UsersData.objects.get(email_id=em)
            if valid.password == pas:
                request.session['user_data'] = valid.email_id
                return redirect('home')
            else:
                messages.error(request, 'Wrong Password...')
                return render(request,'Login_Regi/Login.html')
        except:
            messages.error(request, 'Wrong Email Id...')
            return render(request,'Login_Regi/Login.html')
    return render(request,'Login_Regi/Login.html')

def register(request):
    if request.POST:
        username = request.POST['username']
        email_id = request.POST['email_id']
        pno = request.POST['pno']
        pass1 = request.POST['pass']
        hint = request.POST['Hint']


        
        try:
            valid = UsersData.objects.get(email_id=email_id)
            messages.error(request, 'Email Id Already In Use...')
            return render(request,'Login_Regi/Regi.html')
        except:
            try:
                valid = UsersData.objects.get(contact=pno)
                messages.error(request, 'Contact No Already Exists...')
                return render(request,'Login_Regi/Regi.html')
            except:
                obj = UsersData()
                obj.u_name = username
                obj.email_id = email_id
                obj.contact = pno
                obj.password = pass1
                obj.forgot_ans=hint
                obj.save()
                return redirect('login')
    return render(request,'Login_Regi/Regi.html')


def Index(request):
    vends = vendor.objects.all()
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
        cart = request.session['cart']
    print(cart)    
    try:
        q = request.GET.get('search')
    except:
        q = None
        if q:
            prod= product.objects.filter(Q(p_name__icontains=q) | Q(p_discription__icontains=q) | Q(p_price__icontains=q))
            dealer = vendor.objects.filter(Q(Shop_name__icontains=q) | Q(shop_address__icontains=q))
            if 'user_data' in request.session.keys():
                em = request.session['user_data']
                valid = UsersData.objects.get(email_id=em)
                data = {
                    'pro' : prod,
                    'des': dealer,
                    'owns':vends,
                    'user_data':valid
                }
            else:
                data = {
                    'pro' : prod,
                    'des': dealer,
                    'owns':vends,
                }
    else:
        if 'user_data' in request.session.keys():
            em = request.session['user_data']
            valid = UsersData.objects.get(email_id=em)
            data={'owns':vends,'user_data':valid}
            try:
                valid_cart = Cart.objects.get(U_id=valid)
                request.session['cart'] = json.loads(valid_cart.P_id)
                cart = request.session['cart']
                cart_rec = json.dumps(cart)
                valid_cart.P_id = cart_rec
                valid_cart.save()
            except:
                valid_cart = Cart()
                cart_rec = json.dumps(cart)
                valid_cart.U_id = valid
                valid_cart.P_id = cart_rec
                valid_cart.save()
        else:
            data={'owns':vends}
            
    return render(request,'index.html',data)
    


# Forget Password -----------------

def Confirm(request):
    if request.POST:
        data = request.POST['conf']
        try:
            valid = UsersData.objects.get(forgot_ans=data)
            if valid:
                request.session['useremail'] = valid.email_id
                return redirect('newpassword')
            else:
                return HttpResponse('Wrong Answer')    
        except:
            messages.error(request, 'Wrong Hint..')
    return render(request,'Confirm.html')

def newpassword(request):
    if request.session.has_key('useremail'):
        if request.POST:
            pass_1 = request.POST['pass1']
            pass_2 = request.POST['pass2']
            
            if pass_1 == pass_2:
                valid = UsersData.objects.get(email_id=request.session['useremail'])
                valid.password = pass_2
                valid.save()
                del request.session['useremail']
                return redirect('login')
            else:
                return HttpResponse("<h2><a href=''>Passwords Are Not Same ...</a></h2>")
        return render(request,'New_Pass.html')
    return redirect('login')

# def forgot_pass(request):
#     if 'user' in request.session:
#         if request.POST:
#             pass1 = request.POST['pass1']
#             pass2 = request.POST['pass2']
            
#             if pass1 == pass2:
#                 obj = Register.objects.get(email=request.session['user'])
#                 obj.password = pass2
#                 obj.save()
#                 del request.session['user']
#                 return redirect('logi')
#             else:
#                 messages.add_message(request, messages.ERROR, 'Not Same')
            
#         return render(request,'forgot.html')
#     return redirect('logi')


# def forgot_pass(request):
#     if request.POST:
#         email1 = request.POST['email']
#         print("xdd",email1)
#         number1 = request.POST['m_no']
#         print("num:",number1)
#         print("dsc")
#         val=UsersData.objects.get(email_id=request.POST['email'])
#         print("val",val)
#         valid = UsersData.objects.get(email_id=email1)
#         print("done")
#         if int(valid.contact) == int(number1):
#             print(email1)
#             request.session['useremail'] = email1
            
#             numbers = [1,2,3,4,5,6,7,8,9,0]
#             num = ""
#             for i in range(4):
#                 num += str(random.choice(numbers))
            
#             num = int(num)
#             print(num)
            
#             # ============== Email ==============
            
#             sender_email = "rajmakhijani123@gmail.com"
#             sender_pass = "9033893037123@"
#             receiver_email = email1

#             server = smtplib.SMTP('smtp.gmail.com',587)

#             your_message = "This Is Your OTP Number = "+str(num)

#             print(your_message)

#             msg = email.message.Message()
#             msg['Subject'] = "Your OTP From Best Cleaning Services"
#             msg['From'] = sender_email
#             msg['To'] = receiver_email
#             password = sender_pass
#             msg.add_header('Content-Type','text/html')
#             msg.set_payload(your_message)

#             server.starttls()
#             server.login(msg['From'],password)
#             server.sendmail(msg['From'],msg['To'],msg.as_string())
            
#             # ============== End Email ===========
            
#             request.session['otp'] = num
            
#             return render(request,'OTP.html',{'otp':num})
                                
#         else:
#             return HttpResponse("<h2><a href=''>Mobile Number Is Not Registered</a></h2>")
#             return redirect('forgotpass')
#         #return HttpResponse("<h2><a href=''>Email Is Not Registered</a></h2>")
#         return redirect('forgotpass')
        
#     return render(request,'Forget_Pass.html')

# def otpcheck(request):
#     if request.session.has_key('otp'):
#         if request.POST:
#             otp = request.POST['otp']
#             if int(request.session['otp']) == int(otp):
#                 del request.session['otp']
#                 return redirect('newpassword')
#             else:
#                 return HttpResponse("<h2><a href=""> You Have Entered Wrong OTP </a></h2>")
#         else:
#             return redirect('forgotpass')
#     return redirect('login')


# Forget Password -----------------


def Shop_View(request,id):
    vends = vendor.objects.get(id=id)
    cats = category.objects.filter(venders=vends)
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(email_id=em)
        return render(request,'own_cats.html',{'owns':vends,'cats':cats,'user_data':valid})
    else:
        return render(request,'own_cats.html',{'owns':vends,'cats':cats})

def cat_view(request,id):
    cats = category.objects.get(id=id)
    sub_cat = Sub_category.objects.filter(C_id=cats)
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(email_id=em)
        return render(request,'own_cats.html',{'sub_cat':sub_cat,'cat':cats,'user_data':valid})
    else:
        return render(request,'own_cats.html',{'sub_cat':sub_cat,'cat':cats})

def show_prods(request,id):
    sub_cat = Sub_category.objects.get(id=id)
    prods = product.objects.filter(sub_cate=sub_cat)
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(email_id=em)
        return render(request,'own_cats.html',{'scat':sub_cat,'prod':prods,'user_data':valid})
    else:
        return render(request,'own_cats.html',{'scat':sub_cat,'prod':prods})

def Show_Product(request,id):
    if 'user_data' in request.session.keys():
        prod_data = product.objects.get(id=id)
        feed = feedbacks_of_product.objects.filter(Product_name = prod_data)
        Users = UsersData.objects.get(email_id=request.session['user_data'])
        try:
            obj = feedbacks_of_product.objects.get(Product_name=prod_data,cust=Users)
            
            if request.POST:
                ids = request.POST['ids']
                prate = request.POST['prate']
                pfeedback = request.POST['pfeedback']
                obj.rating = prate
                obj.feedback = pfeedback
                obj.save()
                return redirect('Show_Product',int(ids))
            return render(request,'own_cats.html',{'keys':obj,'feed':feed,'prod_data':prod_data,'user_data':Users})
        except:
            if request.POST:
                ids = request.POST['ids']
                prate = request.POST['prate']
                pfeedback = request.POST['pfeedback']
                
                obj = feedbacks_of_product()
                prod_data = product.objects.get(id=int(ids))
                obj.Product_name = prod_data
                obj.cust = Users
                obj.rating = prate
                obj.feedback = pfeedback
                obj.save()
                return redirect('Show_Product',int(ids))
            return render(request,'own_cats.html',{'feed':feed,'prod_data':prod_data,'user_data':Users})
    else:
        prod_data = product.objects.get(id=id)
        feed = feedbacks_of_product.objects.filter(Product_name = prod_data)
        return render(request,'own_cats.html',{'feed':feed,'prod_data':prod_data})

def Cust_Chats(request):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(email_id=request.session['user_data'])
        mci = ModelChat_IDs.objects.filter(usersData=Users)
        return render(request,'CustChats.html',{'mci':mci})
    else:
        return redirect('ved_login')  


# def Chat_Data_Show(request,id):
#     if 'user_data' in request.session.keys():
#         Users = UsersData.objects.get(email_id=request.session['user_data'])
#         venders = vendor.objects.get(id=id)
#         try:
#             moch = ModelChat_IDs.objects.get(usersData = Users,vendors=venders)
#             print(moch.chat_id)
#             mode_ch = Models_Chats.objects.filter(ch_ids=moch)
#             print(mode_ch)
#             if request.POST:
#                 ptext = request.POST['ptext']
                
#                 obj = Models_Chats()
#                 obj.ch_ids=moch
#                 obj.usersData = Users
#                 obj.problem_text = ptext
#                 obj.save()    
#                 # return redirect('Chat_Data_Show',id)
#             return render(request,'Chat_Data_Show.html',{'templates_data':"base.html",'mc':mode_ch,'moch':moch})
#         except:
#             tz= pytz.timezone('Asia/Kolkata')
#             time_now = datetime.datetime.now(timezone.utc).astimezone(tz)
#             millis = int(time.mktime(time_now.timetuple()))
#             chats_id = "Chat"+str(millis)
            
#             obj = ModelChat_IDs()
#             obj.chat_id = str(chats_id)
#             obj.usersData = Users
#             obj.vendors = venders
#             obj.save()
#             return render(request,'Chat_Data_Show.html',{'templates_data':"base.html"})
#     else:
#         return redirect('login')
    

def Customer_Orders(request):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(email_id=request.session['user_data'])
        otdata = order_table.objects.filter(cust=Users)
        rec = set()
        for i in otdata:
            rec.add(i.order_id)
        rec = list(rec)
        rec.sort()
        return render(request,'custAllOrders.html',{'oids':rec})
    else:
        return redirect('login')
    

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def ViewSpecify_Bill(request,Orids):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(email_id=request.session['user_data'])
        otdata = order_table.objects.filter(cust=Users,order_id=Orids)
        tots = 0
        status = ""
        for i in otdata:
            if i.cancel == True:
                status = "Cancle"
            tots += float(i.total)
        
        # if status == "Cancel":
        Current_Date = datetime.datetime.today() + datetime.timedelta(days=2)
        print ('Current Date: ' + str(Current_Date))

        NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=7)
        print ('Next Date: ' + str(NextDay_Date))
        data = {'status':status,'bilam':tots,'Orids':Orids,'orders':otdata,'oids':Orids,'users':Users,'NextDay_Date':NextDay_Date}
        return render(request,'ViewSpecificBill.html',data)
        
        # data = {'bilam':tots,'Orids':Orids,'orders':otdata,'oids':Orids,'users':Users,'status':status}
        # return render(request,'ViewSpecificBill.html',data)
    else:
        return redirect('login')

def View_specific(request,Orids):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(email_id=request.session['user_data'])
        otdata = order_table.objects.filter(cust=Users,order_id=Orids)
        tots = 0
        for i in otdata:
            tots += float(i.total)
        data = {'bilam':tots,'orders':otdata,'oids':Orids,'users':Users}
        pdf = render_to_pdf('GeneratePdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return redirect('login')

def cancel_data(request,Orids):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(email_id=request.session['user_data'])
        otdata = order_table.objects.filter(order_id=Orids)
        vendata = owner_order_table.objects.filter(order_id=Orids)
        
        for i in otdata:
            i.cancel = True
            i.save()
        
        for i in vendata:
            i.cancel = True
            i.save()
        
        return redirect('ViewSpecify_Bill',str(Orids))
        
    else:
        return redirect('login')

class Orders(View):
    def post(self, request):
        prod = request.POST.get('product')   
        print(prod)
        pay_data = request.POST.get('pay_data')   
        idss_data = request.POST.get('idss_data')   
        ids = request.POST.get('idss')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(prod)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(prod)
                    else:
                        cart[prod]  = quantity-1
                else:
                    cart[prod]  = quantity+1 
            else:
                cart[prod] = 1
        else:
            cart = {}
            cart[prod] = 1
            

        request.session['cart'] = cart
        
        Users = UsersData.objects.get(email_id=request.session['user_data'])
        
        try:
            valid = Cart.objects.get(U_id=Users)
            cart_rec = json.dumps(cart)
            valid.P_id = cart_rec
            valid.save()
        except:
            valid = Cart()
            cart_rec = json.dumps(cart)
            valid.U_id = Users
            valid.P_id = cart_rec
            valid.save()
        
        
        print('cart' , request.session['cart'])
        
        if ids != None:
            return redirect('show_prods',ids)
        elif idss_data != None:
            return redirect('product')
        elif pay_data != None:
            return redirect('cart_order')
        
    def get(self, request):
        return redirect('home')

def Add_Wish_List(request,id):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(email_id=request.session['user_data'])
        JI = product.objects.get(id=id)
        try:
            wL = Wishlist.objects.get(P_id=JI,U_id=user)
            return redirect('Wish_List')    
        except:
            WL = Wishlist()
            WL.U_id = user
            WL.P_id = JI
            WL.save()
        return redirect('Wish_List')
    else:
        return redirect('login')
    
def Wish_List(request):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(email_id=request.session['user_data'])
        U_id = Wishlist.objects.filter(U_id=user)
        return render(request,'WishList.html',{'prod':U_id})
    else:
        return redirect('login')


def COD_Data(request):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(email_id=request.session['user_data'])
        if request.POST:
            ids = list(request.session.get('cart').keys())
            products = product.get_products_by_id(ids)
            cart = request.session['cart']
            Final_Bill = {}
            # request.session['Final_Bill']
            print(cart)
            print("\n-----------------------")
            print(products)
            count = []
            for p in products:
                print("\n-----------------------")
                for i in ids:
                    if int(i) == p.id:
                        data = {}
                        data['id'] = p.id
                        print("product Name = ",p.p_name)
                        data['name'] = p.p_name
                        print("product QTY = ",cart.get(i))
                        data['qty'] = cart.get(i)
                        print("product Price = ",int(p.p_price) * int(cart.get(i)))
                        data['price'] = int(p.p_price) * int(cart.get(i))
                        count.append(data)

            Final_Bill['products'] = count
            Final_Bill['total_price'] = request.POST['total_price']
            print(request.POST['total_price'])
            print(Final_Bill)
            request.session['Final_Bill'] = Final_Bill
            print(request.session['Final_Bill'])
            request.session['Order_total'] = request.POST['total_price']
            print("\n\n-----------------------")
            
            show_data = request.session['Final_Bill']
            amo = request.session['Order_total']
            order_id = request.session['Order_id']
            
            # store in data base ----------------------  
            owner_nm = set()
            date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            for i in show_data['products']:
                prod = product.objects.get(id=i['id'])
                obj = order_table()
                obj.cust = user
                obj.order_id = order_id
                obj.date = str(date)
                obj.img = prod.imgs
                obj.product = i['name']
                obj.qty = i['qty']
                obj.price = prod.p_price
                obj.total = i['price']
                obj.payment = False
                obj.save()
                
                owner = vendor.objects.get(id=prod.venders.id)
                owner_nm.add(owner)
                owner_order = owner_order_table()
                owner_order.owner = owner
                owner_order.cust = user
                owner_order.order_id = order_id
                owner_order.date = str(date)
                owner_order.product = i['name']
                owner_order.qty = i['qty']
                owner_order.price = prod.p_price
                owner_order.total = i['price']
                owner_order.payment = False
                owner_order.save()
            
            for i in owner_nm:
                ven_user = vendor.objects.get(id=i.id)
                # data = order_table.objects.filter(cust = user)
                list_id = owner_order_table.objects.filter(owner = ven_user).values_list('order_id', flat=True)
                list_id = list(set(list(list_id)))
                
                for i in list_id: #Order1606811186
                    obj = Owner_Payment()
                    obj.Owner = ven_user
                    obj.Order_id = str(i)
                    data = owner_order_table.objects.filter(owner = ven_user).filter(order_id = str(i)) #Order1606811186
                    tot = 0
                    for d in data:
                        obj.date = d.date
                        tot += int(d.total)
                    obj.Order_amount = "Cash On Delivery"
                    obj.save()

            # session Delete ------------------ 
            cart = request.session.get('cart')
            if cart:
                request.session['Final_Bill'] = {}
                request.session['Order_total'] = {}
                request.session['cart'] = {}
                cart = request.session['cart']
                valid = Cart.objects.get(U_id=user)
                cart_rec = json.dumps(cart)
                valid.P_id = cart_rec
                valid.save()
            
            return redirect('home')
            
        
        print("CAll")
        ids = list(request.session.get('cart').keys())
        products = product.get_products_by_id(ids) #get_cust_details_by_id
        print(products)        
        
        tz= pytz.timezone('Asia/Kolkata')
        time_now = datetime.datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        order_id = "Order"+str(millis)
        request.session['Order_id'] = order_id
        # order_id = request.session['Order_id']
        

        Current_Date = datetime.datetime.today() + datetime.timedelta(days=4)
        print ('Current Date: ' + str(Current_Date))

        NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=5)
        print ('Next Date: ' + str(NextDay_Date))
        return render(request,'COD.html',{'products' : products,'Current_Date':Current_Date,'NextDay_Date':NextDay_Date})
    else:
        return redirect('login')
    
    
def cart_order(request):    
    if 'user_data' in request.session.keys():
        if request.POST:
            ids = list(request.session.get('cart').keys())
            products = product.get_products_by_id(ids)
            cart = request.session['cart']
            Final_Bill = {}
            count = []
            for p in products:
                for i in ids:
                    if int(i) == p.id:
                        data = {}
                        data['id'] = p.id
                        data['name'] = p.p_name
                        data['qty'] = cart.get(i)
                        data['price'] = int(p.p_price) * int(cart.get(i))
                        count.append(data)

            Final_Bill['products'] = count
            Final_Bill['total_price'] = request.POST['total_price']
            request.session['Final_Bill'] = Final_Bill
            request.session['Order_total'] = request.POST['total_price']
            return redirect('check')
        
        ids = list(request.session.get('cart').keys())
        products = product.get_products_by_id(ids) #get_cust_details_by_id
        return render(request,'order.html',{'products' : products})
    else:
        return redirect('login')

# Payment -----------------------------

def Checkout(request):
    if 'user_data' in request.session.keys():
        tz= pytz.timezone('Asia/Kolkata')
        time_now = datetime.datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(time_now.timetuple()))
        order_id = "Order"+str(millis)
        request.session['Order_id'] = order_id
        
        return redirect('process_payment')
    else:
        return redirect('login')
    
def Process_payment(request):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(email_id=request.session['user_data'])
        show_data = request.session['Final_Bill']
        amo = request.session['Order_total']
        host = request.get_host()
        param_dict = {
            'MID': MERCHANT_ID,
            'ORDER_ID': str(request.session['Order_id']),
            'TXN_AMOUNT': str(amo),
            'CUST_ID': 'darpan_salunke',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://{}{}'.format(host,reverse('handlerequest')),
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'payMent/paytm.html', {'param_dict': param_dict,'User':user,'Order':show_data})
    else:
        return redirect('login')

def EmailCall(request):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(email_id=request.session['user_data'])
        show_data = request.session['Final_Bill']
        amo = request.session['Order_total']
        order_id = request.session['Order_id']
        
        try:
            my_email = "darpansalunkework@gmail.com"
            my_pass = "Darpan@work"
            # fr_email = str(user.email)
            fr_email = "darpansalunke@gmail.com"
            
            server = smtplib.SMTP('smtp.gmail.com',587)
            mead_data = ""
            front = """
            <!DOCTYPE html>
            <html>
                <body>
                    <div>
                        <h2>Name : """ + user.u_name + """</h2>
                        <h2>Email : """ + user.email_id + """</h2>
                        <h2>Order No: """ + order_id + """</h2>
                    </div>
                    <br>
                    <div>
                        <table border="2">
                            <thead>
                                <tr>
                                    <th>
                                        Product Name
                                    </th>
                                    <th>
                                        Product Qty
                                    </th>
                                    <th>
                                        Product Price
                                    </th>
                                </tr>
                            </thead>
                            <tbody>"""
                            
            for i in show_data['products']:
                mead_data += """<tr>
                <td>""" + str(i['name']) + """ </td>
                <td>""" + str(i['qty']) + """ </td> 
                <td>""" + str(i['price']) + """</td></td>
                </tr> """
                
            ended = """<tr>
            <td colspan="2">
            You Have Paid
            </td><td> """ + str(amo) + """
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div> 
                    <br>
                    <div>
                        <h3>Thank you for visiting ....</h3>
                    </div>
                </body>
            </html>
            """
            email_content = front + mead_data + ended
            print(email_content)
            
            msg = email.message.Message()
            msg['Subject'] = 'Your Bill' 
            msg['From'] = my_email
            msg['To'] = fr_email
            password = my_pass
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)
            s = smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string())
            
            # store in data base ----------------------  
            owner_nm = set()
            date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            for i in show_data['products']:
                prod = product.objects.get(id=i['id'])
                obj = order_table()
                obj.cust = user
                obj.order_id = order_id
                obj.date = str(date)
                obj.img = prod.imgs
                obj.product = i['name']
                obj.qty = i['qty']
                obj.price = prod.p_price
                obj.total = i['price']
                obj.payment = True
                obj.save()
                
                owner = vendor.objects.get(id=prod.venders.id)
                owner_nm.add(owner)
                owner_order = owner_order_table()
                owner_order.owner = owner
                owner_order.cust = user
                owner_order.order_id = order_id
                owner_order.date = str(date)
                owner_order.product = i['name']
                owner_order.qty = i['qty']
                owner_order.price = prod.p_price
                owner_order.total = i['price']
                owner_order.payment = True
                owner_order.save()
            
            for i in owner_nm:
                ven_user = vendor.objects.get(id=i.id)
                # data = order_table.objects.filter(cust = user)
                list_id = owner_order_table.objects.filter(owner = ven_user).values_list('order_id', flat=True)
                list_id = list(set(list(list_id)))
                
                for i in list_id: #Order1606811186
                    obj = Owner_Payment()
                    obj.Owner = ven_user
                    obj.Order_id = str(i)
                    data = owner_order_table.objects.filter(owner = ven_user).filter(order_id = str(i)) #Order1606811186
                    tot = 0
                    for d in data:
                        obj.date = d.date
                        tot += int(d.total)
                    obj.Order_amount = tot
                    obj.save()

            # session Delete ------------------ 
            cart = request.session.get('cart')
            if cart:
                request.session['Final_Bill'] = {}
                request.session['Order_total'] = {}
                request.session['cart'] = {}
                cart = request.session['cart']
                valid = Cart.objects.get(U_id=user)
                cart_rec = json.dumps(cart)
                valid.P_id = cart_rec
                valid.save()
            
            return redirect('home')
        except:
            return HttpResponse("Email Not Sent")
    else:
        return redirect('login')    
    # return redirect('home')
            
        # ================== email end ================

@csrf_exempt
def Handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful') 
            return redirect('emailcall')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'paymentsatus.html', {'response': response_dict})

# Payment -----------------------------

def Profile(request):
    if 'user_data' in request.session.keys():
        user = UsersData.objects.get(email_id=request.session['user_data'])
        if request.POST:
            u_name = request.POST['u_name']
            Email = request.POST['Email']
            address = request.POST['address']
            contact = request.POST['contact']
            Password = request.POST['Password']
            
            user.u_name = u_name
            user.email_id = Email
            request.session['user_data'] = Email
            user.address = address
            user.contact = contact
            user.password = Password
            user.save()
            return redirect('home')
        return render(request,'Profile_data.html',{'user_data':user})
    else:
        return redirect('login')

def Cust_Logout(request):
    if 'user_data' in request.session.keys():
        Users = UsersData.objects.get(email_id=request.session['user_data'])
        
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        else:
            print(cart)
            try:
                valid = Cart.objects.get(U_id=Users)
                cart_rec = json.dumps(cart)
                valid.P_id = cart_rec
                valid.save()
                del request.session['cart']
            except:
                valid = Cart()
                cart_rec = json.dumps(cart)
                valid.U_id = Users
                valid.P_id = cart_rec
                valid.save()
                del request.session['cart']
        del request.session['user_data']
        return redirect('login')
    else:
        return redirect('login')

def about(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'Contact.html')

def Product(request):
    if 'user_data' in request.session.keys():
        em = request.session['user_data']
        valid = UsersData.objects.get(email_id=em)
        prods = product.objects.all()
        return render(request,'product.html',{'prod':prods,'user_data':valid})
    else:
        prods = product.objects.all()
        return render(request,'product.html',{'prod':prods})

def Product_details(request):
    return render(request,'product_detail3.html')

def blog(request):
    return render(request,'blog.html')

def form(request):
    return render(request,'Admin_templates/form.html')

# ===============================================================Vender Side====================================\

def Vender_Regis(request):
    if request.POST:
        obj = vendor()
        obj.v_name = request.POST['username']
        obj.v_gstno = request.POST['gstno']
        em = request.POST['email']
        try:
            valid = vendor.objects.get(email_id=em)
            messages.error(request, 'User Id Already In Use...')
            return render(request,'Admin_templates/Regi.html')
        except:
            obj.email_id = em
        obj.contact = request.POST['phoneno']
        obj.password = request.POST['pass']
        obj.save()
        return redirect('ved_login')
    return render(request,'Admin_templates/Regi.html')

def Vender_Login(request):
    if request.POST:
        em = request.POST['username']
        pas = request.POST['pass']
        try:
            valid = vendor.objects.get(email_id=em)
            if valid.password == pas:
                request.session['vender_data'] = valid.email_id
                return redirect('Vender_Dashboard')
            else:
                messages.error(request, 'Wrong Password...')
                return render(request,'Admin_templates/Login.html')
        except:
            messages.error(request, 'Wrong Email Id...')
            return render(request,'Admin_templates/Login.html')
    return render(request,'Admin_templates/Login.html')


# Forget Password -----------------

def Shop_forgot_pass(request):
    if request.POST:
        email1 = request.POST['email']
        number1 = request.POST['m_no']
            
        try:
            valid = vendor.objects.get(email_id=email1)
            if int(valid.contact) == int(number1):
                print(email1)
                request.session['useremail'] = email1
                
                numbers = [1,2,3,4,5,6,7,8,9,0]
                num = ""
                for i in range(4):
                    num += str(random.choice(numbers))
                
                num = int(num)
                print(num)
                
                # ============== Email ==============
                
                sender_email = "darpansalunkework@gmail.com"
                sender_pass = "Darpan@work"
                receiver_email = email1

                server = smtplib.SMTP('smtp.gmail.com',587)

                your_message = "This Is Your OTP Number = "+str(num)

                print(your_message)

                msg = email.message.Message()
                msg['Subject'] = "Your OTP From Advance Billing System"
                msg['From'] = sender_email
                msg['To'] = receiver_email
                password = sender_pass
                msg.add_header('Content-Type','text/html')
                msg.set_payload(your_message)

                server.starttls()
                server.login(msg['From'],password)
                server.sendmail(msg['From'],msg['To'],msg.as_string())
                
                # ============== End Email ===========
                
                request.session['otp'] = num
                
                return render(request,'Admin_templates/OTP.html',{'otp':num})
                                    
            else:
                return HttpResponse("<h2><a href=''>Mobile Number Is Not Registered</a></h2>")
                return redirect('Shop_forgotpass')
        except:
            return HttpResponse("<h2><a href=''>Email Is Not Registered</a></h2>")
            return redirect('shop_forgotpass')
        
    return render(request,'Admin_templates/Forget_Pass.html')

def Shop_otpcheck(request):
    if request.session.has_key('otp'):
        if request.POST:
            otp = request.POST['otp']
            if int(request.session['otp']) == int(otp):
                del request.session['otp']
                return redirect('Shop_newpassword')
            else:
                return HttpResponse("<h2><a href=""> You Have Entered Wrong OTP </a></h2>")
        else:
            return redirect('shop_forgotpass')
    return redirect('ved_login')

def Shop_newpassword(request):
    if request.session.has_key('useremail'):
        if request.POST:
            pass_1 = request.POST['pass1']
            pass_2 = request.POST['pass2']
            
            if pass_1 == pass_2:
                valid = vendor.objects.get(email_id=request.session['useremail'])
                valid.password = pass_2
                valid.save()
                del request.session['useremail']
                return redirect('ved_login')
            else:
                return HttpResponse("<h2><a href=''>Passwords Are Not Same ...</a></h2>")
        return render(request,'Admin_templates/New_Pass.html')
    return redirect('ved_login')

# Forget Password -----------------

def Vender_Logout(request):
    if 'vender_data' in request.session.keys():
        del request.session['vender_data']
        return redirect('ved_login')
    else:
        return redirect('ved_login')

def Vender_Dashboard(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        prods = product.objects.filter(venders=vender_data)
        cate = category.objects.filter(venders=vender_data)
        sub_cate = Sub_category.objects.filter(venders=vender_data)    
        try:
            q = request.GET.get('search')
        except:
            q = None
        if q:
            prod= product.objects.filter(Q(p_name__icontains=q) | Q(p_discription__icontains=q) | Q(p_price__icontains=q))
            
            data = {
                'pro' : prod,
                'vdata':vender_data,
                'cate' : cate
            }
        else:
            data={'vdata':vender_data,'cate' : cate}
            
        # return render(request,'index.html',data)
        return render(request,'Admin_templates/index.html',data)
    else:
        return redirect('ved_login')        

def Owner_Chats(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        mci = ModelChat_IDs.objects.filter(vendors=vender_data)
        return render(request,'Admin_templates/OwnerChats.html',{'mci':mci,'vdata':vender_data})
    else:
        return redirect('ved_login')     

# def Vender_Cust_Chat(request,id):
#     if 'vender_data' in request.session.keys():
#         venders = vendor.objects.get(email_id=request.session['vender_data'])
#         try:
#             moch = ModelChat_IDs.objects.get(id=id)
#             print(moch.chat_id)
#             mode_ch = Models_Chats.objects.filter(ch_ids=moch)
#             print(mode_ch)
#             if request.POST:
#                 ptext = request.POST['ptext']
                
#                 obj = Models_Chats()
#                 obj.ch_ids=moch
#                 obj.vendors = venders
#                 obj.problem_text = ptext
#                 obj.save()    
#                 # return redirect('Chat_Data_Show',id)
#             return render(request,'Chat_Data_Show.html',{'templates_data':"Admin_templates/admin_base.html",'vdata':venders,'mc':mode_ch,'moch':moch})
#         except:
#             return redirect('Vender_Dashboard')
#     else:
#         return redirect('ved_login')     


# def User_Form(request):
#     if request.POST:
#         nm = request.POST['nm']
#         em = request.POST['em']


#         obj = UsersData()
#         obj.u_name = nm
#         obj.email_id = em
#         obj.save()
#         return redirect('Vender_Dashboard')

#     return render(request,'Admin_templates/User_Form.html')

def vendor_form(request): 
    if "vender_data" in request.session.keys():
        obj = vendor.objects.get(email_id=str(request.session['vender_data']))
        if request.POST:
            vnm = request.POST['vnm']
            vgn = request.POST['vgn']
            vem = request.POST['vem']
            vpass = request.POST['vpass']
            vcon = request.POST['vcon']
            vimg = request.FILES.get('vimg')
            shimg = request.FILES.get('shimg')
            shnm = request.POST['shnm']
            shem = request.POST['shem']
            shcon = request.POST['shcon']
            shadd = request.POST['shadd']
            
            obj.v_name = vnm
            obj.v_gstno = vgn
            obj.email_id = vem
            request.session['vender_data'] = vem
            obj.password = vpass
            obj.contact = vcon
            if vimg != None:
                obj.profile = vimg
            if shimg != None:
                obj.shop_img = shimg
            obj.Shop_name = shnm
            obj.shop_address = shadd
            obj.shop_contact_no = shcon
            obj.shop_contact_em = shem
            obj.save()
            return redirect('Vender_Dashboard')
        return render(request,'Admin_templates/vendor_form.html',{'vdata':obj})
    else:
        return redirect('ved_login')   

def category_form(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        prods = category.objects.filter(venders=vender_data)
        return render(request,'Admin_templates/category_form.html',{'prods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login')        
    
def add_cate(request):    
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        if request.POST:
            cnm = request.POST['cnm']
            img = request.FILES.get('img')

            obj = category()
            obj.venders = vender_data
            obj.c_name = cnm
            obj.c_image = img
            obj.save()
            return redirect('category_form')
        return render(request,'Admin_templates/add_category_form.html',{'vdata':vender_data})
    else:
        return redirect('ved_login')        
    
def update_cate(request,id):    
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        obj = category.objects.get(venders=vender_data,id=id)
        if request.POST:
            cnm = request.POST['cnm']
            img = request.FILES.get('img')

            if img != None:
                obj.c_image = img
            obj.c_name = cnm
            
            obj.save()
            return redirect('category_form')
        return render(request,'Admin_templates/add_category_form.html',{'keys':obj,'vdata':vender_data})
    else:
        return redirect('ved_login')      

def delete_cate(request,id):    
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        obj = category.objects.get(id=id)
        obj.delete()
        return redirect('category_form')
    else:
        return redirect('ved_login')  

def sub_category_form(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        prods = Sub_category.objects.filter(venders=vender_data)
        return render(request,'Admin_templates/sub_category_form.html',{'prods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login')   

def vend_sub_category_form(request,id):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        cat = category.objects.get(id=id)
        prods = Sub_category.objects.filter(venders=vender_data,C_id=cat)
        return render(request,'Admin_templates/sub_category_form.html',{'venprods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login')   
    
def add_sub_category_form(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        cats = category.objects.filter(venders=vender_data)
        if request.POST:
            mcat = request.POST['mcat']
            snm = request.POST['snm']
            img = request.FILES.get('img')

            obj = Sub_category()
            obj.venders = vender_data
            obj.C_id = category.objects.get(id=int(mcat))
            obj.name = snm
            obj.Sc_image = img
            obj.save()
            return redirect('sub_category_form')
        return render(request,'Admin_templates/add_sub_category_form.html',{'cats':cats,'vdata':vender_data})
    else:
        return redirect('ved_login')

def update_sub_category_form(request,id):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        cats = category.objects.filter(venders=vender_data)
        obj = Sub_category.objects.get(id=id)
        if request.POST:
            mcat = request.POST['mcat']
            snm = request.POST['snm']
            img = request.FILES.get('img')

            obj.venders = vender_data
            obj.C_id = category.objects.get(id=int(mcat))
            obj.name = snm
            if img != None:
                obj.Sc_image = img
                
            obj.save()
            return redirect('sub_category_form')
        return render(request,'Admin_templates/add_sub_category_form.html',{'keys':obj,'cats':cats,'vdata':vender_data})
    else:
        return redirect('ved_login')

def delete_sub_category_form(request,id):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        obj = Sub_category.objects.get(id=id)
        obj.delete()
        return redirect('sub_category_form')
    else:
        return redirect('ved_login')

def product_form(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        prods = product.objects.filter(venders=vender_data)
        
        return render(request,'Admin_templates/product_form.html',{'prods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login') 

def ven_product_form(request,id):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        sc = Sub_category.objects.get(id=id)
        prods = product.objects.filter(venders=vender_data,sub_cate=sc)
        
        return render(request,'Admin_templates/product_form.html',{'venprods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login') 

def Add_product_form(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        prods = Sub_category.objects.filter(venders=vender_data)
        if request.POST:
            pnm = request.POST['pnm']
            pdis = request.POST['pdis']
            pprice = request.POST['pprice']
            psize = request.POST['psize']
            psk = request.POST['psk']
            img = request.FILES.get('img')
            scats = request.POST['scats']
            
            scates = Sub_category.objects.get(id=int(scats))
            
            obj = product()
            obj.venders = vender_data
            obj.cate = scates.C_id
            obj.sub_cate = scates
            obj.p_name = pnm
            obj.p_discription = pdis
            obj.p_price = pprice
            
            obj.size_id = psize
            obj.stock = psk
            obj.imgs = img
            obj.save()
            return redirect('product_form')
        return render(request,'Admin_templates/add_product_form.html',{'prods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login')  
    
def Update_product_form(request,id):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        prods = Sub_category.objects.filter(venders=vender_data)
        obj = product.objects.get(id=id)
        if request.POST:
            pnm = request.POST['pnm']
            pdis = request.POST['pdis']
            pprice = request.POST['pprice']
            psize = request.POST['psize']
            psk = request.POST['psk']
            img = request.FILES.get('img')
            scats = request.POST['scats']
            
            scates = Sub_category.objects.get(id=int(scats))
            
            obj.venders = vender_data
            obj.cate = scates.C_id
            obj.sub_cate = scates
            obj.p_name = pnm
            obj.p_discription = pdis
            obj.p_price = pprice
            
            obj.size_id = psize
            obj.stock = psk
            if img != None:
                obj.imgs = img
            obj.save()
            return redirect('product_form')
        return render(request,'Admin_templates/add_product_form.html',{'keys':obj,'prods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login')  

def Delete_product_form(request,id):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        obj = product.objects.get(id=id)
        obj.delete() 
        return redirect('product_form')
        return render(request,'Admin_templates/add_product_form.html',{'vdata':vender_data})
    else:
        return redirect('ved_login')  
    
def offer_form(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        prods = Offer.objects.all()
        
        return render(request,'Admin_templates/offer_form.html',{'prods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login') 

def Report_Data(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        oot = owner_order_table.objects.filter(owner=vender_data)
        
        return render(request,'Admin_templates/report.html',{'oot':oot,'vdata':vender_data})
    else:
        return redirect('ved_login')

def Add_Offers(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        prods = product.objects.all()
        if request.POST:
            prod = request.POST['prod']
            odate = request.POST['odate']
            oedate = request.POST['oedate']
            odic = request.POST['odic']

            obj = Offer()
            obj.venders = vender_data
            obj.P_id = product.objects.get(id=int(prod))
            obj. Start_date = odate
            obj.End_date =oedate
            obj.descr = odic
            obj.save()
            return redirect('offer_form')
        return render(request,'Admin_templates/add_offer_form.html',{'prods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login') 

def Update_Offers(request,id):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        prods = product.objects.all()
        obj = Offer.objects.get(id=id)
        if request.POST:
            prod = request.POST['prod']
            odate = request.POST['odate']
            oedate = request.POST['oedate']
            odic = request.POST['odic']

            obj.venders = vender_data
            obj.P_id = product.objects.get(id=int(prod))
            obj. Start_date = odate
            obj.End_date =oedate
            obj.descr = odic
            obj.save()
            return redirect('offer_form')
        return render(request,'Admin_templates/add_offer_form.html',{'keys':obj,'prods':prods,'vdata':vender_data})
    else:
        return redirect('ved_login') 

def Delete_Offers(request,id):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        obj = Offer.objects.get(id=id)
        obj.delete()
        return redirect('offer_form')
    else:
        return redirect('ved_login') 

def order_item_form(request):
    if "vender_data" in request.session.keys():
        Users = vendor.objects.get(email_id=request.session['vender_data'])
        otdata = owner_order_table.objects.filter(owner=Users)
        rec = set()
        for i in otdata:
            rec.add(i.order_id)
        rec = list(rec)
        rec.sort()
        return render(request,'Admin_templates/order_item_form.html',{'oids':rec,'vdata':Users})
    else:
        return redirect('ved_login') 

def VenderView_specific(request,Orids):
    if "vender_data" in request.session.keys():
        Users = vendor.objects.get(email_id=request.session['vender_data'])
        otdata = owner_order_table.objects.filter(owner=Users,order_id=Orids)
        status = ""
        for i in otdata:
            if i.cancel == True and i.deliver != True:
                status = "Canceled"
        
        tots = 0
        stats = set()
        for i in otdata:
            stats.add(i.deliver)
            tots += float(i.total)
        stats = list(stats)
        stats = stats[0]
        keys = False
        if stats == True:
            keys = True
        if request.POST:
            ids = request.POST['ids']
            stat = request.POST['stat']
            if stat == "Deliver":
                # obj = owner_order_table.objects.filter(order_id=Orids)
                for i in otdata:
                    i.deliver = True
                    i.payment = True
                    i.save()
                oids = order_table.objects.filter(order_id=Orids)
                for i in oids:
                    i.deliver = True
                    i.payment = True
                    i.save()
                keys = True
        return render(request,'Admin_templates/VenderBillPage.html',{'status':status,'keys':keys,'vdata':Users,'bilam':tots,'orders':otdata,'oids':Orids})
    else:
        return redirect('ved_login') 

def feedback_form(request):
    if "vender_data" in request.session.keys():
        Users = vendor.objects.get(email_id=request.session['vender_data'])
        if  request.POST:
            fmess =request.POST['fmess']
            fdate = request.POST['fdate']
            
            obj = feedback()
            obj.f_messge = fmess
            obj.f_date = fdate
            obj.save()
            return redirect('feedback_form')
        return render(request,'Admin_templates/feedback_form.html',{'vdata':Users})
    else:
        return redirect('ved_login') 

def message_task(request):
    return render(request,'Admin_templates/message-task.html')

    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def Shop_PDF(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        oot = owner_order_table.objects.filter(owner=vender_data)
        data = {'oot':oot,'vdata':vender_data}
        pdf = render_to_pdf('Admin_templates/GeneratePdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return redirect('ved_login')

def Shop_Excel(request):
    if "vender_data" in request.session.keys():
        vender_data = vendor.objects.get(email_id=str(request.session['vender_data']))
        oot = owner_order_table.objects.filter(owner=vender_data)    
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ReportData.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Customer', 'OrderId', 'Date',  'Products', 'QTY','Price', 'Total', 'payment', 'deliver', 'cancel']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = owner_order_table.objects.filter(owner=vender_data).values_list('cust__u_name', 'order_id', 'date', 'product', 'qty', 'price','total','payment','deliver','cancel')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)

        return response
        
    
    else:
        return redirect('ved_login')



