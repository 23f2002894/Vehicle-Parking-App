from flask_restful import Api, Resource, reqparse
from .models import *
from flask_security import auth_required, roles_required, roles_accepted, current_user
from .utils import *

api = Api()

class BookApi(Resource):
    def get(self):
        bookings = []
        bookings_json = []
        if "admin" in roles_list(current_user.roles):
            bookings = Bookings.query.all()