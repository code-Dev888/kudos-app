import React, {useState, useEffect, useMemo } from "react";
import { api } from "../api/api";

export default function ReceivedKudos({ userId, refreshCounter = 0 }) {
    const [kudos, setKudos] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        let mounted = true
        setLoading(true)

        api.receivedKudos(userId).then((data) => {
            if(mounted) setKudos(data || [])
        }).catch((err) => console.log(err)).finally(() => mounted && setLoading(false));

        return () => {mounted = false}
    }, [userId, refreshCounter])

    const renderedKudos = useMemo(() =>{
        return kudos.map((k) =>(
           <li key={k.id} style={{ borderBottom:'1px solid #eee', padding:'0.5rem 0' }}>
                        <p><strong>From: </strong>{k.sender?.username}</p>
                        <p><strong>Message: </strong>{k.message}</p>

                        <p style={{ fontSize:'0.8rem', color:'#666' }}>
                            {new Date(k.created_at).toLocaleString()}
                        </p>
            </li>
        ));
    }, [kudos]);

    if(loading) return <p>Loading.........</p>

    if(kudos.length === 0) return <p>No kudos received</p>

    return(
        <div style={{ border: '1px solid #ccc', padding:'1rem', marginTop: '2rem'}}>
            <h3>Kudos Received</h3>
            <ul style={{ listStyle: 'none', padding:0, margin:0 }}>{renderedKudos}</ul>
        </div>
    );
}
