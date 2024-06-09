from flask import Blueprint, jsonify, request
from api.model.assetTypeAudit import AssetTypeAudit
from api.model.userAudit import UserAudit
from api.model.assetAudit import AssetAudit
from api.model.projectAudit import ProjectAudit
from api.route.roles import security_level_required
from api.utils.validation import required_parameters
from api.schema.audits import asset_audit_schema, user_audit_schema, asset_type_audit_schema, project_audit_schema
from api.model.audit import Audit

audit_api = Blueprint("audit", __name__)


@audit_api.route("/asset/types", methods=["GET"])
@security_level_required(100)
def getAssetTypeAudit():
    """Gets audit of all asset type changes.

    Returns:
        all_asset_type_audits (json): List of all asset type audits in database.
    """
    return jsonify(asset_type_audit_schema.dump(AssetTypeAudit.query.all())), 200


@audit_api.route("/users", methods=["GET"])
@security_level_required(100)
def getUserAudit():
    """Gets audit of all user changes.

    Returns:
        all_user_audits (json): List of all user audits in database.
    """
    return jsonify(user_audit_schema.dump(UserAudit.query.all())), 200


@audit_api.route("/assets", methods=["GET"])
@security_level_required(100)
def getAssetAudit():
    """"Gets audit of all asset changes.

    Returns:
        all_asset_audits (json): List of all asset audits in database.
    """
    return jsonify(asset_audit_schema.dump(AssetAudit.query.all())), 200


@audit_api.route("/projects", methods=["GET"])
@security_level_required(100)
def getProjectAudit():
    """Gets audit of all project changes.

    Returns:
        all_project_audits (json): List of all project audits in database.
    """
    return jsonify(project_audit_schema.dump(ProjectAudit.query.all())), 200

@audit_api.route("/mylogs", methods=["POST"])
@required_parameters(["email"])
@security_level_required(25)
def getMyAudits():
    """Gets audit made by given user.

    Returns:
        all_audits (json): List of all audits made by given user in database.
    """
    data = request.get_json()
    email = data["email"]

    assetAudits = AssetAudit.query.filter_by(email=email).all()
    projectAudits = ProjectAudit.query.filter_by(email=email).all()
    assetTypeAudits = AssetTypeAudit.query.filter_by(email=email).all()
    userAudits = UserAudit.query.filter_by(admin=email).all()

    audits = list(map(lambda audit:Audit(audit.id, audit.asset_name, audit.operation, audit.time, audit.description), assetAudits))
    audits = [*audits, *list(map(lambda audit:Audit(audit.id, audit.project_name, audit.operation, audit.time, audit.description), projectAudits))]
    audits = [*audits, *list(map(lambda audit:Audit(audit.id, audit.asset_type_name, audit.operation, audit.time, audit.description), assetTypeAudits))]
    audits = [*audits, *list(map(lambda audit:Audit(audit.id, audit.subject, audit.operation, audit.time, audit.subject_role), userAudits))]

    audits = list(map(lambda audit:audit.toDict(), audits))

    return jsonify(audits), 200