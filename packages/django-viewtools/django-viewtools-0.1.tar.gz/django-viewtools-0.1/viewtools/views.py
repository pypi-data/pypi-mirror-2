from django.db import connection as db


def py_error(request):
    raise ValueError("This is an error")


def db_error(request):
    c = db.cursor()
    c.execute("select * from asotuhaosetuhaosethuasote")
