<template>
  <!-- Contains information about the site and who can access what -->
  <div class="about">
    <div class="mx-4">
      <h2>Overview</h2>
      <p>
        This system allows users to store assets, associate assets with each other, and store
        metadata about those assets into a database that can be easily searched and accessed.<br />
        <br />
      </p>

      <h2>Dashboard</h2>
      <p>
        The Dashboard allows for users of all roles to change their name and password for use within
        the system. <br />
        <br />
      </p>

      <h2>Assets</h2>
      <p>
        Asset contains metadata which includes information regarding the author of said asset, the
        date of creation, and its last updated change. <br />
        Users are able to add tags, as well as add attribute values, depending on the type of asset
        they are creating. <br />
        Assets can also have associations, which can be viewed when selecting an asset that displays
        subsequent associated assets. <br />
        Once an asset is added to the database, viewers will be able to inspect the asset and all
        its details on the 'Assets' page. Additionally, users with the necessary permissions can
        also edit and comment on the asset. <br />
        Assets can be easily searched through in the 'Assets' page using different filters.<br />
        <br />
      </p>

      <h2>Projects</h2>
      <p>
        <strong> Only accessible by administrators </strong> <br />
        Projects can be created which allow for assets to be grouped for a specific task. <br />
        <br />
      </p>

      <h2>Admin</h2>
      <p>
        <strong> Only accessible by administrators </strong> <br />
        The admin page allows for system level admins to create asset types, add new users, and view
        the audit log for all activity.<br />
        Asset Types can be created, which contain attributes that can be used when creating assets.
        Asset Types also have attribute inheritance to associate each other to other asset types.<br />
        <br />
        Admins can create new users and assign them to one of three roles: <br />
        - Viewers, which can view the assets page but cannot edit any assets or add any of their
        own.
        <br />
        - Normal users, which can view, add and edit assets on the assets page, but cannot create
        asset types.
        <br />
        - Admin users, which can do all of the previously mentioned tasks, in addition to creating
        asset types. <br />
        <br />
        Admins are also able to view audit logs of all activity in the system which pertains to
        assets, asset types, user management and project management. <br />
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "About",
};
</script>
