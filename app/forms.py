import phonenumbers as phonenumbers
from flask import current_app, flash
from flask_user import UserManager
from flask_user.forms import unique_email_validator, password_validator
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, BooleanField, SubmitField, validators, ValidationError, \
    SelectField
from wtforms.fields.html5 import DateField, EmailField
import pycountry

from app import models


class CountrySelectField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CountrySelectField, self).__init__(*args, **kwargs)
        self.choices = [(country.alpha_2, country.name) for country in pycountry.countries]


# noinspection PyBroadException,PyUnusedLocal
def validate_phone(form, field):
    """Validates a field for a valid phone number

    Args:
        form: REQUIRED, the field's parent form
        field: REQUIRED, the field with data

    Returns:
        None, raises ValidationError if failed
    """
    if len(field.data) > 16:
        raise ValidationError('Invalid phone number')
    try:
        input_number = phonenumbers.parse(field.data)
        if not (phonenumbers.is_valid_number(input_number)):
            raise ValidationError('Invalid phone number')
    except Exception:
        input_number = phonenumbers.parse('+1' + field.data)
        if not (phonenumbers.is_valid_number(input_number)):
            raise ValidationError('Invalid phone number')


# noinspection PyBroadException,PyUnusedLocal
def validate_subdivision(form, field):
    """Validates a field for a valid phone number

    Args:
        form: REQUIRED, the field's parent form
        field: REQUIRED, the field with data

    Returns:
        None, raises ValidationError if failed
    """
    #  TODO: check to see if subdivision is in selected country
    try:
        pycountry.subdivisions.lookup(field.data)
    except Exception:
        raise ValidationError(field.data + ' is not a State / Province / Region')


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
        validators.DataRequired('MSU E-Mail is required'),
    ])
    password = PasswordField('Password', validators=[
        validators.DataRequired('Password is required'),
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
        flash('Invalid E-Mail or Password', 'error')
        return False


class CustomRegisterForm(FlaskForm):
    """Registration form"""
    next = HiddenField()
    reg_next = HiddenField()

    # Login Info
    email = StringField('MSU E-Mail', validators=[
        validators.DataRequired(),
        validators.Email('Invalid email address'),
        unique_email_validator,
    ])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        password_validator
    ])
    retype_password = PasswordField('Retype Password', validators=[
        validators.EqualTo('password', message='Passwords did not match')
    ])

    # MSU Info
    net_id = StringField('NetID', validators=[
        validators.DataRequired()
    ])
    msu_id = StringField('MSU ID (9-digit WITH dashes)', validators=[
        validators.DataRequired(),
        validators.Regexp(r'^\d{3}-\d{3}-\d{3}$', message='Invalid 9-digit MSU ID, be sure to include dashes!')
    ])
    department = SelectField('Department',
                             choices=[('ACC', 'Accounting'),
                                      ('ASE', 'Aerospace Engineering'),
                                      ('AS', 'Aerospace Studies - AFROTC'),
                                      ('AAS', 'African American Studies'),
                                      ('AELC', 'Ag Educ,Leadership & Comm'),
                                      ('ABE', 'Ag. and Bio. Engineering'),
                                      ('AEC', 'Agricultural Economics'),
                                      ('AIS', 'Agricultural Info Sci & Ed'),
                                      ('AGN', 'Agronomy'),
                                      ('ADS', 'Animal Science & Dairy Science'),
                                      ('AN', 'Anthropology'),
                                      ('ALHP', 'Appalachian Ldshp Honors Prog'),
                                      ('AR', 'Archaeology'),
                                      ('ARC', 'Architecture'),
                                      ('ART', 'Art'),
                                      ('BAT', 'BAT Transfer Technical Course'),
                                      ('BCH', 'Biochemistry'),
                                      ('BIO', 'Biological Sciences'),
                                      ('BCS', 'Building Construction Science'),
                                      ('BUS', 'Business Adminstration'),
                                      ('BIS', 'Business Information Systems'),
                                      ('BL', 'Business Law'),
                                      ('BQA', 'Business Quantitive Analysis'),
                                      ('TKB', 'Business Technology'),
                                      ('BTE', 'Business Technology Education'),
                                      ('CHE', 'Chemical Engineering'),
                                      ('CH', 'Chemistry'),
                                      ('FLC', 'Chinese'),
                                      ('CE', 'Civil Engineering'),
                                      ('CFR', 'College of Forest Resources'),
                                      ('CO', 'Communication'),
                                      ('CCL', 'Community College Leadership'),
                                      ('CMB', 'Computational Biology'),
                                      ('CME', 'Computational Engineering'),
                                      ('CPE', 'Computer Engineering'),
                                      ('CSE', 'Computer Science & Engineering'),
                                      ('CP', 'Cooperative Education Program'),
                                      ('COR', 'Corrections'),
                                      ('COE', 'Counselor Education'),
                                      ('CRM', 'Criminology'),
                                      ('CA', 'Culinary Arts'),
                                      ('DSS', 'Disability Support Services'),
                                      ('EC', 'Economics'),
                                      ('EDC', 'Education Core Curriculum'),
                                      ('EDTB', 'Education Student Block'),
                                      ('EDST', 'Education Student Teaching'),
                                      ('EDF', 'Educational Foundations'),
                                      ('EDA', 'Educational Leadership (EDA)'),
                                      ('EDL', 'Educational Leadership (EDL)'),
                                      ('EPY', 'Educational Psychology'),
                                      ('ECE', 'Electrical & Computer Engineer'),
                                      ('EE', 'Electrical Engineering'),
                                      ('EDE', 'Elementary Education'),
                                      ('ENE', 'Engineering Education'),
                                      ('EG', 'Engineering Graphics'),
                                      ('EM', 'Engineering Mechanics'),
                                      ('EN', 'English'),
                                      ('ESL', 'English as Second Language'),
                                      ('EAP', 'English for Academic Purposes'),
                                      ('EPP', 'Entomology & Plant Pathology'),
                                      ('ENS', 'Environmental Science'),
                                      ('EP', 'Exercise Physiology'),
                                      ('EXL', 'Experiental Learning'),
                                      ('FDM', 'Fashion Design & Merchandising'),
                                      ('FIN', 'Finance'),
                                      ('FYE', 'First Year Experience'),
                                      ('FNH', 'Food, Nutrition & Health Promo'),
                                      ('FL', 'Foreign Languages'),
                                      ('FP', 'Forest Products'),
                                      ('FO', 'Forestry'),
                                      ('FLF', 'French'),
                                      ('GLA', 'Gen Liberal Arts'),
                                      ('GS', 'Gender Studies'),
                                      ('GA', 'General Agriculture'),
                                      ('GB', 'General Business'),
                                      ('GE', 'General Engineering'),
                                      ('GNS', 'Genetics'),
                                      ('GR', 'Geography'),
                                      ('GG', 'Geology'),
                                      ('FLG', 'German'),
                                      ('GRD', 'Graduate Studies'),
                                      ('FLH', 'Greek'),
                                      ('HCA', 'Healthcare Administration'),
                                      ('HED', 'Higher Education'),
                                      ('HI', 'History'),
                                      ('HON', 'Honors College'),
                                      ('HDFS', 'Human Development & Family Sci'),
                                      ('HS', 'Human Sciences'),
                                      ('IE', 'Industrial Engineering'),
                                      ('TKI', 'Industrial Technology'),
                                      ('INDT', 'Industrial Technology'),
                                      ('INS', 'Insurance & Risk Management'),
                                      ('IDS', 'Interdisciplinary Studies'),
                                      ('ID', 'Interior Design'),
                                      ('IB', 'International Business'),
                                      ('ISE', 'International Student Exchange'),
                                      ('FLI', 'Italian'),
                                      ('FLJ', 'Japanese'),
                                      ('KI', 'Kinesiology'),
                                      ('LA', 'Landscape Architecture'),
                                      ('FLL', 'Latin'),
                                      ('LSK', 'Learning Skills'),
                                      ('LIB', 'Library'),
                                      ('MGT', 'Management'),
                                      ('DTM', 'Manufacturing'),
                                      ('MKT', 'Marketing'),
                                      ('MA', 'Mathematics'),
                                      ('ME', 'Mechanical Engineering'),
                                      ('MIC', 'Microbiology'),
                                      ('MEC', 'Middle Eastern Culture'),
                                      ('MS', 'Military Science - Army ROTC'),
                                      ('MU', 'Music'),
                                      ('MUE', 'Music Education'),
                                      ('MUA', 'Music, Applied'),
                                      ('NSE', 'National Student Exchange'),
                                      ('NREC', 'Natural Resource & Envir Cons'),
                                      ('PTE', 'Petroleum Engineering'),
                                      ('PHI', 'Philosophy'),
                                      ('PE', 'Physical Education'),
                                      ('PAS', 'Physician Assistant Studies'),
                                      ('PH', 'Physics'),
                                      ('PHY', 'Physiology'),
                                      ('PSS', 'Plant and Soil Sciences'),
                                      ('PS', 'Political Science'),
                                      ('PO', 'Poultry Science'),
                                      ('PSY', 'Psychology'),
                                      ('PPA', 'Public Policy & Administration'),
                                      ('RDG', 'Readings in Education'),
                                      ('REF', 'Real Estate Finance'),
                                      ('REL', 'Religion'),
                                      ('FLR', 'Russian'),
                                      ('EDS', 'Secondary Education'),
                                      ('SL', 'Service Learning'),
                                      ('SW', 'Social Work'),
                                      ('SO', 'Sociology'),
                                      ('FLS', 'Spanish'),
                                      ('EDX', 'Special Education'),
                                      ('SS', 'Sport Studies'),
                                      ('ST', 'Statistics'),
                                      ('SLCE', 'Student Ldshp Comm Engagement'),
                                      ('SBP', 'Sustainable Bioproducts'),
                                      ('TECH', 'Technology'),
                                      ('DTF', 'Technology Foundations'),
                                      ('TKT', 'Technology Teacher Education'),
                                      ('TR', 'Transportation'),
                                      ('UHP', 'University Honors Program'),
                                      ('VTP', 'Veterans Transition Program'),
                                      ('CVM', 'Veterinary Medicine'),
                                      ('VS', 'Veterinary Science'),
                                      ('WFA', 'Wildlife,Fisheries, & Aquaculture'),
                                      ('WS', "Women's Studies")
                                      ],
                             validators=[
                                 validators.DataRequired(),
                             ])

    # Personal Info
    first_name = StringField('First name', validators=[
        validators.DataRequired()
    ])
    middle_name = StringField('Middle name', validators=[
        validators.DataRequired()
    ])
    last_name = StringField('Last name', validators=[
        validators.DataRequired()
    ])
    birth_date = DateField('Birth date', format='%Y-%m-%d', validators=[
        validators.DataRequired()
    ])
    pref_name = StringField('Prefered name (If different from first name)', validators=[
        validators.Optional()
    ])
    maiden_name = StringField('Maiden name (If Applicable)', validators=[
        validators.Optional()
    ])

    # Contact Info

    sec_email = StringField('Personal E-Mail (optional)', validators=[
        validators.Optional(),
        validators.Email('Invalid email address'),
        unique_email_validator
    ])
    prim_phone = StringField('Primary phone', validators=[
        validators.DataRequired(),
        validate_phone
    ])
    sec_phone = StringField('Secondary phone (optional)', validators=[
        validators.Optional(),
        validate_phone
    ])
    country = CountrySelectField('Country', validators=[
        validators.DataRequired(),
    ])
    administrative_area = StringField('State / Province / Region', validators=[
        validators.DataRequired(),
        validate_subdivision
    ])
    locality = StringField('City / Town', validators=[
        validators.DataRequired(),
    ])
    postal_code = StringField('Postal code / ZIP Code', validators=[
        validators.DataRequired(),
    ])
    thoroughfare = StringField('Street address', validators=[
        validators.DataRequired(),
    ])
    premise = StringField('Apartment, Suite, Box number, etc.', validators=[
        validators.Optional(),
    ])

    invite_token = HiddenField('Token')

    submit = SubmitField('Register')


class CustomEditUserProfileForm(FlaskForm):
    """Edit Profile Form form"""
    # MSU Info
    net_id = StringField('NetID', validators=[
        validators.DataRequired()
    ])
    msu_id = StringField('MSU ID (9-digit WITH dashes)', validators=[
        validators.DataRequired(),
        validators.Regexp(r'^\d{3}-\d{3}-\d{3}$', message='Invalid 9-digit MSU ID, be sure to include dashes!')
    ])
    department = SelectField('Department',
                             choices=[('ACC', 'Accounting'),
                                      ('ASE', 'Aerospace Engineering'),
                                      ('AS', 'Aerospace Studies - AFROTC'),
                                      ('AAS', 'African American Studies'),
                                      ('AELC', 'Ag Educ,Leadership & Comm'),
                                      ('ABE', 'Ag. and Bio. Engineering'),
                                      ('AEC', 'Agricultural Economics'),
                                      ('AIS', 'Agricultural Info Sci & Ed'),
                                      ('AGN', 'Agronomy'),
                                      ('ADS', 'Animal Science & Dairy Science'),
                                      ('AN', 'Anthropology'),
                                      ('ALHP', 'Appalachian Ldshp Honors Prog'),
                                      ('AR', 'Archaeology'),
                                      ('ARC', 'Architecture'),
                                      ('ART', 'Art'),
                                      ('BAT', 'BAT Transfer Technical Course'),
                                      ('BCH', 'Biochemistry'),
                                      ('BIO', 'Biological Sciences'),
                                      ('BCS', 'Building Construction Science'),
                                      ('BUS', 'Business Adminstration'),
                                      ('BIS', 'Business Information Systems'),
                                      ('BL', 'Business Law'),
                                      ('BQA', 'Business Quantitive Analysis'),
                                      ('TKB', 'Business Technology'),
                                      ('BTE', 'Business Technology Education'),
                                      ('CHE', 'Chemical Engineering'),
                                      ('CH', 'Chemistry'),
                                      ('FLC', 'Chinese'),
                                      ('CE', 'Civil Engineering'),
                                      ('CFR', 'College of Forest Resources'),
                                      ('CO', 'Communication'),
                                      ('CCL', 'Community College Leadership'),
                                      ('CMB', 'Computational Biology'),
                                      ('CME', 'Computational Engineering'),
                                      ('CPE', 'Computer Engineering'),
                                      ('CSE', 'Computer Science & Engineering'),
                                      ('CP', 'Cooperative Education Program'),
                                      ('COR', 'Corrections'),
                                      ('COE', 'Counselor Education'),
                                      ('CRM', 'Criminology'),
                                      ('CA', 'Culinary Arts'),
                                      ('DSS', 'Disability Support Services'),
                                      ('EC', 'Economics'),
                                      ('EDC', 'Education Core Curriculum'),
                                      ('EDTB', 'Education Student Block'),
                                      ('EDST', 'Education Student Teaching'),
                                      ('EDF', 'Educational Foundations'),
                                      ('EDA', 'Educational Leadership (EDA)'),
                                      ('EDL', 'Educational Leadership (EDL)'),
                                      ('EPY', 'Educational Psychology'),
                                      ('ECE', 'Electrical & Computer Engineer'),
                                      ('EE', 'Electrical Engineering'),
                                      ('EDE', 'Elementary Education'),
                                      ('ENE', 'Engineering Education'),
                                      ('EG', 'Engineering Graphics'),
                                      ('EM', 'Engineering Mechanics'),
                                      ('EN', 'English'),
                                      ('ESL', 'English as Second Language'),
                                      ('EAP', 'English for Academic Purposes'),
                                      ('EPP', 'Entomology & Plant Pathology'),
                                      ('ENS', 'Environmental Science'),
                                      ('EP', 'Exercise Physiology'),
                                      ('EXL', 'Experiental Learning'),
                                      ('FDM', 'Fashion Design & Merchandising'),
                                      ('FIN', 'Finance'),
                                      ('FYE', 'First Year Experience'),
                                      ('FNH', 'Food, Nutrition & Health Promo'),
                                      ('FL', 'Foreign Languages'),
                                      ('FP', 'Forest Products'),
                                      ('FO', 'Forestry'),
                                      ('FLF', 'French'),
                                      ('GLA', 'Gen Liberal Arts'),
                                      ('GS', 'Gender Studies'),
                                      ('GA', 'General Agriculture'),
                                      ('GB', 'General Business'),
                                      ('GE', 'General Engineering'),
                                      ('GNS', 'Genetics'),
                                      ('GR', 'Geography'),
                                      ('GG', 'Geology'),
                                      ('FLG', 'German'),
                                      ('GRD', 'Graduate Studies'),
                                      ('FLH', 'Greek'),
                                      ('HCA', 'Healthcare Administration'),
                                      ('HED', 'Higher Education'),
                                      ('HI', 'History'),
                                      ('HON', 'Honors College'),
                                      ('HDFS', 'Human Development & Family Sci'),
                                      ('HS', 'Human Sciences'),
                                      ('IE', 'Industrial Engineering'),
                                      ('TKI', 'Industrial Technology'),
                                      ('INDT', 'Industrial Technology'),
                                      ('INS', 'Insurance & Risk Management'),
                                      ('IDS', 'Interdisciplinary Studies'),
                                      ('ID', 'Interior Design'),
                                      ('IB', 'International Business'),
                                      ('ISE', 'International Student Exchange'),
                                      ('FLI', 'Italian'),
                                      ('FLJ', 'Japanese'),
                                      ('KI', 'Kinesiology'),
                                      ('LA', 'Landscape Architecture'),
                                      ('FLL', 'Latin'),
                                      ('LSK', 'Learning Skills'),
                                      ('LIB', 'Library'),
                                      ('MGT', 'Management'),
                                      ('DTM', 'Manufacturing'),
                                      ('MKT', 'Marketing'),
                                      ('MA', 'Mathematics'),
                                      ('ME', 'Mechanical Engineering'),
                                      ('MIC', 'Microbiology'),
                                      ('MEC', 'Middle Eastern Culture'),
                                      ('MS', 'Military Science - Army ROTC'),
                                      ('MU', 'Music'),
                                      ('MUE', 'Music Education'),
                                      ('MUA', 'Music, Applied'),
                                      ('NSE', 'National Student Exchange'),
                                      ('NREC', 'Natural Resource & Envir Cons'),
                                      ('PTE', 'Petroleum Engineering'),
                                      ('PHI', 'Philosophy'),
                                      ('PE', 'Physical Education'),
                                      ('PAS', 'Physician Assistant Studies'),
                                      ('PH', 'Physics'),
                                      ('PHY', 'Physiology'),
                                      ('PSS', 'Plant and Soil Sciences'),
                                      ('PS', 'Political Science'),
                                      ('PO', 'Poultry Science'),
                                      ('PSY', 'Psychology'),
                                      ('PPA', 'Public Policy & Administration'),
                                      ('RDG', 'Readings in Education'),
                                      ('REF', 'Real Estate Finance'),
                                      ('REL', 'Religion'),
                                      ('FLR', 'Russian'),
                                      ('EDS', 'Secondary Education'),
                                      ('SL', 'Service Learning'),
                                      ('SW', 'Social Work'),
                                      ('SO', 'Sociology'),
                                      ('FLS', 'Spanish'),
                                      ('EDX', 'Special Education'),
                                      ('SS', 'Sport Studies'),
                                      ('ST', 'Statistics'),
                                      ('SLCE', 'Student Ldshp Comm Engagement'),
                                      ('SBP', 'Sustainable Bioproducts'),
                                      ('TECH', 'Technology'),
                                      ('DTF', 'Technology Foundations'),
                                      ('TKT', 'Technology Teacher Education'),
                                      ('TR', 'Transportation'),
                                      ('UHP', 'University Honors Program'),
                                      ('VTP', 'Veterans Transition Program'),
                                      ('CVM', 'Veterinary Medicine'),
                                      ('VS', 'Veterinary Science'),
                                      ('WFA', 'Wildlife,Fisheries, & Aquaculture'),
                                      ('WS', "Women's Studies")
                                      ],
                             validators=[
                                 validators.DataRequired(),
                             ])

    # Personal Info
    first_name = StringField('First name', validators=[
        validators.DataRequired()
    ])
    middle_name = StringField('Middle name', validators=[
        validators.DataRequired()
    ])
    last_name = StringField('Last name', validators=[
        validators.DataRequired()
    ])
    birth_date = DateField('Birth date', format='%Y-%m-%d', validators=[
        validators.DataRequired()
    ])
    pref_name = StringField('Prefered name (If different from first name)', validators=[
        validators.Optional()
    ])
    maiden_name = StringField('Maiden name (If Applicable)', validators=[
        validators.Optional()
    ])

    # Contact Info

    sec_email = StringField('Personal E-Mail (optional)', validators=[
        validators.Optional(),
        validators.Email('Invalid email address'),
    ])
    prim_phone = StringField('Primary phone', validators=[
        validators.DataRequired(),
        validate_phone
    ])
    sec_phone = StringField('Secondary phone (optional)', validators=[
        validators.Optional(),
        validate_phone
    ])
    country = CountrySelectField('Country', validators=[
        validators.DataRequired(),
    ])
    administrative_area = StringField('State / Province / Region', validators=[
        validators.DataRequired(),
        validate_subdivision
    ])
    locality = StringField('City / Town', validators=[
        validators.DataRequired(),
    ])
    postal_code = StringField('Postal code / ZIP Code', validators=[
        validators.DataRequired(),
    ])
    thoroughfare = StringField('Street address', validators=[
        validators.DataRequired(),
    ])
    premise = StringField('Apartment, Suite, Box number, etc.', validators=[
        validators.Optional(),
    ])

    submit = SubmitField('Update')
