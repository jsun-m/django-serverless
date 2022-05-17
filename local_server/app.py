import importlib


from flask import Flask, request, abort, Response

from modules.flask_optional_routes import OptionalRoutes


app = Flask(__name__)
opt_app = OptionalRoutes(app)

@opt_app.routes("/<function_name>/<action_method>?", methods=["POST"])
def _route(function_name, action_method=None):
    test_event = request.get_json()
    if not test_event:
        test_event = {}

    test_event["headers"] = request.headers

    url_path = function_name.replace("-", "_")
    if action_method:
        action_method = action_method.replace("-", "_")
    test_context = {}

    try:
        module_path = f"functions.{url_path}.handler"
        print(module_path)
        handler_module = importlib.import_module(module_path)
    except ModuleNotFoundError:
        abort(404)

    response = handler_module.handler(test_event, test_context, action_method)
    return Response(
        response["body"], status=response["statusCode"], mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
