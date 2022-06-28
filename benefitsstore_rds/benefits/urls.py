from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("registeremployee",views.registeremployee, name="registeremployee"),
    path("registeremployeeapi",views.registeremployeeapi, name="registeremployeeapi"),
    path("registerbusiness",views.registerbusiness, name="registerbusiness"),
    path("registerprovider",views.registerprovider, name="registerprovider"),
    path("availablebalance",views.availablebalance, name="availablebalance"),
    path("cartquantity",views.cartquantity, name="cartquantity"),
    path("store", views.store, name="store"),
    path("categoriesapi", views.categoriesapi, name="categoriesapi"),
    path("storeapi", views.storeapi, name="storeapi"),
    path("addlisting",views.addlisting, name="addlisting"),
    path("viewlisting/<str:id>/", views.viewlisting, name="viewlisting"),
    path("cart",views.cart, name="cart"),
    path("cartapi",views.cartapi, name="cartapi"),
    path("checkout",views.checkout, name="checkout"),
    path("viewbenefits",views.viewbenefits, name="viewbenefits"),
    path("redeemitems",views.redeemitems, name="redeemitems"),
    path("redemptionhistory",views.redemptionhistory, name="redemptionhistory"),
    path("viewsales", views.viewsales, name="viewsales"),
    path("editlisting/<str:id>/", views.editlisting, name="editlisting"),
    path("viewemployees", views.viewemployees, name="viewemployees"),
    path("search/", views.search, name="search"),
    path("searchresults/<str:searchQuery>/", views.searchresults, name="searchresults")
]
