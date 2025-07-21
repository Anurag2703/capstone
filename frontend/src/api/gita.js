import axiosInstance from './axiosInstance'

export const getVerseBySentiment = async (sentiment) => {
    try {
        const response = await axiosInstance.post('/gita/', {
            sentiment
        })
        return response.data
    } catch (err) {
        console.error('Error fetching Gita verse:', err)
        return null
    }
}
