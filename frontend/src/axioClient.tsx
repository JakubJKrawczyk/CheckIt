import axios from "axios"

const axioClient = axios.create({
    baseUrl: "http://localhost:3000",
    headers: {
        'Content-Type': 'application/json',
    },
})

export default axioClient