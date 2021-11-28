from django.db import models

class Area(models.Model):
    name =  models.CharField(default="",max_length=30)
    Pincode = models.CharField(default="",max_length=20)

class UsersData(models.Model):
    area = models.ForeignKey("Area",on_delete=models.CASCADE,blank=True,null=True)
    u_id = models.PositiveIntegerField(default=0,null=False)
    u_name = models.CharField(default="",max_length=30,null=False)
    email_id = models.CharField(default="",max_length=30,null=False)
    password = models.CharField(default="",max_length=20,null=False)
    contact = models.PositiveIntegerField(default=0,null=False)
    state = models.CharField(default="",max_length=15,null=False)
    country = models.CharField(default="", max_length=15, null=False)
    city = models.CharField(default="", max_length=15, null=False)
    address = models.TextField(default="")
    profile = models.ImageField(default="", upload_to="UserProfile/", max_length=400,blank=True,null=True)
    forgot_ans = models.CharField('Write Something Which Help You To Change Your Password',max_length=100,default='')

    def __str__(self):
        return self.u_name

class vendor(models.Model):
    v_name = models.CharField(default="", max_length=30, null=False)
    v_gstno = models.CharField(default="", null=False,max_length=100)
    email_id = models.CharField(default="", max_length=30, null=False)
    password = models.CharField(default="", max_length=20, null=False)
    contact = models.PositiveIntegerField(default=0, null=False)
    profile = models.ImageField(default="", upload_to="VenderProfile/", max_length=400,blank=True,null=True)
    shop_img = models.ImageField(default="", upload_to="VenderProfile/", max_length=400,blank=True,null=True)
    Shop_name = models.CharField(default="", max_length=100, null=False)
    shop_address = models.TextField(default="")
    shop_contact_no = models.CharField(default="", max_length=30, null=False)
    shop_contact_em = models.CharField(default="", max_length=30, null=False)

    def __str__(self):
        return self.Shop_name

class ModelChat_IDs(models.Model):
    chat_id = models.CharField(default="", max_length=100, null=False)
    usersData = models.ForeignKey("UsersData", default="",on_delete=models.CASCADE,blank=True, null=True)
    vendors = models.ForeignKey("vendor", default="",on_delete=models.CASCADE,blank=True, null=True)

class Models_Chats(models.Model):
    ch_ids = models.ForeignKey("ModelChat_IDs", default="",on_delete=models.CASCADE,blank=True, null=True)
    usersData = models.ForeignKey("UsersData", default="",on_delete=models.CASCADE,blank=True, null=True)
    vendors = models.ForeignKey("vendor", default="",on_delete=models.CASCADE,blank=True, null=True)
    problem_text = models.TextField(default="")
    date_time = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    

class order_table(models.Model):
    cust = models.ForeignKey("UsersData", on_delete=models.CASCADE)
    order_id = models.CharField(default='',max_length=100) 
    date = models.DateTimeField(auto_now=False,blank=True, null=True)
    img = models.ImageField(upload_to="orders/",default='')
    product = models.CharField(default='',max_length=300)
    qty = models.CharField(default='',max_length=100)
    price = models.CharField(default='',max_length=100)
    total = models.CharField(default='',max_length=100)
    payment = models.BooleanField(default=False)
    deliver = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)

    def __str__(self):
        return self.cust

class owner_order_table(models.Model):
    owner = models.ForeignKey("vendor", on_delete=models.CASCADE)
    cust = models.ForeignKey("UsersData", on_delete=models.CASCADE)
    order_id = models.CharField(default='',max_length=100) 
    date = models.DateTimeField(auto_now=False,blank=True, null=True)
    product = models.CharField(default='',max_length=300)
    qty = models.CharField(default='',max_length=100)
    price = models.CharField(default='',max_length=100)
    total = models.CharField(default='',max_length=100)
    payment = models.BooleanField(default=False)
    deliver = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product

class Owner_Payment(models.Model):
    Owner = models.ForeignKey("vendor", on_delete=models.CASCADE)
    Order_id = models.CharField(default='',max_length=100) 
    date = models.DateTimeField(auto_now=False,blank=True, null=True)
    Order_amount = models.CharField(default='',max_length=100)
    
    def __str__(self):
        return self.Order_id

class category(models.Model):
    venders = models.ForeignKey("vendor", on_delete=models.CASCADE,blank=True, null=True)
    c_name = models.CharField(default="", max_length=30, null=False)
    c_image = models.ImageField(default="", upload_to="Product_Cat/", max_length=400,blank=True,null=True)

    def __str__(self):
       return self.c_name

class Sub_category(models.Model):
    venders = models.ForeignKey("vendor", on_delete=models.CASCADE,blank=True, null=True)
    C_id = models.ForeignKey("category",on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(default="",max_length=20)
    Sc_image = models.ImageField(default="", upload_to="Product_sub_cat", max_length=400,blank=True,null=True)
    def __str__(self):
        return self.name
            
class product(models.Model):
    venders = models.ForeignKey("vendor", on_delete=models.CASCADE,blank=True, null=True)
    cate = models.ForeignKey("category", on_delete=models.CASCADE,blank=True, null=True)
    sub_cate = models.ForeignKey("Sub_category", on_delete=models.CASCADE,blank=True, null=True)
    p_name = models.CharField(default="", max_length=30, null=False)
    p_discription = models.TextField(default="")
    p_price = models.PositiveIntegerField(default=0, null=False)
    
    size_id = models.PositiveIntegerField(default=0, null=False)
    imgs = models.ImageField(upload_to="Product_imgs/",default="", max_length=400,blank=True,null=True)

    @staticmethod
    def get_products_by_id(ids):
        return product.objects.filter(id__in = ids)

    def __str__(self):
       return self.p_name
    class Meta:
        verbose_name_plural = "Services"

class feedbacks_of_product(models.Model):
    Product_name = models.ForeignKey("product", on_delete=models.CASCADE)
    cust = models.ForeignKey("UsersData", on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    rating = models.CharField(max_length=20,default = '1')
    feedback = models.TextField()
    def __str__(self):
       return self.cust
    class Meta:
        verbose_name_plural = "Services FeedBack"


class Offer(models.Model):
    venders = models.ForeignKey("vendor", on_delete=models.CASCADE,blank=True, null=True)
    Start_date = models.DateField(auto_now=False,blank=True,null=True)
    End_date = models.DateField(auto_now=False,blank=True,null=True)
    P_id = models.ForeignKey("product",on_delete=models.CASCADE,blank=True,null=True)
    descr = models.CharField(default="",max_length=200)


class Cart(models.Model):
    U_id = models.ForeignKey("UsersData",on_delete=models.CASCADE,blank=True,null=True)
    P_id = models.TextField(default="",blank=True, null=True)



class Order(models.Model):
    U_id = models.ForeignKey("UsersData",on_delete=models.CASCADE,blank=True,null=True)
    V_id = models.ForeignKey("vendor",on_delete=models.CASCADE,blank=True,null=True)
    Order_date = models.DateField(auto_now=False,blank=True,null=True)
    Contact_no = models.IntegerField(default=0)       


class Wishlist(models.Model):
    U_id = models.ForeignKey("UsersData",on_delete=models.CASCADE,blank=True,null=True)
    P_id = models.ForeignKey("product",on_delete=models.CASCADE,blank=True,null=True)


class Orderitem(models.Model):
    P_id = models.ForeignKey("product",on_delete=models.CASCADE,blank=True,null=True)
    Quantity = models.CharField(default="",max_length=100)
    Amount = models.CharField(default="",max_length=100)



class feedback(models.Model):
    U_id = models.ForeignKey("UsersData",on_delete=models.CASCADE,blank=True,null=True)
    P_id =models.ForeignKey("product",on_delete=models.CASCADE,blank=True,null=True)
    f_id = models.CharField(default="",max_length=100)
    f_date = models.DateField(auto_now=False,blank=True,null=True) 
    f_messge =  models.TextField(default="",max_length=400)
    def __str__(self):
	    return self.f_id



class Payment(models.Model):
    U_id =models.ForeignKey("UsersData",on_delete=models.CASCADE,blank=True,null=True)
    V_id =models.ForeignKey("vendor",on_delete=models.CASCADE,blank=True,null=True)
    P_mode =models.CharField(default="",max_length=100)
    p_date =models.DateField(auto_now=False,blank=True,null=True)
    P_amount =models.CharField(default="",max_length=20)


