from datetime import datetime
from flask import Blueprint, jsonify, request
from api.model.assets import Asset, AssetAttribute
from api.schema.assets import asset_schema, single_asset_schema, advanced_asset_schema, single_advanced_asset_schema
from api.model.assetTypes import AssetTypeAttribute, AssetType
from api.model.tags import Tag, association_table
from api.model.projects import Project, project_map
from api.route.roles import security_level_required
from api.utils.validation import required_parameters
import api.utils.assetAudit as audit
from datetime import datetime
from api.model.db import db
from api.model.assetRating import AssetRating
from api.schema.assetRating import ratings_schema

asset_api = Blueprint("asset", __name__)


@asset_api.route("/", methods=["GET"])
@security_level_required(25)
def getAssets():
    """Gets all the assets in the database.

    Returns:
        all_assets (json): List of all asset in database as asset objects.
    """
    return jsonify(advanced_asset_schema.dump(Asset.query.all())), 200


@asset_api.route("/<id>", methods=["GET"])
@security_level_required(25)
def getAssetById(id):
    """Gets a single asset.

    Args:
        id (int): the id of the requested asset.

    Returns:
        asset (json): Asset requested as an asset object.
    """
    return jsonify(single_advanced_asset_schema.dump(Asset.query.filter_by(asset_id=id).first())), 200


@asset_api.route("/add", methods=["POST"])
@required_parameters(["asset_name", "asset_type_id", "attributes", "tag_names", "project_names"])
@security_level_required(50)
def addAsset(current_user):
    """Adds a new asset.

    Returns:
        asset (json): Asset that was just added as an asset object.
    """
    data = request.get_json()

    if data["asset_name"].strip() == "":
        return jsonify({"message": "Asset name cannot be empty."}), 400

    if Asset.query.filter_by(asset_name=data["asset_name"]).first() != None:
        return jsonify({"message": "Asset name already in database. Choose a different name."}), 400

    new_asset = Asset(data["asset_name"], data["asset_type_id"],
                      current_user["id"], datetime.now())

    db.session.add(new_asset)
    db.session.flush()
    assetTypeAttributes = AssetTypeAttribute.query

    # Creates all new attributes
    for attribute in data["attributes"]:
        attribute_value = data["attributes"][attribute]

        if attribute_value.strip() == "":
            return jsonify({"message": "Attribute name cannot be empty."}), 400

        asset_attribute_ids = assetTypeAttributes.filter_by(
            attribute_name=attribute).first().asset_attribute_id
        new_attribute_value = AssetAttribute(
            attribute_value, new_asset.asset_id, asset_attribute_ids)
        db.session.add(new_attribute_value)

    # Assigns tags and creates all new tags
    for tag_name in data["tag_names"]:
        tag = Tag.query.filter_by(tag_name=tag_name).first()
        if tag == None:
            tag = Tag(tag_name)
        new_asset.tags.append(tag)

    # Assigns projects
    for project_name in data["project_names"]:
        project = Project.query.filter_by(project_name=project_name).first()
        new_asset.projects.append(project)

    db.session.commit()

    # Logs the asset creation
    audit.recordCreate(
        user_email=current_user["email"], asset_name=data["asset_name"])

    return jsonify(single_asset_schema.dump(new_asset)), 201


@asset_api.route("/", methods=["DELETE"])
@required_parameters(["asset_id"])
@security_level_required(50)
def deleteAsset(current_user):
    """Removes an asset from the database.

    Returns:
        asset (json): Asset removed from database as an asset object.
    """
    data = request.get_json()

    if Asset.query.filter_by(asset_id=data["asset_id"]).first() == None:
        return jsonify({"message": "Asset does not exist in database."}), 404

    asset = Asset.query.filter_by(asset_id=data["asset_id"])

    asset_name = asset.first().asset_name

    response = asset_schema.dump(asset)
    db.session.delete(asset.first())

    db.session.commit()

    # Logs the asset deletion
    audit.recordDelete(asset_name=asset_name, user_email=current_user["email"])

    return jsonify(response), 200


@asset_api.route("/", methods=["PATCH"])
@required_parameters(["asset_id", "asset_name", "attributes", "tag_names", "project_names"])
@security_level_required(50)
def updateAsset(current_user):
    """Edits asset name and attribute values.

    Returns:
        asset (json): Asset updated as an asset object.
    """
    data = request.get_json()

    if data["asset_name"].strip() == "":
        return jsonify({"message": "Asset name cannot be empty."}), 400

    if Asset.query.filter(Asset.asset_id != data["asset_id"], Asset.asset_name == data["asset_name"]).first() != None:
        return jsonify({"message": "Asset name already in database. Choose a different name."}), 400

    asset = Asset.query.filter_by(asset_id=data["asset_id"]).first()

    # Names to update log
    names = asset.asset_name, data["asset_name"]
    asset.asset_name = data["asset_name"]

    db.session.query(association_table).filter_by(
        asset_id=data["asset_id"]).delete()

    db.session.commit()

    # Updates and creates tags
    for tag_name in data["tag_names"]:
        tag = Tag.query.filter_by(tag_name=tag_name).first()
        if tag == None:
            tag = Tag(tag_name)
        asset.tags.append(tag)

    db.session.query(project_map).filter_by(
        asset_id=data["asset_id"]).delete()

    # Updates projects
    for project_name in data["project_names"]:
        project = Project.query.filter_by(project_name=project_name).first()
        asset.projects.append(project)

    # Updates attributes
    for id, value in data["attributes"].items():
        if value.strip() == "":
            return jsonify({"message": "Attribute name cannot be empty."}), 400

        asset_attribute_id = AssetTypeAttribute.query.filter_by(
            asset_attribute_id=id).first().asset_attribute_id
        asset_attribute = AssetAttribute.query.filter_by(
            asset_id=asset.asset_id).filter_by(asset_attribute_type_id=asset_attribute_id).first()

        asset_attribute.attribute_value = value

    db.session.commit()

    # Logs the asset update
    audit.recordUpdate(asset_name=asset.asset_name,
                       user_email=current_user["email"],
                       names=names)

    return jsonify({"message": "Update successful."}), 200


@asset_api.route("/associations/<id>", methods=["GET"])
@security_level_required(25)
def getAssociatedAssets(id):
    """Gets related assets ordered by strongest association first.

    Args:
        id (int): the id of the asset for which the associations are provided.

    Returns:
        associated_assets (json): Top 10 most associated assets as asset objects.
    """
    queried_asset = Asset.query.filter_by(asset_id=id).first()

    #tag ids of all assets tags
    tag_ids = map(lambda tag: tag.tag_id, db.session.query(association_table).filter(association_table.c.asset_id == id).all())

    #A query returning asset ids and a count of all thier occurances
    count_query = db.session.query(association_table.c.asset_id, db.func.count(
        association_table.c.asset_id).label("count"))
    #Filter the query by tag ids, group by asset id and order the list by their count
    assets = count_query.filter(association_table.c.tag_id.in_(tag_ids), association_table.c.asset_id != id).group_by(
        association_table.c.asset_id).order_by(~db.func.count(association_table.c.asset_id)).all()

    #Creates list of all added asset ids
    asset_ids = list(map(lambda asset: asset.asset_id, assets))
    asset_ids.append(queried_asset.asset_id)

    #List of asset rating objects with thier count mapped to rating
    ratings = map(lambda asset: AssetRating(
        asset.asset_id, asset.count+1), assets)

    otherAssets = Asset.query

    #Adds all other assets as rating objects to "ratings" list with low ratings
    for id in asset_ids:
        otherAssets = otherAssets.filter(Asset.asset_id != id)

    ratings = [
        *list(ratings), *list(map(lambda asset: AssetRating(asset.asset_id, 1), otherAssets))]

    #Applies multipliers to ratings
    for rating in ratings:
        multiplier = 1
        associated_asset = Asset.query.filter_by(
            asset_id=rating.asset_id).first()
        associated_asset_type = AssetType.query.filter_by(
            asset_type_id=associated_asset.asset_type_id).first()
        associated_asset_type_id = associated_asset_type.asset_type_id

        #if assets share asset types the multiplier is increased
        if associated_asset_type_id == queried_asset.asset_type_id:
            multiplier = multiplier+1

        #for each project shared, the multiplier is increased
        for project in associated_asset.projects:
            if project in queried_asset.projects:
                multiplier = multiplier+2

        rating.ratingMulti(multiplier)

    #Values are dumped into a schema and sorted by thier new rating. Only the top 10 are sent
    values = ratings_schema.dump(ratings)
    values = sorted(values, key=lambda d: d["rating"], reverse=True)
    return jsonify(values[:10]), 200
