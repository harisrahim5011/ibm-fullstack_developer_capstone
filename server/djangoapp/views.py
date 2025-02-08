from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse
import logging
import json
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
from .populate import initiate

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create a `login_request` view to handle sign in request
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}

    if user is not None:
        login(request, user)
        response_data["status"] = "Authenticated"
    return JsonResponse(response_data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


# Create a `registration` view to handle sign up request
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    try:
        User.objects.get(username=username)
        return JsonResponse(
            {"userName": username, "error": "Already Registered"}
        )
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        return JsonResponse(
            {"userName": username, "status": "Authenticated"}
        )


def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})


# Update the `get_dealerships` render list of dealerships
def get_dealerships(request, state="All"):
    endpoint = (
        "/fetchDealers"
        if state == "All"
        else f"/fetchDealers/{state}"
    )
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        for review_detail in reviews:
            sentiment = analyze_review_sentiments(
                review_detail['review']
            )
            review_detail['sentiment'] = sentiment['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    return JsonResponse({"status": 400, "message": "Bad Request"})


def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            logger.error(
                f"Error in posting review: {e}"
            )
            return JsonResponse(
                {"status": 401, "message": "Error in posting review"}
            )
    return JsonResponse({"status": 403, "message": "Unauthorized"})
    
