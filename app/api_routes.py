from flask import request
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Event

api = Api()

class EventApi(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        search_query = request.args.get('q', default='', type=str)

        events = Event.query.filter(
            Event.title.ilike(f'%{search_query}%') |
            Event.description.ilike(f'%{search_query}%') |
            Event.location.ilike(f'%{search_query}%')
        ).all()

        event_data = [{
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date_time': event.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            'location': event.location,
            'organizer': {
                'id': event.organizer_id,
                'username': event.organizer.username,
                'email': event.organizer.email
            },
            'photo_filename': event.photo_filename
        } for event in events]

        return {'events': event_data}


api.add_resource(EventApi, '/api/events')

