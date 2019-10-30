import logging

import azure.functions as func
from datetime import datetime


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    name = req.params.get("name")
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get("name")

    if name:
        return func.HttpResponse(f"Hello {name}!!! (" + str(datetime.now()) + ")\n")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400,
        )
