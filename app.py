from flask import Flask
from flask_restful import Api

from resources.cv_resource import CVResource
from resources.job_title_resource import JobTitleResource
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
api = Api(app)


api.add_resource(JobTitleResource, "/job-title")
api.add_resource(CVResource, "/generate-cv")


if __name__ == "__main__":
    app.run(debug=True)
