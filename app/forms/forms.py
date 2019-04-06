from flask import current_app, flash
from flask_user import UserManager
from flask_user.forms import unique_email_validator, password_validator
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, BooleanField, SubmitField, validators, \
    SelectField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional, Length

from app import models
from app.forms.fields import DepartmentSelectField, CountrySelectField
from app.forms.validators import validate_phone, validate_subdivision


class CustomUserManager(UserManager):

    # noinspection PyAttributeOutsideInit
    def customize(self, app):
        self.LoginFormClass = CustomLoginForm
        self.RegisterFormClass = CustomRegisterForm
        self.EditUserProfileFormClass = CustomEditUserProfileForm


class CustomLoginForm(FlaskForm):
    """Login form"""
    next = HiddenField()
    reg_next = HiddenField()

    email = StringField('MSU E-Mail', validators=[
        DataRequired('MSU E-Mail is Required'),
    ])
    password = PasswordField('Password', validators=[
        DataRequired('Password is Required'),
    ])
    remember_me = BooleanField('Remember me')

    submit = SubmitField('Sign in')

    def __init_(self, *args, **kwargs):
        super(CustomLoginForm, self).__init_(*args, **kwargs)

    def validate(self):
        # grab the user manager
        user_manager = current_app.user_manager

        # handle invalid fields
        if not super(CustomLoginForm, self).validate():
            return False

        # find user by email
        user = user_manager.db_manager.db_adapter.ifind_first_object(models.User, email=self.email.data)

        # handle successful authentication
        if user and user_manager.verify_password(self.password.data, user.password):
            return True

        # unsuccessful authentication
        flash('Invalid email or password', 'error')
        return False


class CustomRegisterForm(FlaskForm):
    """Registration form"""
    next = HiddenField()
    reg_next = HiddenField()

    # Login Info
    email = StringField('MSU E-Mail', validators=[
        DataRequired(),
        validators.Email('Invalid email address'),
        unique_email_validator,
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        password_validator
    ])
    retype_password = PasswordField('Retype Password', validators=[
        validators.EqualTo('password', message='Passwords did not match')
    ])

    # MSU Info
    net_id = StringField('NetID', validators=[
        DataRequired()
    ])
    msu_id = StringField('MSU ID (9-digit WITH dashes)', validators=[
        DataRequired(),
        validators.Regexp(r'^\d{3}-\d{3}-\d{3}$', message='Invalid 9-digit MSU ID, be sure to include dashes!')
    ])
    department = DepartmentSelectField('Department', validators=[
        DataRequired()
    ])

    # Personal Info
    first_name = StringField('First name', validators=[
        DataRequired()
    ])
    middle_name = StringField('Middle name', validators=[
        DataRequired()
    ])
    last_name = StringField('Last name', validators=[
        DataRequired()
    ])
    birth_date = DateField('Date of Birth', format='%Y-%m-%d', validators=[
        DataRequired()
    ])
    pref_name = StringField('Prefered name (if different from first name)', validators=[
        Optional()
    ])
    maiden_name = StringField('Maiden name (if applicable)', validators=[
        Optional()
    ])

    # Contact Info

    sec_email = StringField('Personal email (Optional)', validators=[
        Optional(),
        validators.Email('Invalid email address'),
        unique_email_validator
    ])
    prim_phone = StringField('Primary phone', validators=[
        DataRequired(),
        validate_phone
    ])
    sec_phone = StringField('Secondary phone (Optional)', validators=[
        Optional(),
        validate_phone
    ])
    # address = FormField(CompleteAddressForm)
    thoroughfare = StringField('Street address', validators=[
        DataRequired(),
    ])
    premise = StringField('Apt/Suite/Box number', validators=[
        Optional(),
    ])
    locality = StringField('City/Town', validators=[
        DataRequired(),
    ])
    administrative_area = StringField('State/Province/Region', validators=[
        DataRequired(),
        validate_subdivision
    ])
    postal_code = StringField('ZIP/Postal code', validators=[
        DataRequired(),
    ])
    country = CountrySelectField('Country', validators=[
        DataRequired(),
    ])
    invite_token = HiddenField('Token')

    submit = SubmitField('Register')


class CustomEditUserProfileForm(FlaskForm):
    """Edit Profile Form form"""
    # MSU Info
    net_id = StringField('NetID', validators=[
        DataRequired()
    ])
    msu_id = StringField('MSU ID (9-digit WITH dashes)', validators=[
        DataRequired(),
        validators.Regexp(r'^\d{3}-\d{3}-\d{3}$', message='Invalid 9-digit MSU ID, be sure to include dashes!')
    ])
    department = DepartmentSelectField('Department', validators=[
        DataRequired()
    ])

    # Personal Info
    first_name = StringField('First name', validators=[
        DataRequired()
    ])
    middle_name = StringField('Middle name', validators=[
        DataRequired()
    ])
    last_name = StringField('Last name', validators=[
        DataRequired()
    ])
    birth_date = DateField('Date of birth', format='%Y-%m-%d', validators=[
        DataRequired()
    ])
    pref_name = StringField('Prefered name (if different from first name)', validators=[
        Optional()
    ])
    maiden_name = StringField('Maiden name (if applicable)', validators=[
        Optional()
    ])

    # Contact Info

    sec_email = StringField('Personal email (Optional)', validators=[
        Optional(),
        validators.Email('Invalid email address'),
    ])
    prim_phone = StringField('Primary phone', validators=[
        DataRequired(),
        validate_phone
    ])
    sec_phone = StringField('Secondary phone (Optional)', validators=[
        Optional(),
        validate_phone
    ])
    # address = FormField(CompleteAddressForm)

    thoroughfare = StringField('Street address', validators=[
        DataRequired(),
    ])
    premise = StringField('Apt/Suite/Box number', validators=[
        Optional(),
    ])
    locality = StringField('City/Town', validators=[
        DataRequired(),
    ])
    administrative_area = StringField('State/Province/Region', validators=[
        DataRequired(),
        validate_subdivision
    ])
    postal_code = StringField('ZIP/Postal code', validators=[
        DataRequired(),
    ])
    country = CountrySelectField('Country', validators=[
        DataRequired(),
    ])

    submit = SubmitField('Update')


class CreateSubmissionForm(FlaskForm):
    id = HiddenField()
    user_id = HiddenField()
    title = StringField('Title', validators=[
        DataRequired()
    ])
    abstract = TextAreaField('Abstract', validators=[
        DataRequired()
    ])

    type = SelectField('Document type', validators=[
        DataRequired()
    ], choices=[
        ('0', 'Master\'s Thesis'),
        ('1', 'Educational Specialist\'s Thesis'),
        ('2', 'Doctoral Disseration'),
    ])

    release = SelectField('Release type', validators=[
        DataRequired()
    ], choices=[
        ('0', 'Worldwide'),
        ('1', 'Restricted'),
        ('2', 'Embargo'),
    ])

    professor = StringField('Major Professor\'s NetID', validators=[
        DataRequired(),
        Length(max=8)
    ])

    years = SelectField('Restict time (if Restricted is selected)', validators=[
        DataRequired()
    ], choices=[
        ('0', ''),
        ('1', '1 year'),
        ('2', '2 years'),
        ('3', '3 years'),
    ])

    signature = FileField('Signature file', validators=[
        FileRequired(),
        FileAllowed(['pdf'], "PDF's only!")
    ])

    submit = SubmitField('Create Submission')


class CreateRevisionForm(FlaskForm):
    id = HiddenField()
    submission_id = HiddenField()

    file = FileField('Thesis or Dissertation file', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx'], ".pdf, .doc, or .docx only!")
    ])

    submit = SubmitField('Create Revision')


class CreateReviewForm(FlaskForm):
    id = HiddenField()
    revision_id = HiddenField()
    comments = TextAreaField('Comments', validators=[Optional()])
    check_1 = BooleanField('The Pages in Study needs to be updated on the abstract page.',
                           validators=[Optional()])
    check_2 = BooleanField('Chapter numbers should appear in Roman Numerals.',
                           validators=[Optional()])
    check_3 = BooleanField('The page after the copyright page is blank and should be removed',
                           validators=[Optional()])
    check_4 = BooleanField('Remove any signature lines that do not specify a committee member\'s name on the approval page.',
                           validators=[Optional()])
    check_5 = BooleanField('The student name on your dissertation and your ETD account should match.',
                           validators=[Optional()])
    check_6 = BooleanField('On the abstract page, there is a drop-down to “Select Appropriate Title”for your professor. Please choose the title for your professor from the drop-down.',
                           validators=[Optional()])
    check_7 = BooleanField('The title needs to be in sentence case, meaning only the first word is capitalized and any proper nouns. Please correct this throughout the paper and in your ETD account.',
                           validators=[Optional()])
    check_8 = BooleanField('Chapter 1 should start at page 1. To correct this go to the footer at Chapter 1 and go to Page Number, Format Page Number, and “Start at 1”. The update the table of contents, list of tables and figures and Pages in Study on the abstract.',
                           validators=[Optional()])
    check_9 = BooleanField('References need to be single spaced with a space in between.',
                           validators=[Optional()])
    check_10 = BooleanField('Figures/Tables need to be resized to fit in the margins. Review all figures/tables to make sure they fit in the margins. It is helpful to have the rulers and gridlines on in the View pane when resizing.',
                            validators=[Optional()])
    check_11 = BooleanField('Table needs to be resized to fit in margins.',
                            validators=[Optional()])
    check_12 = BooleanField('Chapter title pages should have a 2” top margin',
                            validators=[Optional()])
    check_13 = BooleanField('Third level headings in APA style should be contained “in the paragraph”. To correct this in the document, do the following:<ul><li>Type title of third (fourth or fifth) level heading. Start paragraph on same line as heading.</li><li>Place cursor on space before first letter of paragraph and choose “Heading in Paragraph” style.</li><li>Highlight title of heading and choose “3rd level heading” (or forth or fifth).</li></ul>',
                            validators=[Optional()])
    check_14 = BooleanField('The Appendix document should be on a separate page from the Appendix number and title page.',
                            validators=[Optional()])
    check_15 = BooleanField('The sublevel headings are not connected to the styles, so the sub-level heading are not appearing as they should. Please open the style pane and click on the sublevel headings and appropriate style. The update the table of contents.',
                            validators=[Optional()])
    check_16 = BooleanField('The word CHAPTER is missing from the table of contents. To be able to see the code that populates that word, go to File, Options, Display, and click on hidden texts. Then pull up the template and copy and paste the code (it appears after the word CHAPTER I) into your document. The update the Table of contents and the word Chapter should appear.',
                            validators=[Optional()])
    check_17 = BooleanField('There need to be 1” left and right margins on the landscape pages.',
                            validators=[Optional()])
    check_18 = BooleanField('The titles need to be on the same page as the table or image.',
                            validators=[Optional()])
    check_19 = BooleanField('The tables/figures are not connected to the styles, so the List of Tables/List of Figures is not populating correcting. To connect them just click the table/figure title and in the style pane, click table title/figure title. You will know they are connected when a blue rectangular box appears around the correct style in the style pane. The update your List of Tables/List of Figures and they should appear.',
                            validators=[Optional()])
    check_20 = BooleanField('Need to separate figure titles, from figure notes.',
                            validators=[Optional()])
    check_21 = BooleanField('Need to separate table titles, from table notes.',
                            validators=[Optional()])
    check_22 = BooleanField('Some paragraphs are indented and others aren’t. This needs to be consistent throughout the document.',
                            validators=[Optional()])
    check_23 = BooleanField('If a table is continued on another page, it needs to say “Table ____ (continued)” above the table on the subsequent pages.',
                            validators=[Optional()])
    check_24 = BooleanField('There is an extra page at the end on the document that need to be removed.',
                            validators=[Optional()])
    check_25 = BooleanField('Reduce Abstract to 150 words for Thesis or 350 for Dissertation.',
                            validators=[Optional()])
    check_26 = BooleanField('Removed signed signature page. This page should has no signatures',
                            validators=[Optional()])
    check_27 = BooleanField('Begin chapter on “Chapter” page.',
                            validators=[Optional()])
    check_28 = BooleanField('Center Appendix A title page vertically and horizontally on the page.',
                            validators=[Optional()])
    check_29 = BooleanField('Chapter titles need to be all capitalized.',
                            validators=[Optional()])
    check_30 = BooleanField('Removed unused committee signature lines.',
                            validators=[Optional()])
    check_31 = BooleanField('Check Graduation Date in Abstract',
                            validators=[Optional()])
    check_32 = BooleanField('Missing “Chapter” page __.',
                            validators=[Optional()])

    submit = SubmitField('Submit Review')
