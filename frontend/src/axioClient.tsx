import axios from "axios"

const axioClient = axios.create({
    baseURL: "http://localhost:21370/api",
    headers: {
        'Content-Type': 'application/json',
    },
})

export default axioClient