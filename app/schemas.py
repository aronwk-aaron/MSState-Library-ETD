from flask_marshmallow.sqla import ModelSchema
from app import ma
from .models import User, Notification, Submission, Revision, Review


class UserSchema(ModelSchema):
    class Meta:
        model = User


class NotificationsSchema(ModelSchema):
    class Meta:
        model = Notification


class SubmissionSchema(ModelSchema):
    class Meta:
        model = Submission


class RevisionSchema(ModelSchema):
    class Meta:
        model = Revision


class ReviewSchema(ModelSchema):
    class Meta:
        model = Review
