from flask import Blueprint, request, jsonify
from api.model.projects import Project, project_map
from api.schema.projects import project_schema, single_project_schema
from api.model.assets import Asset
from api.model.db import db
from api.route.roles import security_level_required
from api.utils.validation import required_parameters
import api.utils.projectAudit as audit

project_api = Blueprint("project", __name__)


@project_api.route("/", methods=["POST"])
@required_parameters(["name", "description", "assets"])
@security_level_required(100)
def createProject(current_user):
    """Adds a new project.

    Returns:
        response (json): Success message.
    """
    data = request.get_json()

    if data["name"].strip() == "":
        return jsonify({"message": "Project name cannot be empty."}), 400

    if data["description"].strip() == "":
        return jsonify({"message": "Project description cannot be empty."}), 400

    if Project.query.filter_by(project_name=data["name"]).first() != None:
        return jsonify({"message": "Project name already in database. Choose a different name."}), 400

    new_project = Project(
        data["name"], data["description"], current_user["id"])
    db.session.add(new_project)
    db.session.flush()
    db.session.refresh(new_project)

    # Adds all provided assets to the project
    for asset_id in data["assets"]:
        asset = Asset.query.filter_by(asset_id=asset_id).first()
        new_project.assets.append(asset)

    db.session.commit()

    # Logs the project creation
    audit.recordCreate(
        user_email=current_user["email"], project_name=data["name"])

    return jsonify({"message": "success"}), 201


@project_api.route("/<id>", methods=["PATCH"])
@required_parameters(["project_name", "project_description", "assets"])
@security_level_required(100)
def editProject(id, current_user):
    """Updates a single project.

    Args:
        id (int): the id of the project to edit.

    Returns:
        updated_project (json): Updated project as a project object.
    """
    data = request.get_json()

    if data["project_name"].strip() == "":
        return jsonify({"message": "Project name cannot be empty."}), 400

    if data["project_description"].strip() == "":
        return jsonify({"message": "Project description cannot be empty."}), 400

    if Project.query.filter(Project.project_id != id, Project.project_name == data["project_name"]).first() != None:
        return jsonify({"message": "Project name already in database. Choose a different name."}), 400

    project = Project.query.filter_by(project_id=id)

    names = project.first().project_name, data["project_name"]

    project.update({"project_name": data["project_name"],
                    "project_description": data["project_description"]})

    project = project.first()

    # Removes all mapped assets in the project map
    db.session.query(project_map).filter_by(
        project_id=project.project_id).delete()

    # Updates assets of the project
    for asset_name in data["assets"]:
        asset = Asset.query.filter_by(asset_name=asset_name).first()
        project.assets.append(asset)

    db.session.commit()

    # Logs the project update
    audit.recordUpdate(
        user_email=current_user["email"], project_name=data["project_name"], names=names)

    return jsonify(single_project_schema.dump(project)), 200


@project_api.route("/", methods=["GET"])
@security_level_required(25)
def getProjects():
    """Gets all of the projects.

    Returns:
        all_projects (json): List of all projects in database as project objects.
    """
    return jsonify(project_schema.dump(Project.query.all())), 200


@project_api.route("/<id>", methods=["GET"])
@security_level_required(25)
def getProject(id):
    """Gets a single project.

    Args:
        id (int): the id of the requested project.

    Returns:
        requested_project (json): Requested project as a project object.
    """
    return jsonify(single_project_schema.dump(Project.query.filter_by(project_id=id).first())), 200


@project_api.route("/<id>", methods=["DELETE"])
@security_level_required(100)
def deleteProject(id, current_user):
    """Deletes a single project.

    Args:
        id (int): the id of the project being deleted.

    Returns:
        deleted_project (json): Deleted project as a project object.
    """
    project = Project.query.filter_by(project_id=id)

    project_name = project.first().project_name
    res = single_project_schema.dump(project.first())

    project.delete()
    db.session.commit()

    # Logs the project deletion
    audit.recordDelete(project_name=project_name,
                       user_email=current_user["email"])

    return jsonify(res), 200
