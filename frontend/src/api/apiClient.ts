// apiClient.ts
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { camelizeKeys, decamelizeKeys } from 'humps';
class ApiClient {
  private instance: AxiosInstance;
  private auth!: ReturnType<typeof useAuthStore>;

  constructor(baseURL: string, config?: AxiosRequestConfig) {
    this.instance = axios.create({
      baseURL,
      ...config, // Allow overriding default config
    });

    // Add interceptors for request/response handling if needed
    this.instance.interceptors.request.use(async (config) => {
      if (config.data) {
        config.data = decamelizeKeys(config.data);
      }

      config = await this.auth.applyHeaders(config)
      return config;
    });

    this.instance.interceptors.response.use(
      (response) => {
        if (response.data) {
          response.data = camelizeKeys(response.data);
        }

        return response
      },
      (error) => {
        // Handle errors globally
        return Promise.reject(error);
      }
    );
  }

  public setAuthStore(store: ReturnType<typeof useAuthStore>) {
    this.auth = store;
  }

  public async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.instance.get(url, config);
    return response.data;
  }

  public async post<T, B>(url: string, data?: B, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.instance.post(url, data, config);
    return response.data;
  }

  // Add other methods (put, delete, patch) as needed
}

export default ApiClient;
