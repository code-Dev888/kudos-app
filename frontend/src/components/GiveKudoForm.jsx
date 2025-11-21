import React, {useState, useEffect } from "react";
import { api } from "../api/api";

export default function GiveKudoForm({ user, onKudoGiven }) {
    const [colleagues, setColleagues] = useState([])
    const [receiverId, setReceiverId] = useState('')
    const [message, setMessage] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        api.getColleagues(user.id).then((data) => {
            // console.log('colleagues:', data); 
            setColleagues(data)
            if(data.length > 0) setReceiverId(data[0].id)
        }).catch((err) => console.log(err));
    }, [user.id]);

    const handleSubmit= async(e) => {
        e.preventDefault()
        setError('')
        setLoading(true)

        try{
            await api.giveKudo(user.id, receiverId, message)
            setReceiverId('')
            setMessage('')
            onKudoGiven()
        } catch(err) {
            setError(err.message || 'Failed to give kudo')
        } finally{
            setLoading(false)
        }
    };

    return(
        <div style={{ border: '1px solid #ccc', padding: '1rem', marginBottom: '1rem' }}>
            <h3>Give a Kudo</h3>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '0.5rem' }}>
                    <label>to:</label>
                    <select style={{ marginLeft: '0.5rem' }} value={receiverId} onChange={(e) => setReceiverId(e.target.value)} required>
                        <option value="">Select a Colleague</option>
                        {colleagues.map((c) => (
                            <option key={c.id} value={c.id}>
                                {c.username}
                            </option>
                        ))}
                    </select>
                </div>

                <div style={{ marginBottom: '0.5rem' }}>
                    <label>Message:</label>
                    <textarea style={{ display:'block', width:'100%' }} value={message} onChange={(e) => setMessage(e.target.value)} rows={3} />
                </div>

                {error && <p style={{ color: 'red' }}>{error}</p>}

                <button type="submit" disabled={loading}>
                    {loading ? 'Sending......': 'Give Kudo'}
                </button>
            </form>
        </div>
    );
}