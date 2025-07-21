import axios from 'axios'

const axiosInstance = axios.create({
    baseURL: '/', // thanks to Vite proxy
    headers: {
        'Content-Type': 'application/json'
    }
})

export default axiosInstance