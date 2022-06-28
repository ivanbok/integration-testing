from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
import datetime

from .models import Categories, Benefits, Company, BenefitsProviderCompany, RedemptionHistory, User, EmployeeUser, \
    BusinessUser, BenefitsProviderUser, InternalStaffUser, TransactionHistory

from .serializers import CategoriesSerializer, BenefitsSerializer, CompanySerializer, BenefitsProviderCompanySerializer, \
    RedemptionHistorySerializer, UserSerializer, EmployeeUserSerializer, BusinessUserSerializer, \
        BenefitsProviderUserSerializer, InternalStaffUserSerializer, TransactionHistorySerializer

def index(request):
    return render(request, "benefits/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("store"))
        else:
            return render(request, "benefits/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "benefits/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    return render(request, "benefits/register.html")

def registeremployee(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        company = request.POST["company"]
        company = company.lower()
        employeeID = request.POST["employeeID"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "benefits/registeremployee.html", {
                "message": "Passwords must match."
            })

        # Ensure that Company Exists in Database
        num_companies = Company.objects.all().count()
        companyExists = False
        for id in range(1, num_companies + 1):
            SelectedCompany = Company.objects.get(id=str(id))
            if SelectedCompany.company_name == company:
                companyExists = True
                companyObject = SelectedCompany
                points = int(SelectedCompany.standard_points)
        if companyExists == False:
            return render(request, "benefits/registeremployee.html", {
                "message": "Company Does Not Exist."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password,\
                first_name=first_name, last_name=last_name, is_employee = True)
            user.save()
        except IntegrityError:
            return render(request, "benefits/registeremployee.html", {
                "message": "Username already taken."
            })
        employeeObject = EmployeeUser.objects.create(
            user = user,
            employeeID = employeeID,
            company = companyObject,
            points = points)
        employeeObject.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "benefits/registeremployee.html")

@csrf_exempt
@api_view(['POST'])
def registeremployeeapi(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        company = request.POST["company"]
        company = company.lower()
        employeeID = request.POST["employeeID"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            errorMessage = {"error": True, "message": "Passwords do not match. "}
            return Response(data=errorMessage, status=status.HTTP_200_OK)

        # Ensure that Company Exists in Database
        num_companies = Company.objects.all().count()
        companyExists = False
        for id in range(1, num_companies + 1):
            SelectedCompany = Company.objects.get(id=str(id))
            if SelectedCompany.company_name == company:
                companyExists = True
                companyObject = SelectedCompany
                points = int(SelectedCompany.standard_points)
        if companyExists == False:
            errorMessage = {"error": True, "message": "Company does not exist. "}
            return Response(data=errorMessage, status=status.HTTP_200_OK)
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password,\
                first_name=first_name, last_name=last_name, is_employee = True)
            user.save()
        except IntegrityError:
            errorMessage = {"error": True, "message": "Username already taken. "}
            return Response(data=errorMessage, status=status.HTTP_200_OK)
        employeeObject = EmployeeUser.objects.create(
            user = user,
            employeeID = employeeID,
            company = companyObject,
            points = points)
        employeeObject.save()
        login(request, user)
        successMessage = {"error": False, "message": "Account created. "}
        return Response(data=successMessage, status=status.HTTP_200_OK)



def registerbusiness(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        company = request.POST["company"]
        company = company.lower()
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "benefits/registerbusiness.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password,\
                first_name=first_name, last_name=last_name, is_business = True)
            user.save()
        except IntegrityError:
            return render(request, "benefits/registerbusiness.html", {
                "message": "Username already taken."
            })
        
        # Check if Company Exists in the Database, else add Company to Database
        num_companies = Company.objects.all().count()
        companyExists = False
        for id in range(1, num_companies + 1):
            SelectedCompany = Company.objects.get(id=str(id))
            if SelectedCompany.company_name == company:
                companyExists = True
                companyObject = SelectedCompany
        if companyExists == False:
            ## create company DB
            companyObject = Company.objects.create(
                company_name = company,
                standard_points = 1000)
            companyObject.save()

        # Create Business User
        businessUserObject = BusinessUser.objects.create(
            user = user,
            company = companyObject
        )
        businessUserObject.save
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "benefits/registerbusiness.html")

def registerprovider(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        providercompany = request.POST["providercompany"]
        providercompany = providercompany.lower()
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "benefits/registerprovider.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password,\
                first_name=first_name, last_name=last_name, is_serviceprovider = True)
            user.save()
        except IntegrityError:
            return render(request, "benefits/registerprovider.html", {
                "message": "Username already taken."
            })
        
        # Check if Provider Company Exists in the Database, else add Provider Company to Database
        num_providers = BenefitsProviderCompany.objects.all().count()
        providerExists = False
        for id in range(1, num_providers + 1):
            SelectedProvider = BenefitsProviderCompany.objects.get(id=str(id))
            if SelectedProvider.company_name == providercompany:
                providerExists = True
                providerObject = SelectedProvider
        if providerExists == False:
            ## create company DB
            providerObject = BenefitsProviderCompany.objects.create(
                company_name = providercompany)
            providerObject.save()

        # Create Provider User
        benefitsProviderUserObject = BenefitsProviderUser.objects.create(
            user = user,
            serviceCompany = providerObject
        )
        benefitsProviderUserObject.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "benefits/registerprovider.html")

@login_required
def availablebalance(request):
    is_employee = request.user.is_employee
    if is_employee:
        employeeUserObject = EmployeeUser.objects.get(user=request.user)
        availablePoints = employeeUserObject.points

        ## Optional: Format String Nicely (at the expense of loading speed)
        format_string = False
        if format_string:
            availablePoints = str(availablePoints)
            # Add comma to '000
            num_digits = len(availablePoints)
            first_digits = num_digits % 3
            if first_digits < num_digits:
                counter = 0
                availablePointsNew = ""
                for digit in availablePoints:
                    counter = counter + 1
                    availablePointsNew = availablePointsNew + digit
                    if (counter % 3 - first_digits) == 0 and (counter != num_digits):
                        availablePointsNew = availablePointsNew + ","
                availablePoints = availablePointsNew

        return JsonResponse({
            "availablePoints": availablePoints
        })
    else:
        availablePoints = "N/A"
        return JsonResponse({
            "availablePoints": availablePoints
        })


def store(request):
    if request.method == "POST":
        # View Category Selected
        categoryFilter = request.POST["category"]
    else:
        categoryFilter = "all"

    # Create Category Dropdown List
    categories = []
    categoriesQueryResponse = Categories.objects.all()
    for categoryObject in categoriesQueryResponse:
        categories.append(categoryObject.category)
    
    # Create List of Products
    benefitsList = []
    if categoryFilter == "all":
        benefitsQueryResponse = Benefits.objects.all()
    else:
        categoryObject = Categories.objects.get(category=categoryFilter)
        benefitsQueryResponse = Benefits.objects.filter(category=categoryObject)
    
    today = datetime.datetime.now()
    for benefitsObject in benefitsQueryResponse:
        if benefitsObject.is_active:
            benefitsDict = {}
            id = benefitsObject.id
            title = benefitsObject.title
            categoryObjectSpecific = benefitsObject.category
            category = categoryObjectSpecific.category
            providerObject = benefitsObject.provider
            provider = providerObject.company_name
            price = benefitsObject.price
            imageurl = benefitsObject.imageurl
            # Calculate Recency
            date_listed = benefitsObject.date_created
            date_listed = date_listed.replace(tzinfo=None)
            delta = today - date_listed
            recency = int(delta.days)
            benefitsDict = {"id": id, "title": title, "category": category,"provider": provider, "price": price, "imageurl": imageurl, "recency": recency}
            benefitsList.append(benefitsDict)

    # Sort Product List by Date
    benefitsList.sort(key = lambda benefitsDict : benefitsDict["recency"], reverse=True)

    # Return page regardless of whether it is post or get
    return render(request, "benefits/store.html", {
        "categories": categories,
        "selected": categoryFilter,
        "benefitsList": benefitsList
    })

def categoriesapi(request):
    if request.method == "GET":
        categoriesQueryResponse = Categories.objects.all()
        serializer = CategoriesSerializer(categoriesQueryResponse, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def storeapi(request):
    if request.method == "POST":
        # data = JSONParser().parse(request)
        # serializer = CategoriesSerializer(data=data)
        categoryFilter = request.POST["category"]
    else:
        categoryFilter = "all"

    # Create List of Products
    if categoryFilter == "all":
        benefitsQueryResponse = Benefits.objects.all()
    else:
        categoryObject = Categories.objects.get(category=categoryFilter)
        benefitsQueryResponse = Benefits.objects.filter(category=categoryObject)
    serializer = BenefitsSerializer(benefitsQueryResponse, many=True)
    return JsonResponse(serializer.data, safe=False)

@login_required
def addlisting(request):
    if request.user.is_authenticated:
        is_provider = request.user.is_serviceprovider
    if is_provider:
        # search for provider account details
        username = request.user.username
        BenefitsProviderUserObject = BenefitsProviderUser.objects.get(user=request.user)
        BenefitsProviderCompanyObject = BenefitsProviderUserObject.serviceCompany
        BenefitsProviderCompanyName = BenefitsProviderCompanyObject.company_name
    else: 
        BenefitsProviderCompanyName = ""
    
    if request.method == "POST":
        if is_provider:
            title = request.POST["title"]
            price = int(request.POST["price"])
            description = request.POST["description"]
            category = request.POST["category"] #need to convert to category object
            categoryObject = Categories.objects.filter(category=category).first()
            imageurl = request.POST["imageurl"]
            producttype = request.POST["producttype"]
            if producttype == "product":
                is_product = True
            else:
                is_product = False
            tags = request.POST["tags"]
            benefitsObject = Benefits.objects.create(
                title = title,
                description = description,
                category = categoryObject,
                posted_by = BenefitsProviderUserObject,
                provider = BenefitsProviderCompanyObject,
                price = price, 
                numberPurchased = 0,
                imageurl = imageurl,
                tags = tags,
                is_product = is_product,
                is_active = True
            )
            benefitsObject.save()
            return render(request, "benefits/index.html") #to change to generated listing page
        else:
            return render(request, "benefits/error.html", {
                "message": "You do not have permission to perform this action. This requires a service provider account. "
            })
    else:
        categories = []
        categories_set = Categories.objects.all()
        for categoryObject in categories_set:
            category = categoryObject.category
            categories.append(category)
        return render(request, "benefits/addlisting.html", {
            "is_provider": is_provider,
            "company_name": BenefitsProviderCompanyName,
            "categories": categories
        })

@login_required
def viewlisting(request, id):
    if request.method == "POST":
        if request.user.is_authenticated:
            is_employee = request.user.is_employee
            if is_employee:
                benefitsObject = Benefits.objects.get(id=id)
                employeeUserObject = EmployeeUser.objects.get(user=request.user)
                cartContentsString = employeeUserObject.cart
                cartContents = parseBenefitsList(cartContentsString)
                existingItem = False
                for cartIndex, cartObjectTuple in enumerate(cartContents):
                    if int(cartObjectTuple[0]) == int(id):
                        existingItem = True
                        quantity = cartObjectTuple[1]
                        quantity = quantity + 1
                        cartContents[cartIndex] = (id, quantity)
                if not existingItem:
                    cartObjectTuple = (id, 1)
                    cartContents.append(cartObjectTuple)
                cartContentsString = packageBenefitsList(cartContents)
                employeeUserObject.cart = cartContentsString
                employeeUserObject.save()
                return HttpResponseRedirect(reverse('cart'))
            else:
                return render(request, "benefits/error.html", {
                    "message": "You do not have permission to perform this action. This requires an employee account."
                })
    if request.method == "GET":
        benefitsObject = Benefits.objects.get(id=id)
        title = benefitsObject.title
        description = benefitsObject.description
        categoryObject = benefitsObject.category
        category = categoryObject.category
        BenefitsProviderUserObject = benefitsObject.posted_by
        BenefitsProviderCompanyObject = benefitsObject.provider
        provider_company_name = BenefitsProviderCompanyObject.company_name
        price = benefitsObject.price
        numberPurchased = benefitsObject.numberPurchased
        imageurl = benefitsObject.imageurl
        tagsString = benefitsObject.tags.strip()
        tags = []
        tagWord = ""
        if tagsString:
            for tagChar in tagsString:
                if tagChar == ",":
                    tags.append(tagWord.strip())
                    tagWord = ""
                else:
                    tagWord = tagWord + tagChar
            tags.append(tagWord.strip())

        is_active = benefitsObject.is_active
        if request.user.is_authenticated:
            is_employee = request.user.is_employee
            is_business = request.user.is_serviceprovider
            is_serviceprovider = request.user.is_serviceprovider
            is_ownstaff = request.user.is_serviceprovider
            return render(request, "benefits/viewlisting.html", {
                "title": title,
                "description": description,
                "category": category,
                "provider_company_name": provider_company_name,
                "price": price,
                "imageurl": imageurl,
                "tags": tags,
                "is_active": is_active,
                "is_employee": is_employee,
                "id": id
            })

@login_required
def cartquantity(request):
    is_employee = request.user.is_employee
    if is_employee:
        employeeUserObject = EmployeeUser.objects.get(user=request.user)
        cartContents = parseBenefitsList(employeeUserObject.cart)
        itemIDs = []
        itemQuantity = []
        for cartObjectTuple in cartContents:
            itemIDs.append(cartObjectTuple[0])
            itemQuantity.append(cartObjectTuple[1])
        return JsonResponse({
            "itemIDs": itemIDs,
            "itemQuantity": itemQuantity
        })

@login_required
def cart(request):
    if request.method == "POST": # linked to item quantity update in cart
        is_employee = request.user.is_employee
        if is_employee:
            employeeUserObject = EmployeeUser.objects.get(user=request.user)
            benefitsID = int(request.POST["itemID"])
            updatedQuantity = int(request.POST["quantity"])
            cartContents = parseBenefitsList(employeeUserObject.cart)
            for cartIndex, cartObjectTuple in enumerate(cartContents):
                if int(cartObjectTuple[0]) == benefitsID:
                    if updatedQuantity == 0:
                        cartContents.remove(cartContents[cartIndex])
                    else:
                        cartContents[cartIndex] = (cartObjectTuple[0], updatedQuantity)
            employeeUserObject.cart = packageBenefitsList(cartContents)
            employeeUserObject.save()
            return HttpResponseRedirect(reverse("cart"))
        else:
            return render(request, "benefits/error.html", {
                "message": "You do not have permission to perform this action. This requires an employee account."
            })
    else:
        is_employee = request.user.is_employee
        if is_employee:
            employeeUserObject = EmployeeUser.objects.get(user=request.user)
            availablePoints = employeeUserObject.points
            cartContents = parseBenefitsList(employeeUserObject.cart)
            cart = []
            total_cost = 0
            serialNumber = 0
            contains_product = False
            for cartObjectTuple in cartContents:
                cartObjectid = cartObjectTuple[0]
                quantity = cartObjectTuple[1]
                cartObject = Benefits.objects.get(id=cartObjectid)
                is_product = cartObject.is_product
                if is_product:
                    contains_product = True
                cartItem = {}
                serialNumber = serialNumber + 1
                evenSN = (serialNumber % 2 == 0)
                id = cartObject.id
                title = cartObject.title
                imageurl = cartObject.imageurl
                price = cartObject.price
                is_active = cartObject.is_active
                if is_active:
                    total_cost = total_cost + price * quantity
                cartItem = {"serialNumber": serialNumber, "quantity": quantity, "evenSN": evenSN, "id": id, "title": title, "imageurl": imageurl, "price": price, "is_active": is_active}
                cart.append(cartItem)
            
            # Check for remaining point balance and whether it is sufficient to place order
            remainingPoints = int(availablePoints - total_cost)
            sufficientPoints = True
            if remainingPoints < 0:
                sufficientPoints = False
            return render(request, "benefits/cart.html", {
                "cart": cart,
                "total_cost": total_cost,
                "availablePoints": availablePoints,
                "remainingPoints": remainingPoints,
                "sufficientPoints": sufficientPoints,
                "contains_product": contains_product
            })
        else:
            return render(request, "benefits/error.html", {
                "message": "Cart page is only applicable to employee users."
            })

@csrf_exempt
@api_view(['GET', 'POST'])
def cartapi(request, *args, **kwargs):
    is_employee = request.user.is_employee
    if request.method == "POST": # linked to item quantity update in cart
        is_employee = request.user.is_employee
        if is_employee:
            employeeUserObject = EmployeeUser.objects.get(user=request.user)
            benefitsID = int(request.POST["itemID"])
            updatedQuantity = int(request.POST["quantity"])
            cartContents = parseBenefitsList(employeeUserObject.cart)
            for cartIndex, cartObjectTuple in enumerate(cartContents):
                if int(cartObjectTuple[0]) == benefitsID:
                    if updatedQuantity == 0:
                        cartContents.remove(cartContents[cartIndex])
                    else:
                        cartContents[cartIndex] = (cartObjectTuple[0], updatedQuantity)
            employeeUserObject.cart = packageBenefitsList(cartContents)
            employeeUserObject.save()
            return Response(data="Success!", status=status.HTTP_200_OK)
        else:
            pass
    elif request.method == 'GET':
        if is_employee:
            employeeUserObject = EmployeeUser.objects.get(user=request.user)
            availablePoints = employeeUserObject.points
            cartContents = parseBenefitsList(employeeUserObject.cart)
            cart = []
            total_cost = 0
            serialNumber = 0
            contains_product = False
            for cartObjectTuple in cartContents:
                cartObjectid = cartObjectTuple[0]
                quantity = cartObjectTuple[1]
                cartObject = Benefits.objects.get(id=cartObjectid)
                is_product = cartObject.is_product
                if is_product:
                    contains_product = True
                cartItem = {}
                id = cartObject.id
                title = cartObject.title
                imageurl = cartObject.imageurl
                price = cartObject.price
                is_active = cartObject.is_active
                if is_active:
                    total_cost = total_cost + price * quantity
                cartItem = {"id": id, "quantity": quantity, "title": title, "imageurl": imageurl, "price": price, "is_active": is_active, "is_product": is_product}
                cart.append(cartItem)
            
            # Check for remaining point balance and whether it is sufficient to place order
            remainingPoints = int(availablePoints - total_cost)
            sufficientPoints = True
            if remainingPoints < 0:
                sufficientPoints = False
        else:
            pass #Return error
        return Response(data=cart, status=status.HTTP_200_OK)


@login_required
def checkout(request):
    if request.method == "POST":
        is_employee = request.user.is_employee
        if is_employee:
            contains_product = False
            employeeUserObject = EmployeeUser.objects.get(user=request.user)
            availablePoints = employeeUserObject.points
            cartContents = parseBenefitsList(employeeUserObject.cart)
            total_cost = 0

            cart = []
            transactionIDs = []
            total_cost = 0
            serialNumber = 0

            for cartObjectTuple in cartContents: 
                cartObjectid = cartObjectTuple[0]
                quantity = cartObjectTuple[1]
                cartObject = Benefits.objects.get(id=cartObjectid)
                if cartObject.is_active:
                    price = quantity * cartObject.price
                    total_cost = total_cost + price
                    if cartObject.is_product:
                        contains_product = True

            if contains_product:
                addressLineOne = request.POST["addressLineOne"]
                addressLineTwo = request.POST["addressLineTwo"]
                postalcode = request.POST["postalcode"]

            if availablePoints >= total_cost:
                # Get Employee List of Owned Benefits
                benefitsList = parseBenefitsList(employeeUserObject.benefits)
                for cartObjectTuple in cartContents:
                    cartObjectid = cartObjectTuple[0]
                    quantity = cartObjectTuple[1]
                    cartObject = Benefits.objects.get(id=cartObjectid)
                    if cartObject.is_active:
                        is_product = cartObject.is_product
                        alreadyOwned = False
                        # Transfer to owned benefits
                        for benefitsListIndex, benefitsTuple in enumerate(benefitsList):
                            if int(cartObjectTuple[0]) == int(benefitsTuple[0]):
                                alreadyOwned = True
                                quantity = int(cartObjectTuple[1]) + int(benefitsTuple[1])
                                benefitsList[benefitsListIndex] = benefitsTuple[0], quantity
                        
                        if not alreadyOwned:
                            benefitsList.append(cartObjectTuple)

                        # Record Items Purchased
                        cartItem = {}
                        serialNumber = serialNumber + 1
                        evenSN = (serialNumber % 2 == 0)
                        id = cartObject.id
                        title = cartObject.title
                        imageurl = cartObject.imageurl
                        price = cartObject.price
                        cartItem = {"serialNumber": serialNumber, "quantity": quantity, "evenSN": evenSN, "id": id, "title": title, "imageurl": imageurl, "price": price}
                        cart.append(cartItem)

                        # Remove from Employee's Cart
                        employeeUserObject.cart = ""
                        # Add purchase count to Benefit
                        cartObject.numberPurchased = cartObject.numberPurchased + 1
                        cartObject.save()
                        # Subtract Points from User
                        price = cartObject.price
                        availablePoints = availablePoints - price * quantity
                        # Log Transaction
                        listingID = cartObject
                        buyer = employeeUserObject
                        buyerCompany = employeeUserObject.company
                        seller = cartObject.provider
                        if is_product: 
                            transactionObject = TransactionHistory.objects.create(
                                listingID = listingID,
                                quantity = quantity,
                                addressLineOne = addressLineOne,
                                addressLineTwo = addressLineTwo,
                                postalcode = postalcode,
                                price = price,
                                buyer = buyer,
                                buyerCompany = buyerCompany,
                                seller = seller
                            )
                        else:
                            transactionObject = TransactionHistory.objects.create(
                                listingID = listingID,
                                quantity = quantity,
                                price = price,
                                buyer = buyer,
                                buyerCompany = buyerCompany,
                                seller = seller
                            ) 
                        transactionObject.save()
                        transactionIDs.append(transactionObject.id)
                employeeUserObject.points = availablePoints
                benefitsListString = packageBenefitsList(benefitsList)
                employeeUserObject.benefits = benefitsListString
                employeeUserObject.save()
                return render(request, "benefits/checkoutconfirmation.html", {
                    "cart": cart,
                    "total_cost": total_cost,
                    "availablePoints": availablePoints,
                    "transactionIDs": transactionIDs
                })
            else:
                return render(request, "benefits/error.html", {
                    "message": "You do not have sufficient balance to make this purchase."
                })
        else:
            return render(request, "benefits/error.html", {
                "message": "You do not have permission to perform this action. Please sign in with an employee account."
            })
    else:
        return render(request, "benefits/error.html", {
            "message": "You do not have permission to view this page. "
        })

@login_required
def viewbenefits(request):
    if request.method=="GET":
        is_employee = request.user.is_employee
        if is_employee:
            employeeUserObject = EmployeeUser.objects.get(user=request.user)
            benefitsTupleList = parseBenefitsList(employeeUserObject.benefits)
            benefitList = []
            serialNumber = 0
            for benefitsTuple in benefitsTupleList:
                benefitDict = {}
                benefit = Benefits.objects.get(id=int(benefitsTuple[0]))
                title = benefit.title
                description = benefit.description
                provider = benefit.provider
                imageurl = benefit.imageurl
                serialNumber = serialNumber + 1
                evenSN = (serialNumber % 2 == 0)
                quantity = benefitsTuple[1]
                benefitDict = {"id": int(benefitsTuple[0]), "title": title, "description": description, "provider": provider, "imageurl": imageurl, \
                    "serialNumber": serialNumber, "evenSN": evenSN , "quantity": quantity}
                benefitList.append(benefitDict)
            return render(request, "benefits/viewbenefits.html", {
                "benefitList": benefitList
            })
        else:
            return render(request, "benefits/error.html", {
                "message": "The purchased benefits page is only applicable to employee users."
        })

@login_required
def redeemitems(request):
    if request.method == "POST":
        is_employee = request.user.is_employee
        if is_employee:
            redeemtype = request.POST["redeemtype"]
            itemid = request.POST["itemid"]
            employeeUserObject = EmployeeUser.objects.get(user=request.user)
            benefitsTupleList = parseBenefitsList(employeeUserObject.benefits)
            quantityRedeemed = 0
            benefitsObject = Benefits.objects.get(id=int(itemid))
            for benefitsListIndex, benefitsTuple in enumerate(benefitsTupleList):
                if int(benefitsTuple[0]) == int(itemid):
                    if redeemtype == "all":
                        quantityRedeemed = benefitsTuple[1]
                        benefitsTupleList.remove(benefitsTuple)
                    elif redeemtype == "single":
                        quantity = int(benefitsTuple[1])
                        quantityRedeemed = 1
                        if quantity > 1:
                            new_quantity = quantity - 1
                            benefitsTupleList[benefitsListIndex] = (benefitsTuple[0], new_quantity)
                        else: 
                            benefitsTupleList.remove(benefitsTuple)
            benefitsString = packageBenefitsList(benefitsTupleList)
            employeeUserObject.benefits = benefitsString
            employeeUserObject.save()

            if quantityRedeemed > 0:
                #Log redemption
                listingID = benefitsObject
                buyer = employeeUserObject
                buyerCompany = employeeUserObject.company
                seller = benefitsObject.provider
                redemptionObject = RedemptionHistory.objects.create(
                    listingID = listingID,
                    quantityRedeemed = quantityRedeemed,
                    buyer = buyer,
                    buyerCompany = buyerCompany,
                    seller = seller
                )
                redemptionObject.save()
            return HttpResponseRedirect(reverse('viewbenefits'))
        else:
            return render(request, "benefits/error.html", {
                "message": "You do not have the appropriate credentials to perform this action."
            })
    else:
        return render(request, "benefits/error.html", {
                "message": "Invalid Request Type."
        })

@login_required
def redemptionhistory(request):
    is_employee = request.user.is_employee
    if is_employee:
        employeeUserObject = EmployeeUser.objects.get(user=request.user)
        redemptionHistoryObjects = RedemptionHistory.objects.filter(buyer=employeeUserObject)
        redemptionHistory = []
        serialNumber = len(redemptionHistoryObjects) + 1
        for redemptionHistoryObject in redemptionHistoryObjects:
            serialNumber = serialNumber - 1
            evenSN = (serialNumber % 2) == 0
            benefitsObject = redemptionHistoryObject.listingID
            title = benefitsObject.title
            description = benefitsObject.description
            quantityRedeemed = int(redemptionHistoryObject.quantityRedeemed)
            seller = redemptionHistoryObject.seller
            redemptionDateTime = redemptionHistoryObject.redemptionDateTime
            redemptionDateTimeString = redemptionDateTime.strftime("%d/%m/%Y")
            redemptionHistoryDict = {"serialNumber": serialNumber, "evenSN":evenSN ,"title": title, "description": description, "quantityRedeemed": quantityRedeemed, 
                "seller": seller, "redemptionDate": redemptionDateTimeString}
            redemptionHistory.append(redemptionHistoryDict)
        redemptionHistory.sort(key = lambda redemptionItem : redemptionItem["serialNumber"])
    return render(request, "benefits/redemptionhistory.html", {
        "redemptionHistory": redemptionHistory
    })

@login_required
def viewsales(request):
    if request.method == "POST":
        actionType = request.POST["actionType"]
        if actionType == "editlisting":
            benefitID = request.POST["benefitID"]
            return HttpResponseRedirect(reverse('editlisting', kwargs={'id': benefitID}))
        elif actionType == "resetSales":
            benefitID = request.POST["benefitID"]
            benefitsObject = Benefits.objects.get(id=benefitID)
            benefitsObject.numberPurchased = 0
            benefitsObject.save()
            return HttpResponseRedirect(reverse('viewsales'))
        elif actionType == "deactivate":
            benefitID = request.POST["benefitID"]
            benefitsObject = Benefits.objects.get(id=benefitID)
            benefitsObject.is_active = False
            benefitsObject.save()
            saved = True
            return HttpResponseRedirect(reverse('viewsales'))
        elif actionType == "activate":
            benefitID = request.POST["benefitID"]
            benefitsObject = Benefits.objects.get(id=benefitID)
            benefitsObject.is_active = True
            benefitsObject.save()
            saved = True
            return HttpResponseRedirect(reverse("viewsales"))
        else:
            return HttpResponseRedirect(reverse("viewsales"))
    else:
        is_serviceprovider = request.user.is_serviceprovider
        if is_serviceprovider:
            benefitsProviderUserObject = BenefitsProviderUser.objects.get(user=request.user)
            benefitsProviderCompanyObject = benefitsProviderUserObject.serviceCompany
            benefits = Benefits.objects.filter(provider=benefitsProviderCompanyObject)
            benefitList = []
            benefitListInactive = []
            serialNumberActive = 0
            serialNumberInactive = 0
            for benefit in benefits:
                benefitDict = {}
                id = benefit.id
                title = benefit.title
                description = benefit.description
                price = benefit.price
                numberPurchased = benefit.numberPurchased
                imageurl = benefit.imageurl
                is_active = benefit.is_active
                if is_active:
                    serialNumberActive = serialNumberActive + 1
                    serialNumber = serialNumberActive
                else:
                    serialNumberInactive = serialNumberInactive + 1
                    serialNumber = serialNumberInactive
                evenSN = (serialNumber % 2 == 0)
                benefitDict = {
                    "id": id, "title": title, "description": description, "price": price, "numberPurchased": numberPurchased, \
                    "imageurl": imageurl, "serialNumber": serialNumber, "evenSN": evenSN, "is_active": is_active
                }
                if is_active:
                    benefitList.append(benefitDict)
                else:
                    benefitListInactive.append(benefitDict)
            return render(request, "benefits/viewsales.html", {
                "benefitList": benefitList,
                "benefitListInactive": benefitListInactive
            })
        else:
            return render(request, "benefits/error.html", {
                "message": "The view sales page is only applicable to service providers."
            })

@login_required
def editlisting(request, id):
    if request.user.is_serviceprovider:
        BenefitsProviderUserObject = BenefitsProviderUser.objects.get(user=request.user)
        BenefitsProviderCompanyObject = BenefitsProviderUserObject.serviceCompany
        benefitsObject = Benefits.objects.get(id=id)
        benefitsObjectProvider = benefitsObject.provider
        # Validate that user has the authority to edit this listing
        if benefitsObjectProvider.id is BenefitsProviderCompanyObject.id:
            if request.method == "POST":
                pass
            else:
                # Extract Data of Benefits Object
                id = int(benefitsObject.id)
                title = benefitsObject.title
                description = benefitsObject.description
                categoryObject = benefitsObject.category
                selected_category = categoryObject.category
                price = benefitsObject.price
                imageurl = benefitsObject.imageurl
                tags = benefitsObject.tags
                is_active = benefitsObject.is_active

                # Extract Categories List
                categoriesQueryResponse = Categories.objects.all()
                categories = []
                for categoryObject in categoriesQueryResponse:
                    category = categoryObject.category
                    categories.append(category)
                return render(request, "benefits/editlisting.html", {
                    "id": id,
                    "title": title,
                    "description": description,
                    "price": price,
                    "imageurl": imageurl,
                    "tags": tags,
                    "categories": categories,
                    "selected_category": selected_category,
                    "is_active": is_active
                })
        else:
            return render(request, "benefits/error.html", {
                "message": "You do not have authority to edit this listing"
            })

@login_required
def viewemployees(request):
    if request.user.is_business:
        if request.method=="POST":
            pass
        else: 
            # Get Database of Employees
            businessUserObject = BusinessUser.objects.get(user=request.user)
            companyObject = businessUserObject.company
            employeeUserQueryResponse = EmployeeUser.objects.filter(company = companyObject)
            employeeList = []
            for employeeUserObject in employeeUserQueryResponse:
                employeeID = employeeUserObject.employeeID
                points = employeeUserObject.points
                benefits = employeeUserObject.benefits.all()
                for benefit in benefits:
                    title = benefit.title
                    id = benefit.id
                employeeDict = {"employeeID": benefits, "points": points}
                employeeList.append(employeeDict)
            return render(request, "benefits/viewemployees.html")
    else:
        return render(request, "benefits/error.html", {
            "message": "You do not have permission to view this page. Please sign in with a business account."
        })

def search(request):
    if request.method=="POST":
        searchString = request.POST["searchquery"]
        searchString = searchString.strip()
        searchStringOut = ""
        for searchChar in searchString:
            if searchChar.isalpha() or searchChar.isalpha():
                searchStringOut = searchStringOut + searchChar
            elif searchChar == " ":
                searchStringOut = searchStringOut + "+"
        return HttpResponseRedirect(reverse('searchresults', kwargs={'searchQuery': searchStringOut}))


def searchresults(request, searchQuery):
    searchString = ""
    searchList = []
    for searchChar in searchQuery:
        if searchChar.isalpha() or searchChar.isalpha():
            searchString = searchString + searchChar
        elif searchChar == "+":
            searchList.append(searchString.lower())
            searchString = ""
    searchList.append(searchString.lower())

    # Search Listings 
    ## Assign ranks (where higher is better)
    results_list = []
    benefitsQueryResponse = Benefits.objects.all()
    for benefitsObject in benefitsQueryResponse:
        resultDict = {}
        rank = 0
        include = False
        title = benefitsObject.title.lower()
        tags = benefitsObject.tags.lower()
        description = benefitsObject.description.lower()
        date_created = benefitsObject.date_created
        date_created = date_created.replace(tzinfo=None)
        for searchItem in searchList:
            if searchItem in title:
                include = True
                rank = rank + 5
            if searchItem in tags:
                include = True
                rank = rank + 3
            if searchItem in description:
                include = True
                rank = rank + 1
        if include:
            # Rank higher for more recent listings
            today = datetime.datetime.now()
            delta = today - date_created
            recency = (delta.days)/180
            recencyRank = 5 - int(recency)
            if recencyRank > 0:
                rank = rank + recencyRank
            # Create Result as Dictionary and add to List of Results
            resultDict = {"title": benefitsObject.title, "id": benefitsObject.id, "rank": rank, "description": description}
            results_list.append(resultDict)
        
    # Sort Results based on Rank
    results_list.sort(key = lambda resultDictItem : resultDictItem["rank"], reverse = True)
    return render(request, "benefits/searchresults.html", {
        "searchList": searchList,
        "results_list": results_list
    })

def parseBenefitsList(benefitsString):
    outputList = []
    tempEntry = ""
    tempTuple = ()
    is_id = True
    is_quantity = False
    idString = ""
    quantityString = ""

    for char in benefitsString:
        if char == "-":
            quantity = int(quantityString)
            quantityString = ""
            idString = ""
            tempEntry = ""
            is_id = True
            tempTuple = id, quantity
            outputList.append(tempTuple)
            tempTuple = ()
        elif char == ",":
            id = int(idString)
            is_id = False
            is_quantity = True
        else:
            if is_id:
                idString = idString + char
            elif is_quantity: 
                quantityString =  quantityString + char
    return outputList

def packageBenefitsList(benefitsList):
    benefitsString = ""
    for listItem in benefitsList: 
        id = str(listItem[0])
        quantity = str(listItem[1])
        benefitsString = benefitsString + id + "," + quantity + "-"
    return benefitsString





## To-Do List

## Completed
# 1. Create Page for Service Providers to Post Listing (DONE)
# 2. Create Listing Page (DONE)
# 3. Create Cart Page (DONE)
# 4. Create Checkout Confirmation Page: Show purchase summary (DONE)
# 5. Create a "My Benefits" page for employee users (DONE)
# 6. Create generic error page (DONE)
# 7. Create Search Function (DONE)
# 8. Show number of balance points user has on top right corner (likely use JavaScript API) (DONE)
# 9. Create Shop page (DONE)
# 10. Create Category Filter (DONE)
# 11. Update NavBar (DONE)
# 12. Run through code and generate error messages for each case when if-else criteria is not met (DONE)
# 13. Create page for service providers to look at their own listings and sales (DONE)
# 14. Allow service providers to modify their listing (DONE)

## To Do (Higher Priority)
# 15. Create page for businesses to view their employee data
# 16. Add redeem function: When they check out, they need to redeem the benefit (and show the service provider)
# 17. Add 2 different types of listings: One is a product, the other is a one-time service
# 18. Product: Do mailing (add address etc)

## To Do (Lower Priority)
# 16. Create page for Internal Staff or Service Providers to view Transaction Logs (lower priority)
# 17. Create Page for Company to Submit or Remove Valid Employees (using their ID) (lower priority)
# 18. Create page for Internal Staff with Admin privileges to create new staff accounts
# 19. Create page for users to modify their information
# 20. Create page to show service provider company profile and all their listings

## Optional (future improvements)
# Create a page to upload spreadsheets of a certain fixed format (upload list of valid employee IDs)
# Analytics tools/Dashboard for business to view their employee usage on aggregate basis