import React from 'react';
import '../styles/components/loader.css';

export default function Loader() {
    return (
        <div className="loader-overlay">
        <div className="spinner"></div>
        </div>
    );
}
