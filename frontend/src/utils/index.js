import { createToast } from "mosha-vue-toastify";
import "mosha-vue-toastify/dist/style.css";
import moment from "moment";


export const formatDate = (value) => {
  // Returns a provided date in a reader-friendly format
  return moment(String(value)).format("DD-MM-YYYY HH:mm");
};

export const successToast = (message) => {
  // Displays a pop-up for a successful task execution
  createToast(message, {
    type: "success",
    position: "bottom-center",
  });
};

export const dangerToast = (message) => {
  // Displays a pop-up for a failed task execution
  createToast(message, {
    type: "danger",
    position: "bottom-center",
  });
};

export const warningToast = (message) => {
  // Displays a pop-up to provide extra clarification to the user
  createToast(message, {
    type: "warning",
    position: "bottom-center",
  });
};