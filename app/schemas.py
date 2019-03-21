from flask_marshmallow import Marshmallow
from .models import User, Notification, Submission, Revision, Review

ma = Marshmallow()


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class NotificationsSchema(ma.ModelSchema):
    class Meta:
        model = Notification


class SubmissionSchema(ma.ModelSchema):
    class Meta:
        model = Submission


class RevisionSchema(ma.ModelSchema):
    class Meta:
        model = Revision


class ReviewSchema(ma.ModelSchema):
    class Meta:
        model = Review
