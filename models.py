from bson import json_util
from mongoengine import connect, Document, StringField, BooleanField, ReferenceField, ListField, CASCADE

connect(db="hw08", host="mongodb+srv://userweb16:456789@cluster0.utgfjfb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)
    
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True, unique=True)
    sent = BooleanField(required=False)
    meta = {"collection": "contacts"}
