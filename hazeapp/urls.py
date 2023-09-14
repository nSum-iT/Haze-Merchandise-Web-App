from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.index, name="home"),

    path('store/Hoodie_Hunch/', views.store, name="store"),
	path('products/<str:name>/', views.product_details, name='product_detail'),


	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

	
    path('contact/', views.contact, name="contact"),
    path('faq/', views.faq, name="faq"),

	
    path('login/', views.loginUser, name="login"),
    path('register/', views.register, name="register"),
	path('logout/', views.logoutUser, name="logout"),


	path('account/', views.account, name="account"),

]