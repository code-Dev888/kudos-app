import React, { useState } from 'react';
import { api } from '../api/api';

export default function Login({ onLogin }) {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')

    const handleSubmit = async(e) => {
        e.preventDefault();
        setError('');

        try{
            const user = await api.login(username, password)
            onLogin(user)
        }
        catch (err) {
            setError(err.message || 'Login Failed')
        }
    };

    return (
        <div style={{ maxWidth: 400, margin: '4rem auto', textAlign: 'center' }}>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input style={{ display: 'block', margin: '1rem auto', padding: '0.5rem' }} placeholder='Username' value={username} onChange={(e) => setUsername(e.target.value)} />
                <input style={{ display: 'block', margin: '1rem auto', padding: '0.5rem' }} type='password' placeholder='Password' value={password} onChange={(e) => setPassword(e.target.value)} />
                
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <button style={{ padding: '0.5rem 1rem' }}>
                    Login
                </button>
            </form>
        </div>
    );
}