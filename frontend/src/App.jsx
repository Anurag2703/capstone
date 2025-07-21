import React from 'react';
import BackgroundScene from './components/BackgroundScene';
import Navbar from './components/Navbar';
import './styles/App.css';

function App() {
  return (
    <>
      <Navbar />
      <div className="app-container">
        <BackgroundScene />
        <div className="content-overlay">
          <h1>Proactive Mental Wellness Assistant</h1>
          <p className="tagline">
            Your AI-powered companion for emotional balance, reflection, and growth.
          </p>


          {/* HERO SECTION */}
          <div className="hero-glass">
            <div className="hero-section">
              <p>
                Explore verses from the Bhagavad Gita, tailored to your current emotions.
                Whether you’re feeling overwhelmed, seeking clarity, or practicing forgiveness—let wisdom guide you.
              </p>
              <p>
                Our assistant helps you pause, reflect, and find inner calm through timeless teachings.
                It’s more than advice—it’s a journey toward balance and self-discovery.
              </p>
              <p>
                Designed for anyone seeking peace in a busy world, this tool blends ancient wisdom
                with modern AI to give you personalized guidance whenever you need it.
              </p>
            </div>
          </div>
        </div>
      </div>


      {/* FOOTER */}
      <hr className="footer-separator" />

      <footer className="footer">
        <p>
          © {new Date().getFullYear()} Proactive Mental Wellness Assistant. All rights reserved.
        </p>
        <p>
          <a href="#about">Home</a> | <a href="#about">About</a> | <a href="#contact">Contact</a>
        </p>
      </footer>
    </>
  );
}

export default App;
