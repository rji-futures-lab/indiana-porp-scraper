import sqlite3

from peewee import *

db = SqliteDatabase('restraining-orders.db')

class RestrainingOrder(Model):
	case_number = CharField()
	name = CharField()
	city = CharField()
	born = IntegerField(null=True)
	date_issued = DateField()
	date_served = DateField(null=True)
	attempted_serve = DateField(null=True)
	officer_notes = CharField(null=True)
	order_dismissed_on = DateField(null=True)
	order_expired_on = DateField(null=True)
	dismissal_reason = CharField(null=True)
	date_filed = DateField()
	race = CharField()
	county = CharField()
	url = CharField()
	html = TextField()
	class Meta:
		database = db

		
db.connect()
db.create_tables([RestrainingOrder])