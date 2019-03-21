from flask_marshmallow import Marshmallow
from flask_marshmallow.sqla import ModelSchema

from .models import User, Notifications, Submission, Revision, Review

ma = Marshmallow()


class UserSchema(ModelSchema):
    class Meta:
        model = User


class NotificationsSchema(ModelSchema):
    class Meta:
        model = Notifications


class SubmissionSchema(ModelSchema):
    class Meta:
        model = Submission


class RevisionSchema(ModelSchema):
    class Meta:
        model = Revision


class ReviewSchema(ModelSchema):
    class Meta:
        model = Review
