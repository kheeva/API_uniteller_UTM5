from controller import App

from helpers import parse_post_params, is_correct_query_params, our_signature, pay
from settings import ip_white_list, required_query_params, password


application = App(ip_white_list)


@application.register_handler('^/uniteller_api_v1/$', ['POST'])
def uniteller_url_handler(environ, url_params):
    try:
        length = int(environ.get('CONTENT_LENGTH', '0'))
    except:
        return b'412: Need a content', 412, {}
    else:
        post_params = parse_post_params(environ['wsgi.input'], length)
        print(post_params)

        if not is_correct_query_params(post_params, required_query_params):
            return b'412: BAD PARAMS', 412, {}

        if not our_signature(post_params, password, required_query_params):
            return b'403: Forbidden', 403, {}

        return pay(post_params)
