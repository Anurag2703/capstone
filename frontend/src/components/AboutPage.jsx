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
            <strong>MindVerse</strong> is your AI-powered companion for emotional balance,
            reflection, and growth. Inspired by the timeless wisdom of the Bhagavad Gita,
            we blend ancient knowledge with cutting-edge AI to provide personalized guidance
            whenever you need it.
            </p>
            <p>
            Our mission is to help individuals pause, reflect, and find clarity in the
            fast-paced modern world. Whether you're feeling overwhelmed, seeking
            direction, or simply exploring your inner self, MindVerse is here to guide you.
            </p>
            <p>
            Built with ❤️ using React and Three.js, we aim to make your journey to mental
            wellness engaging, calming, and meaningful.
            </p>
        </div>
        </div>
    );
}
