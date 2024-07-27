from flask import Blueprint, render_template, request
from models import recommend_by_place_name

views = Blueprint('views', __name__)


@views.route('/')
def home():
    # get name of place from get request
    place_name = request.args.get('name', '')
    start = int(request.args.get('start', 0))
    print(start)
    end = start+8
    
    if place_name:
        recommendations = recommend_by_place_name(place_name, start=start, end=end)
    else:
        recommendations = ['Not Found']

    return render_template('index.html', recommendations=recommendations, place_name=place_name, prev=start-8, next=start+8)