<template>
  <!-- This component allows the user to enter and submit a new comment -->
  <div class="modal-container">
    <div class="modal-header"><h3>Add Comment</h3></div>
    <div class="modal-body" style="height: 50vh">
      <div class="input-group">
        <textarea
          class="form-control mb-4"
          style="height: 25vh; resize: none"
          aria-label="With textarea"
          v-model="message"
        ></textarea>
      </div>

      <div v-if="replyTo && replyToMessage">
        <h5 class="border-top pt-4">Replying to:</h5>
        <p class="text-truncate">{{ replyToMessage.message }}</p>
        <p>
          From: {{ replyToMessage.created_by.user_name.first_name }}
          {{ replyToMessage.created_by.user_name.last_name }}
          ({{ replyToMessage.created_by.email }})
        </p>
      </div>
    </div>

    <div class="modal-footer">
      <input @click="createComment" type="button" value="Submit comment" class="btn btn-success" />
      <input @click="$emit('close')" type="button" value="Cancel" class="btn btn-danger" />
    </div>
  </div>
</template>

<script>
import { addComment, getAssetComments } from "@/api";
import { successToast } from "@/utils";

export default {
  name: "AddComment",
  props: [
    // The asset the comment is applied to
    "asset",
    // The id of the parent comment if the new comment is a reply
    "replyTo",
  ],

  data() {
    return {
      // The comment entered by the user
      message: "",
      // Stores a list of all comments made on the asset
      assetComments: [],
    };
  },

  computed: {
    replyToMessage() {
      // Finds the parent comment of the reply being added
      return this.assetComments.find((comment) => comment.id == this.replyTo);
    },
  },

  methods: {
    async createComment() {
      // Creates a new comment on the asset
      if (!confirm("Are you sure you want to add a comment?")) {
        return;
      }

      try {
        let data = {
          asset_id: this.asset.asset_id,
          message: this.message,
          reply_id: null,
        };

        // Sets parent if comment is a reply
        if (this.replyTo) {
          data.reply_id = this.replyTo;
        }

        let res = await addComment(data);
        successToast(res.message);
        this.$emit("close");
      } catch (error) {
        console.log(error);
      }
    },

    async getComments() {
      // Gets all comments for the asset
      try {
        this.assetComments = await getAssetComments(this.asset.asset_id);
      } catch (error) {
        console.log(error);
      }
    },
  },

  beforeMount() {
    this.getComments();
  },
};
</script>
