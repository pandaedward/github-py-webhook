# from __future__ import print_function
import json
import os
import sys

from github import Github

from flask import Flask, request

app = Flask(__name__)

# Ensure a github token is set in environment variable
# TODO: Retrieve secret from Key Vault or Secret Manager

try:
    os.environ["GITHUB_PAT"]
except KeyError:
    print("Please set environment variable GITHUB_PAT")
    sys.exit(1)
# User or Personal Access Token must have read/write access to repository to add issue to
client = Github(os.environ["GITHUB_PAT"])


# @app.route("/payload", methods=['POST'])
@app.route('/')
def api_root():
    # API root level for testing only
    return '200'


# Only takes POST
@app.route('/payload', methods=['POST'])
def api_payload():
    print(request.get_data())
    # print(json.loads(request.get_data()))
    api_body = json.loads(request.get_data())
    print(api_body)
    # determine organisation webhook action type
    webhook_action = api_body["action"]

    if webhook_action == 'created':
        print("New repository name: ", api_body["repository"]["name"])
        print("Repository full name: ", api_body["repository"]["full_name"])
        # org_repo = client.get_repo(api_body["repository"]["full_name"])
        org_repo = client.get_repo(api_body["repository"]["full_name"])
        print(org_repo)
        # pygithub call to create issue
        issue = org_repo.create_issue(
            title="A new repository is created",
            body="Hooray! A new repository is created. Let's notify @pandaedward and celebrate",
            labels=[
                org_repo.get_label("good first issue")
            ]
        )
        print(issue)
        print("First issue created in new repository")
        # Identify branch to protect
        print("Default branch: ", api_body["repository"]["default_branch"])
        default_branch = api_body["repository"]["default_branch"]
        # pygithub call to get branch
        protect_branch = org_repo.get_branch(default_branch)
        # Call to edit branch protection
        protect_branch.edit_protection(strict=True, required_approving_review_count=2, enforce_admins=True)
        print("Edited branch protection rules for: ", default_branch)
    else:
        # TODO Other actions to be added
        print("Not interested in actions other than created")

    return 'OK'


if __name__ == '__main__':
    app.run(debug=True)
