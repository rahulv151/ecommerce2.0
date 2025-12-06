from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('view/<int:pid>', views.view, name='view'),
    path('cart/', views.cart, name='cart'),
    path('addcart/<int:pid>', views.add_cart, name='addcart'),
    path('removeCart/<int:pid>/', views.removeCart, name='removeCart'),
    path('search/',views.search,name='search'),
    path('range/',views.range,name="range"),
    path('watchList/',views.watchList,name="watchList"),
    path('laptopList/',views.laptopList,name="laptopList"),
    path('mobileList/',views.mobileList,name="mobileList"),
    path('sort/',views.sort,name="sort"),
    path('sorth/',views.sorth,name="sorth"),
    path('updateqty/<int:uval>/<int:pid>/',views.updatqty,name="updateqty"),
    path('register',views.register_user,name="register"),
    path('login',views.login_user,name="login"),
    path('logout',views.logout_user,name="logout"),
    path('viewOrder/',views.viewOrder,name="viewOrder"),
    path('payment/',views.makePayment,name="payment"),
    path('inserProd/',views.inserProduct,name="inserProd"),
]