/* 
import axios from "axios"

const axiosClient = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
    headers: {
        "Content-Type": "application/json",
    },
})

export default axiosClient */
const API_BASE = 'http://127.0.0.1:8000/api'

async function request(path, options = {}) {
    const res = await fetch(`${API_BASE}${path}`, {
        headers: {'Content-Type': 'application/json'}, ...options
    });

    const text = await res.text()
    let data;
    try {
        data = text ? JSON.parse(text): null;
    } catch (e) {
        data = text
    }

    if(!res.ok){
        const err = (data && data.error) || (data && data.detail) || res.statusText
        throw new Error(err)
    }
    return data
}

export const api = {
    login:(username, password) => request('/auth/login/', {method: 'POST', body: JSON.stringify({username, password}) }),

    getAllUsers: () => request('/users/'),
    getColleagues: (userId) => request(`/users/${userId}/`),

    giveKudo: (senderId, receiverId, message ='') => request(`/kudos/give/${senderId}/`, {method: 'POST', body:JSON.stringify({receiver_id: receiverId, message}) }),

    receivedKudos: (userId) => request(`/kudos/received/${userId}/`),
    remainingKudos: (userId) => request(`/kudos/remaining/${userId}/`),

}