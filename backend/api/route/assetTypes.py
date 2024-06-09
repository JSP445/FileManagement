from api.model.assetTypes import AssetType, AssetTypeAttribute
from api.schema.assetTypes import asset_type_schema, asset_type_info_schema, single_asset_type_schema, type_schema
from api.model.attributeTypes import AttributeType
from flask import Blueprint, jsonify, request
from api.route.roles import security_level_required
from api.utils.validation import required_parameters
from api.model.assets import Asset, AssetAttribute
import api.utils.assetTypeAudit as audit
from api.model.db import db
from api.schema.assets import asset_schema

asset_types_api = Blueprint("Asset Types", __name__)


@asset_types_api.route("/", methods=["GET"])
@security_level_required(25)
def getAllAssetTypes():
    """Gets all asset types.

    Returns:
        all_asset_types (json): A list of all asset types in database as asset type objects.
    """
    return jsonify(asset_type_schema.dump(AssetType.query.all())), 200


@asset_types_api.route("/details", methods=["GET"])
@security_level_required(25)
def getAssetInfo():
    """Gets the id and name of all asset types.
    Returns:
        asset_type (json): Asset type requested as an asset type object.
    """
    return jsonify(asset_type_info_schema.dump(AssetType.query.all())), 200


@asset_types_api.route("/<int:asset_type_id>", methods=["DELETE"])
@security_level_required(100)
def removeAssetType(current_user, asset_type_id):
    """Removes an asset type.

    Args:
        asset_type_id (int): the id of the asset type being deleted.

    Returns:
        asset_type (json): Deleted asset type as an asset type object.
    """
    assetType = AssetType.query.filter_by(asset_type_id=asset_type_id)

    if assetType.first() == None:
        return jsonify({"message": "Asset type selected not in database."}), 404

    asset_type_name = assetType.first().asset_type_name
    parentAssetTypeId = assetType.first().inherited_from

    res = asset_type_schema.dump(assetType)

    # Sets all children to inherit from the parent of this asset type
    AssetType.query.filter_by(inherited_from=asset_type_id).update(
        {"inherited_from": parentAssetTypeId})

    db.session.flush()

    db.session.delete(assetType.first())

    db.session.commit()

    # Logs the asset type deletion
    audit.recordDelete(asset_type_name, current_user["email"])

    if AssetType.query.filter_by(asset_type_id=asset_type_id).first() == None:
        return jsonify(res), 200


@asset_types_api.route("/", methods=["POST"])
@required_parameters(["asset_type_name", "parent_asset_type"])
@security_level_required(100)
def addAssetType(current_user):
    """Adds an asset type.

    Returns:
        asset_type (json): Added asset type as an asset type object.
    """
    data = request.get_json()

    if data["asset_type_name"].strip() == "":
        return jsonify({"message": "Asset type name cannot be empty."}), 400

    if AssetType.query.filter_by(asset_type_name=data["asset_type_name"]).first() != None:
        return jsonify({"message": "Asset type name already in database. Choose a different name."}), 400

    new_asset_type = AssetType(data["asset_type_name"], current_user["id"])
    new_asset_type.set_parent(data["parent_asset_type"])

    db.session.add(new_asset_type)
    db.session.flush()
    db.session.refresh(new_asset_type)

    # Adds attributes to the asset type
    if "attributes" in data:
        attributes = data["attributes"]

        for attribute in attributes:
            if "type_id" in attribute:
                new_asset_attribute = AssetTypeAttribute(
                    new_asset_type.asset_type_id, attribute["name"], attribute["type_id"])
            else:
                new_asset_attribute = AssetTypeAttribute(
                    new_asset_type.asset_type_id, attribute["name"])
            db.session.add(new_asset_attribute)

    db.session.flush()
    db.session.commit()

    # Logs the asset type creation
    audit.recordCreate(data["asset_type_name"], current_user["email"])

    return jsonify(single_asset_type_schema.dump(new_asset_type)), 201


@asset_types_api.route("/<id>", methods=["GET"])
@security_level_required(25)
def getAssetType(id):
    """Gets a single asset type.

    Args:
        id (int): the id of the requested asset type.

    Returns:
        asset_type (json): Requested asset type as an asset type object.
    """
    asset_type = AssetType.query.filter_by(asset_type_id=id)
    if asset_type.first() == None:
        return jsonify({"message": "Asset type selected not in database."}), 404

    parent_attributes = []

    current_asset_type = asset_type.first()
    parent_asset_type_name = single_asset_type_schema.dump(
        AssetType.query.filter_by(asset_type_id=current_asset_type.inherited_from).first())["asset_type_name"]

    # Gets all attributes from parent asset types
    while current_asset_type.asset_type_id != current_asset_type.inherited_from:
        parent_asset_type = AssetType.query.filter_by(
            asset_type_id=current_asset_type.inherited_from).first()

        for attribute in single_asset_type_schema.dump(parent_asset_type)["attributes"]:
            parent_attributes.append(attribute)
        current_asset_type = parent_asset_type

    res = single_asset_type_schema.dump(asset_type.first())
    res["parent_attributes"] = parent_attributes
    res["parent_name"] = parent_asset_type_name
    return jsonify(res), 200


@asset_types_api.route("/", methods=["PATCH"])
@required_parameters(["asset_type_id", "asset_type_name", "attributes"])
@security_level_required(100)
def updateAssetType(current_user):
    """"Edits asset types.

    Returns:
        asset_type (json): Updated asset type as an asset type object.
    """
    data = request.get_json()

    if data["asset_type_name"].strip() == "":
        return jsonify({"message": "Asset type name cannot be empty."}), 400

    updated_asset_type = AssetType.query.filter_by(
        asset_type_id=data["asset_type_id"])

    if updated_asset_type.first() == None:
        return jsonify({"message": "Asset type selected not found in database."}), 404

    # Names to update log
    names = updated_asset_type.first().asset_type_name, data['asset_type_name']

    if AssetType.query.filter(AssetType.asset_type_id != data['asset_type_id'], AssetType.asset_type_name == data['asset_type_name']).first() != None:
        return jsonify({"message": "Another asset type already has this name."}), 400

    types_attributes = AssetTypeAttribute.query.filter_by(
        asset_type_id=data["asset_type_id"])

    # Updates attributes
    for attribute in data["attributes"]:
        if "attribute_name" not in attribute:
            return jsonify({"message": "Missing required parameter: attribute_name."}), 400

        if attribute["attribute_name"].strip() == "":
            return jsonify({"message": "Attribute name cannot be empty."}), 400

        if "asset_attribute_id" not in attribute:
            return jsonify({"message": "Missing required parameter: asset_attribute_id"}), 400

        if "attribute_type_id" not in attribute:
            return jsonify({"message": "Missing required parameter: asset_type_id"}), 400

        attribute_name = attribute["attribute_name"]
        attribute_type_id = attribute["attribute_type_id"]
        uniqueCheck = AssetTypeAttribute.query.filter_by(
            asset_type_id=data["asset_type_id"]).filter_by(attribute_name=attribute_name)

        # Create new attribute
        if attribute["asset_attribute_id"] < 0:
            if uniqueCheck.first() != None:
                return jsonify({"message": "An attribute of this asset type already has this name."}), 400

            new_attribute = AssetTypeAttribute(
                data["asset_type_id"], attribute_name, attribute_type_id)

            db.session.add(new_attribute)
            db.session.flush()
            db.session.refresh(new_attribute)

            Asset.query.filter_by(asset_type_id=data["asset_type_id"])

            # Enters blank fields when a new attributed to an asset
            for asset in updated_asset_type.first().assets:
                attribute = AssetAttribute(
                    "EMPTY", asset.asset_id, new_attribute.asset_attribute_id)
                db.session.add(attribute)
            for asset_type in updated_asset_type.first().children:
                if asset_type.asset_type_id != updated_asset_type.first().asset_type_id:
                    for asset in asset_type.assets:
                        attribute = AssetAttribute(
                            "EMPTY", asset.asset_id, new_attribute.asset_attribute_id)
                        db.session.add(attribute)

            updated_asset_type.update({})

            db.session.flush()
            db.session.refresh(new_attribute)

            types_attributes = types_attributes.filter(
                AssetTypeAttribute.asset_attribute_id != new_attribute.asset_attribute_id)
        else:
            updated_attribute = AssetTypeAttribute.query.filter_by(
                asset_attribute_id=attribute["asset_attribute_id"])

            if updated_attribute.first() == None:
                return jsonify({"message": "An asset attribute selected was not found in the database."}), 404

            if uniqueCheck.first() != None and uniqueCheck.first() != updated_attribute.first():
                return jsonify({"message": "An attribute of this asset type already has this name."}), 400

            # Updates attribute types
            if updated_attribute.first().attribute_type_id != attribute_type_id:
                updated_attribute.update(
                    {"attribute_type_id": attribute_type_id})

            if updated_attribute.first().attribute_name != attribute_name:
                updated_attribute.update({"attribute_name": attribute_name})
                updated_asset_type.update({})

            types_attributes = types_attributes.filter(
                AssetTypeAttribute.asset_attribute_id != attribute["asset_attribute_id"])

    if updated_asset_type.first().asset_type_name != data["asset_type_name"]:
        updated_asset_type.update({"asset_type_name": data["asset_type_name"]})

    for attribute in types_attributes:
        AssetAttribute.query.filter_by(
            asset_attribute_type_id=attribute.asset_attribute_id).delete()

    types_attributes.delete()

    db.session.commit()

    # Logs the asset type update
    audit.recordUpdate(names, current_user["email"])

    return jsonify(single_asset_type_schema.dump(updated_asset_type.first())), 200


@asset_types_api.route("/attribute", methods=["GET"])
@security_level_required(100)
def getAttributeTypes():
    """Get all data types of asset type attributes.

    Returns:
        all_asset_attribute_types (json): List of all attribute types in database as Attribute type objects.
    """
    return jsonify(type_schema.dump(AttributeType.query.all())), 200
