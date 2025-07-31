// frontend/src/components/AboutPage.jsx
import React from "react";
import BackgroundScene from "./BackgroundScene";
import "../styles/AboutPage.css";

export default function AboutPage() {
    return (
        <div className="about-page">
        <BackgroundScene />
        <div className="about-overlay">
            <h1>About Us</h1>
            <p>
                <strong>MindVerse</strong> is a thoughtful fusion of ancient wisdom and modern AI, crafted to support emotional well-being and inner reflection. Inspired by the enduring truths of the Bhagavad Gita, we aim to help you reconnect with yourself—one meaningful interaction at a time.
            </p>
            <p>
                We believe that amidst the noise of modern life, everyone deserves a quiet space for clarity. Whether you're navigating stress, burnout, anxiety, or just in need of perspective, MindVerse offers gentle guidance drawn from timeless verses and personalized support through advanced AI.
            </p>
            <p>
                Our platform is more than just a tool—it's a companion for mindful living. With each response, we invite you to reflect, heal, and grow—at your own pace.
            </p>
        </div>
        </div>
    );
}
