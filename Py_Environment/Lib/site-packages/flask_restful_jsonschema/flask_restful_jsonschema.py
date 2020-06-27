import jsonschema
import flask
import flask_restful


def get_valid_json_or_abort(schema):
    """Either return the request's JSON, which
    matches the supplied JSON `schema`.

    Arguments:
        schema (dict): See jsonschema Python package.

    Aborts:
        400: The request does not adhere to the schema.

    Returns:
        JSON: JSON that fits the supplied `schema`.

    """

    json_request = flask.request.get_json(force=True)

    try:
        jsonschema.validate(json_request, schema)
    except jsonschema.ValidationError as e:
        flask_restful.abort(400, message=e.message)
    else:
        return json_request


def validate_json(func):
    """Decorator specifically for wrapping flask_restful
    Resource method... methods (get/post/put, etc.).

    """

    # get the function name because we're going to
    # see if we need SCHEMA_POST, SCHEMA_GET, etc.
    function_name = func.__name__.upper()

    def wrapped_func(self, *args, **kwargs):
        respective_schema = getattr(self, 'SCHEMA_' + function_name)
        json_request = get_valid_json_or_abort(respective_schema)
        return func(self, json_request, *args, **kwargs)

    return wrapped_func
