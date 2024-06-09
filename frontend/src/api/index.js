import store from "@/store/index.js";
import axios from "axios";

const BASE_URL = "http://localhost:8080/api";

// Sets the token in the header
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers["Authorization"] = "Bearer " + token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Logs the user out if they are not authenticated
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response.status == 401) {
      store.dispatch("logout");
    }
    return Promise.reject(error);
  }
);

export const register = (body) => {
  return axios.post(`${BASE_URL}/auth/register`, body).then((res) => res.data);
};

export const addAssetType = (body) => {
  return axios.post(`${BASE_URL}/asset/type/`, body).then((res) => res.data);
};

export const fetchAssetTypes = (body) => {
  return axios.get(`${BASE_URL}/asset/type/details`, body).then((res) => res.data);
};

export const fetchAssetType = (id) => {
  return axios.get(`${BASE_URL}/asset/type/${id}`).then((res) => res.data);
};

export const removeAssetType = (id) => {
  return axios.delete(`${BASE_URL}/asset/type/${id}`).then((res) => res.data);
};

export const updateAssetType = (body) => {
  return axios.patch(`${BASE_URL}/asset/type/`, body).then((res) => res.data);
};

export const authenticate = (body) => {
  return axios.post(`${BASE_URL}/auth/login`, body).then((res) => res.data);
};

export const fetchAllAssetTypes = () => {
  return axios.get(`${BASE_URL}/asset/type/`).then((res) => res.data);
};

export const addAsset = (body) => {
  return axios.post(`${BASE_URL}/asset/add`, body).then((res) => res.data);
};

export const getAssets = () => {
  return axios.get(`${BASE_URL}/asset/`).then((res) => res.data);
};

export const getAttributeTypes = () => {
  return axios.get(`${BASE_URL}/asset/type/attribute`).then((res) => res.data);
};

export const deleteAsset = (body) => {
  return axios.delete(`${BASE_URL}/asset/`, { data: body }).then((res) => res.data);
};

export const updateAsset = (body) => {
  return axios.patch(`${BASE_URL}/asset/`, body).then((res) => res.data);
};

export const associateAsset = (asset_id) => {
  return axios.get(`${BASE_URL}/asset/associations/${asset_id}`, asset_id).then((res) => res.data);
};

export const getRoles = () => {
  return axios.get(`${BASE_URL}/role/`).then((res) => res.data);
};

export const getUsers = () => {
  return axios.get(`${BASE_URL}/user/`).then((res) => res.data);
};

export const deleteUser = (user_id) => {
  return axios.delete(`${BASE_URL}/user/${user_id}`).then((res) => res.data);
};

export const tagNames = () => {
  return axios.get(`${BASE_URL}/tag/`).then((res) => res.data);
};

export const updateUserDetails = (body) => {
  return axios.patch(`${BASE_URL}/user/`, body).then((res) => res.data);
};

export const updatePassword = (body) => {
  return axios.patch(`${BASE_URL}/user/password`, body).then((res) => res.data);
};
export const addProject = (body) => {
  return axios.post(`${BASE_URL}/project/`, body).then((res) => res.data);
};

export const getProjects = () => {
  return axios.get(`${BASE_URL}/project/`).then((res) => res.data);
};

export const getProject = (id) => {
  return axios.get(`${BASE_URL}/project/${id}`).then((res) => res.data);
};

export const getAsset = (id) => {
  return axios.get(`${BASE_URL}/asset/${id}`).then((res) => res.data);
};

export const editProject = (id, body) => {
  return axios.patch(`${BASE_URL}/project/${id}`, body).then((res) => res.data);
};

export const deleteProject = (id) => {
  return axios.delete(`${BASE_URL}/project/${id}`).then((res) => res.data);
};

export const changeUserRole = (body) => {
  return axios.patch(`${BASE_URL}/user/role`, body).then((res) => res.data);
};

export const assetTypeLogs = () => {
  return axios.get(`${BASE_URL}/audit/asset/types`).then((res) => res.data);
};

export const userLogs = () => {
  return axios.get(`${BASE_URL}/audit/users`).then((res) => res.data);
};

export const assetLogs = () => {
  return axios.get(`${BASE_URL}/audit/assets`).then((res) => res.data);
};

export const projectLogs = () => {
  return axios.get(`${BASE_URL}/audit/projects`).then((res) => res.data);
};

export const getAssetComments = (id) => {
  return axios.get(`${BASE_URL}/comment/${id}`).then((res) => res.data);
};

export const addComment = (body) => {
  return axios.post(`${BASE_URL}/comment/`, body).then((res) => res.data);
};

export const deleteComment = (id) => {
  return axios.delete(`${BASE_URL}/comment/${id}`).then((res) => res.data);
};

export const getMyLogs = (email) => {
  return axios.post(`${BASE_URL}/audit/mylogs`, email).then((res) => res.data);
};