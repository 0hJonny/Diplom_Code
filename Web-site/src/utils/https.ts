import axios from "axios";
import  type { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from "axios";


// console.log('import.meta.env: ', import.meta.env.BASE_URL);


// 创建 axios 实例
let service: AxiosInstance | any;
if (import.meta.env.MODE === "development") {
  service = axios.create({
    baseURL: "/api/v1", // api 的 base_url
    timeout: 50000 // 请求超时时间
  });
} else {
  // 生产环境下
  service = axios.create({
    baseURL: "/api/v1",
    timeout: 50000
  });
}

// request 拦截器 axios 的一些配置
service.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // const token = getAuthToken();
    // if (token) {
    //   config.headers = {
    //     ...config.headers,
    //     Authorization: `Bearer ${token}`
    //   };
    // }
    return config;
  },
  (error: any) => {
    // Do something with request error
    console.error("error:", error); // for debug
    Promise.reject(error);
  }
);

// respone 拦截器 axios 的一些配置
service.interceptors.response.use(
  (res: AxiosResponse) => {
    // Some example codes here:
    // code == 0: success
    if (res.status === 200) {
      const {data} = res
      return Promise.resolve(data);
    } else {
      console.error("error:", res);
      return Promise.reject(new Error(res.data.message || "Error"));
    }
  },
  (error: any) => Promise.reject(error)
);

export default service;