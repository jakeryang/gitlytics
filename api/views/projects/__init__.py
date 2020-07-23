from flask import Blueprint, render_template, url_for, redirect, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from requests_oauthlib import OAuth2Session
from marshmallow import ValidationError

from app import db
from models import Course, Invite, Project, Group, User, ProjectTypes, Repo
import views.projects.schemas as ps
from .utils import add_webhook
import settings

projects = Blueprint('projects', __name__)

@projects.route("/", methods=['POST'])
@jwt_required
def create_project():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No json provided"}), 400
    try:
        data = ps.project_create_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 422
    course = Course.query.get(data['course_id'])
    if not course:
        return jsonify(error="Course ID not found"), 400
    if course.owner_id != current_user.id:
        return jsonify(error="Unauthorized to add a project to course"), 403

    project = Project(name=data['name'],
                      description=data['description'],
                      start_date=data['start_date'],
                      due_date=data['due_date'],
                      course_id=data['course_id'],
                      type=data['type'])
    db.session.add(project)
    db.session.commit()

    if 'group' in data['type']:
        for group in data['groups']:
            g = Group(project_id=project.id)
            for user in group:
                u = User.query.get(user['id'])
                g.users.append(u)
            db.session.add(g)
        db.session.commit()

    return jsonify(message="success", project=ps.project_schema.dump(project))

@projects.route("/<int:project_id>", methods=['DELETE'])
@jwt_required
def delete_project(project_id):
    project = Project.query.get(project_id)

    if project is None:
        return jsonify(message="Not found"), 404

    if project.course.owner_id == current_user.id:
        db.session.delete(project)
        db.session.commit()
        return jsonify({}), 204
    else:
        return jsonify(message="Unauthorized"), 403

@projects.route("/<int:project_id>/repos", methods=['POST'])
@jwt_required
def add_repo(project_id):
    data = request.get_json()
    project = Project.query.get(project_id)
    if project is None:
        return jsonify(message="Project not found"), 404
    if not project.course.is_user(current_user.id):
        return jsonify(message="Unauthorized to add project"), 403
    repo = project.get_repo_for_user(current_user.id)
    if repo:
        return jsonify(message="Already added repo for project"), 400

    repo = Repo(project_id=project.id, name=data['repo_name'])
    repo.user_id = current_user.id
    if project.type is not ProjectTypes.IND:
        g = project.get_group_for_user(current_user.id)
        if g is None:
            return jsonify(message="Not part of group"), 400
        repo.group_id = g.id

    webhook = add_webhook(repo.name, current_user.oauth_token)
    if 'id' not in webhook:
        return jsonify(error="Could not create webhook", data=webhook), 401
    repo.webhook_id = webhook['id']

    db.session.add(repo)
    db.session.commit()
    return jsonify(repo=ps.RepoSchema().dump(repo)), 201

@projects.route("/search/repo")
@jwt_required
def search_user_repos():
    github = OAuth2Session(settings.GITHUB_OAUTH_CLIENT_ID, token={"access_token": current_user.oauth_token})
    resp = github.get(f"{settings.GITHUB_API_BASE_URL}user/repos?sort=pushed&affiliation=owner").json()

    return jsonify([{"full_name": u['full_name']} for u in resp])