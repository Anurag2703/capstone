import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // ✅ added for navigation
import "../styles/components/LoginModal.css";

export default function LoginModal({ onClose }) {
    const [activeTab, setActiveTab] = useState("login");
    const navigate = useNavigate(); // ✅ hook for navigation

    // ✅ handle login submit
    const handleLoginSubmit = (e) => {
        e.preventDefault();
        // here you can add your auth logic later
        onClose();            // close the modal
        navigate("/chat");    // navigate to chat interface
    };

    // ✅ handle signup submit
    const handleSignupSubmit = (e) => {
        e.preventDefault();
        // here you can add signup logic later
        onClose();            // close the modal
        navigate("/chat");    // navigate to chat interface after signup
    };

    return (
        <div className="modal-overlay">
        <div className="modal-glass">
            <button className="close-btn" onClick={onClose}>✕</button>
            <div className="tab-header">
            <button
                className={activeTab === "login" ? "active" : ""}
                onClick={() => setActiveTab("login")}
            >
                Login
            </button>
            <button
                className={activeTab === "signup" ? "active" : ""}
                onClick={() => setActiveTab("signup")}
            >
                Sign Up
            </button>
            </div>

            <div className="tab-content">
            {activeTab === "login" ? (
                <form className="form" onSubmit={handleLoginSubmit}>
                <input type="email" placeholder="Email" required />
                <input type="password" placeholder="Password" required />
                <button type="submit" className="form-btn">Login</button>
                </form>
            ) : (
                <form className="form" onSubmit={handleSignupSubmit}>
                <input type="text" placeholder="Name" required />
                <input type="email" placeholder="Email" required />
                <input type="password" placeholder="Password" required />
                <button type="submit" className="form-btn">Sign Up</button>
                </form>
            )}
            </div>
        </div>
        </div>
    );
}
