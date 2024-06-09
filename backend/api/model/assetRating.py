class AssetRating:
    """Model for finding the association of assets."""

    def __init__(self, id, rating):
        """
        Args:
            id (int): id of the asset.
            rating (int): the level of association between the two assets.
        """
        self.asset_id = id
        self.rating = rating

    def ratingMulti(self, multiplier):
        """Increases the rating by a multiplier to indicate higher association.

        Args:
            multiplier (int): the multiplier to increase the rating by.
        """
        self.rating = self.rating * multiplier
