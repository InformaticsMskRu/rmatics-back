from marshmallow import EXCLUDE
from webargs.flaskparser import parser


@parser.location_loader('request_any')
def load_from_any_location(request, schema):
    """Mimics webargs < 6, which looked at the query string, the form and the JSON body.

    The first of them that has a field wins, in that order.
    """
    data = {}
    body = request.get_json(silent=True)
    if isinstance(body, dict):
        data.update(body)
    data.update(request.form.to_dict())
    data.update(request.args.to_dict())
    return data


def parse_args(argmap, request=None, **kwargs):
    return parser.parse(argmap, request, location='request_any', unknown=EXCLUDE, **kwargs)
