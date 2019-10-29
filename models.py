import sqlite3

from peewee import *

db = SqliteDatabase('restraining-orders.db')

class RestrainingOrder(Model):
	case_number = CharField(primary_key=True)
	name = CharField()
	city = CharField(null=True)
	born = IntegerField(null=True)
	date_issued = DateField(null=True)
	date_served = DateField(null=True)
	attempted_serve = DateField(null=True)
	officer_notes = CharField(null=True)
	order_dismissed_on = DateField(null=True)
	order_expired_on = DateField(null=True)
	dismissal_reason = CharField(null=True)
	date_filed = DateField(null=True)
	race = CharField(null=True)
	county = CharField(null=True)
	url = CharField()
	html = TextField(null=True)
	class Meta:
		database = db

		
db.connect()
db.create_tables([RestrainingOrder])