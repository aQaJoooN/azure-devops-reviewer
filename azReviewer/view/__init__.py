from azReviewer import api

from azReviewer.view.webhook import WebHookResource


api.add_resource(
    WebHookResource,
    "/webhook",
    methods=["GET"],
    endpoint="webhook"
)
api.add_resource(
    WebHookResource,
    "/webhook/pipeline",
    methods=["POST"],
    endpoint="pipeline"
)
