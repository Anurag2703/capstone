import React, { useState } from 'react';
import Loader from './Loader';
import '../styles/components/gitaViewer.css';

export default function GitaViewer() {
    const [input, setInput] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const fetchGita = async () => {
        setLoading(true);
        setResult(null);
        try {
            const res = await fetch('http://127.0.0.1:8000/gita/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sentiment: input })
            });
            const data = await res.json();
            setResult(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="gita-viewer">
            {loading && <Loader />}

            <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder="Enter sentiment..."
            />
            <button onClick={fetchGita}>Get Verse</button>

            {result && result.verse && (
                <div className="verse-card">
                <h2>Chapter {result.chapter}, Verse {result.verse_number}</h2>
                <p>{result.verse}</p>
                </div>
            )}
        </div>
    );
}
