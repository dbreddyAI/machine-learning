'''@validate_password

This file contains functions for validating the user's password against
a set of requirements.

'''

from flask import current_app
import yaml


def load_min(app=True, root='/vagrant'):
    '''@load_min

    This method returns the minimum character requirement for passwords.

    @app, indicates if function is to be used by application, or manually

    '''
    if app:
        min_c = current_app.config.get('PASSWORD_MIN_C')
        return {'password_min_c': min_c, 'error': None}
    else:
        with open(root + "/hiera/settings.yaml", 'r') as stream:
            try:
                min_c = \
                       yaml.load(stream)['validate_password']['password_min_c']
                return {'password_min_c': min_c, 'error': None}
            except yaml.YAMLError as error:
                return {'password_min_c': None, 'error': error}


def load_max(app=True, root='/vagrant'):
    '''@load_max

    This method returns the maximum character requirement for passwords.

    @app, indicates if function is to be used by application, or manually

    '''
    if app:
        max_c = current_app.config.get('PASSWORD_MAX_C')
        return {'password_max_c': max_c, 'error': None}
    else:
        with open(root + "/hiera/settings.yaml", 'r') as stream:
            try:
                max_c = \
                       yaml.load(stream)['validate_password']['password_max_c']
                return {'password_max_c': max_c, 'error': None}
            except yaml.YAMLError as error:
                return {'password_max_c': None, 'error': error}


def req_min_c(password):
    '''@req_min_c

    This method returns True if the minimum password character requirement is
    met.

    @password, is the password to be validated

    '''
    min_c = load_min(app=False)['password_min_c']
    min_c = 10 if min_c is None else min_c
    return len(password) >= min_c


def req_max_c(password):
    '''@req_max_c

    This method returns True if the maximum password character requirement is
    met.

    @password, is the password to be validated

    '''
    max_c = load_max(app=False)['password_max_c']
    max_c = 64 if max_c is None else max_c
    return len(password) <= max_c


def req_numeral(password):
    '''@req_numeral

    This method returns True if the password contains a number.

    @password, is the password to be validated

    '''
    numerals = '0123456789'
    return any(map(lambda n: n in password, list(numerals)))


def req_lower(password):
    '''@req_lower

    This method returns True if the password contains a lowercase letter.

    @password, is the password to be validated

    '''
    lowers = 'abcdefghijklmnopqrstuvwxyz'
    return any(map(lambda a: a in password, list(lowers)))


def req_upper(password):
    '''@req_upper

    This method returns True if the password contains an uppercase letter.

    @password, is the password to be validated

    '''
    uppers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    return any(map(lambda a: a in password, list(uppers)))


def validate_password(password):
    '''@validate_password

    This method returns True if the password meets all requirements.

    @password, is the password to be validated

    '''
    return req_min_c(password) and req_max_c(password) and \
        req_numeral(password) and (req_lower(password) or
            req_upper(password))
