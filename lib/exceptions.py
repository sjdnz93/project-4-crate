from functools import wraps
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.response import Response
from django.core.exceptions import ImproperlyConfigured
from rest_framework import status

from records.models import Record
from reviews.models import Review

from django.contrib.auth import get_user_model
User = get_user_model()


def exceptions(func):
    @wraps(func)

    def wrapper(*args, **kwargs):
        try:
            print('WRAPPER FUNCTION EXECUTED, TRYING TO EXECUTE CONTROLLER')
            return func(*args, **kwargs)
        except (User.DoesNotExist, PermissionDenied) as e:
            print(e.__class__.__name__)
            print(e)
            return Response({ 'detail': 'Unauthorized' }, status.HTTP_401_UNAUTHORIZED)
        except (NotFound, Record.DoesNotExist, Review.DoesNotExist) as e:
            print(e.__class__.__name__)
            print(e)
            return Response(e.__dict__ if e.__dict__ else { 'detail': str(e) }, status.HTTP_404_NOT_FOUND)
        except (ValidationError, ImproperlyConfigured) as e:
            print(e.__class__.__name__)
            print(e)
            return Response(e.__dict__ if e.__dict__ else { 'detail': str(e) }, status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(e.__class__.__name__)
            print(e)
            return Response(e.__dict__ if e.__dict__ else str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            print('EXCEPTION OCCURRED')

    return wrapper        