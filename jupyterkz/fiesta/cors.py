class CorsMiddleware(object):
    def process_response(self, req, response):
        response["Access-Control-Allow-Origin"] = "*"
        return response
