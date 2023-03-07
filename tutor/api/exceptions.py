from rest_framework.exceptions import APIException

class NoTheme(APIException):
    status_code = 400
    default_detail = 'Debe proporcionar un tema para generar el ejercicio.'
    default_code = 'no_theme_provided'

class NoEjercicio(APIException):
    status_code = 404
    default_detail = 'No existen ejercicios para el tema.'
    default_code = 'no_exercises_found'

class NoID(APIException):
    status_code = 400
    default_detail = 'No se proporciono ID.'
    default_code = 'no_id_provided'

class NoAnswer(APIException):
    status_code = 400
    default_detail = 'No se proporciono respuesta.'
    default_code = 'no_answer_provided'

class NotMatch(APIException):
    status_code = 403
    default_detail = 'No esta asignado el ejercicio a este estudiante.'
    default_code = 'not_match'
