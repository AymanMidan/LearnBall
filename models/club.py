from datetime import datetime
from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.learnball
clubs = db.clubs

class Club:
    def __init__(self, name, country, city, coords, players, stadium, trophies,
                 continent, history, monument):
        self.name = name
        self.country = country
        self.city = city
        self.coords = coords
        self.players = players
        self.stadium = stadium
        self.trophies = trophies
        self.continent = continent
        self.history = history
        self.monument = monument

    def to_dict(self):
        return {
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'coords': self.coords,
            'players': self.players,
            'stadium': self.stadium,
            'trophies': self.trophies,
            'continent': self.continent,
            'history': self.history,
            'monument': self.monument
        }

    @staticmethod
    def from_dict(data):
        return Club(
            name=data.get('name'),
            country=data.get('country'),
            city=data.get('city'),
            coords=data.get('coords'),
            players=data.get('players'),
            stadium=data.get('stadium'),
            trophies=data.get('trophies'),
            continent=data.get('continent'),
            history=data.get('history'),
            monument=data.get('monument')
        )

    def save(self):
        return clubs.insert_one(self.to_dict())

    @staticmethod
    def get_all():
        return [Club.from_dict(club) for club in clubs.find()]

    @staticmethod
    def get_by_name(name):
        data = clubs.find_one({'name': name})
        return Club.from_dict(data) if data else None