<template>
  <!-- This component displays all comments made on an asset -->
  <div class="modal-container">
    <div class="modal-header"><h3>Comments</h3></div>
    <div class="modal-body overflow-auto" style="height: 50vh">
      <div
        v-for="comment in this.comments"
        :key="comment.id"
        :id="comment.id"
        :ref="'card' + comment.id"
      >
        <div class="card mb-2">
          <div class="card-header">
            {{ comment.created_by.user_name.first_name }}
            {{ comment.created_by.user_name.last_name }}
            ({{ comment.created_by.email }})

            <a v-if="canEdit" @click="$emit('replyTo', comment.id)" href="#">
              Reply to this comment
            </a>
          </div>

          <div class="card-body">
            <p v-if="comment.reply_to">
              <a @click="jumpToParent(comment.reply_to.id)" :href="'#' + comment.reply_to.id"
                >Replying to ...</a
              >
            </p>
            <h5 class="card-title">
              <span style="white-space: pre-wrap">{{ comment.message }} </span>
            </h5>
            <p class="card-text">
              {{ formatDate(comment.created_on) }}
            </p>
          </div>

          <div class="card-footer" v-if="canEdit && comment.created_by.id == currentUser.id">
            <button type="button" class="btn btn-danger" @click="removeComment(comment.id)">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal-footer justify-content-between">
      <button type="button" class="btn btn-primary" @click="$emit('asset')">Open asset info</button>

      <button type="button" class="btn btn-secondary" @click="$emit('close')">Close</button>
      <button type="button" class="btn btn-success" v-if="canEdit" @click="$emit('replyTo', null)">
        Add Comment
      </button>
    </div>
  </div>
</template>

<script>
import { formatDate } from "@/utils";
import { deleteComment, getAssetComments } from "@/api";

export default {
  name: "Comments",
  props: [
    // The asset for which the comments are being displayed
    "asset",
  ],
  emits: [
    // Closes the pop-up
    "close",
    // The id of the parent comment if a new comment is a reply
    "replyTo",
  ],

  setup() {
    return {
      formatDate,
    };
  },

  data() {
    return {
      // Allows user to add comments if they have the required security level
      canEdit: false,
      // The security required to make a new comment
      requiredSecurity: 50,
      // A list of all comments on the asset
      comments: [],
      // The currently logged in user's details
      currentUser: this.$store.getters.currentUser,
    };
  },

  methods: {
    async getComments() {
      // Loads all comments on the asset
      try {
        this.comments = await getAssetComments(this.asset.asset_id);
      } catch (error) {
        console.log(error);
      }
    },

    jumpToParent(id) {
      // Displays the parent of a selected reply comment
      this.$refs["card" + id][0].firstChild.classList.add("alert-info");
      setTimeout(() => {
        this.$refs["card" + id][0].firstChild.classList.remove("alert-info");
      }, 400);
    },

    async removeComment(id) {
      // Removes a comment from the database
      if (!confirm("Are you sure you would like to delete this comment?")) {
        return;
      }

      try {
        await deleteComment(id);
        this.getComments();
      } catch (error) {
        console.log(error);
      }
    },
  },

  beforeMount() {
    // Determines if user can edit assets
    this.canEdit = this.$store.getters.securityLevel >= this.requiredSecurity;

    this.getComments();
  },
};
</script>

<style>
.card {
  transition: background-color 200ms ease;
}
</style>
