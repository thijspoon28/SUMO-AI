import { API_BASE_URL } from "@/config";
import axios from "axios";
import { camelizeKeys, decamelizeKeys } from 'humps';

const rawApi = axios.create({
    baseURL: API_BASE_URL
});

rawApi.interceptors.request.use(config => {
    if (config.data) {
        config.data = decamelizeKeys(config.data);
    }
    return config;
});

rawApi.interceptors.response.use(response => {
    if (response.data) {
        response.data = camelizeKeys(response.data);
    }
    return response;
});

export default rawApi;
