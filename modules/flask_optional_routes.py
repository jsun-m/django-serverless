# Optional routes found here https://github.com/sudouser2010/flask_optional_routes
import copy

class RouteBranch:

    def __init__(self):
        self.string = ''

    def append_new_route_segment(self, segment):
        self.string = '{}/{}'.format(self.string, segment)

class RouteBranchManager:

    def __init__(self):
        first_branch = RouteBranch()
        self.route_branches = [first_branch]

    def get_copy_of_preexisting_branches(self):
        return copy.deepcopy(self.route_branches)

    def add_segment_to_all_branches(self, segment):
        for route_branch in self.route_branches:
            route_branch.append_new_route_segment(segment)

    def add_new_branches_to_route_branches(self, new_branches):
        self.route_branches.extend(new_branches)

    def add_segment_to_a_copy_of_all_branches(self, segment):
        copy_of_preexisting_route_branches = self.get_copy_of_preexisting_branches()

        for route_branch in copy_of_preexisting_route_branches:
            route_branch.append_new_route_segment(segment)
        self.add_new_branches_to_route_branches(copy_of_preexisting_route_branches)

    def get_route_strings(self):
        routes = [route_branch.string for route_branch in self.route_branches]
        return routes

class OptionalRoutes:
    def __init__(self, app, delimiter='?'):
        self.app = app
        self.delimiter = delimiter

    def segment_ends_with_option_delimiter(self, segment):
        if segment == '':
            return False

        last_character_in_segment = segment[-1]
        return last_character_in_segment == self.delimiter

    def get_segment_without_delimiter(self, segment):
        delimiter_lenth = len(self.delimiter)
        return segment[:-delimiter_lenth]

    def remove_starting_slash(self, route):
        return route[1:]

    def route_starts_with_forward_slash(self, route):
        first_character = route[0]
        return first_character == '/'

    def validate_route(self, route):
        assert self.route_starts_with_forward_slash(route), 'Route does not start with forward slash'

    def generate_optional_routes(self, route):

        self.validate_route(route)
        route = self.remove_starting_slash(route)
        route_segments = route.split('/')
        route_manager = RouteBranchManager()

        for segment in route_segments:
            if self.segment_ends_with_option_delimiter(segment):
                segment_without_delimiter = self.get_segment_without_delimiter(segment)
                route_manager.add_segment_to_a_copy_of_all_branches(segment_without_delimiter)
            else:
                route_manager.add_segment_to_all_branches(segment)

        routes = route_manager.get_route_strings()
        return routes

    def routes(self, rule, **options):
        """A decorator that is used to register a view function for a
        given URL rule.  This does the same thing as :meth:`add_url_rule`
        but is intended for decorator usage::
            @app.route('/')
            def index():
                return 'Hello World'
        For more information refer to :ref:`url-route-registrations`.
        :param rule: the URL rule as string
        :param endpoint: the endpoint for the registered URL rule.  Flask
                         itself assumes the name of the view function as
                         endpoint
        :param options: the options to be forwarded to the underlying
                        :class:`~werkzeug.routing.Rule` object.  A change
                        to Werkzeug is handling of method options.  methods
                        is a list of methods this rule should be limited
                        to (``GET``, ``POST`` etc.).  By default a rule
                        just listens for ``GET`` (and implicitly ``HEAD``).
                        Starting with Flask 0.6, ``OPTIONS`` is implicitly
                        added and handled by the standard request handling.
        """
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            optional_routes = self.generate_optional_routes(rule)

            for optional_route in optional_routes:
                self.app.add_url_rule(optional_route, endpoint, f, **options)
            return f
        return decorator