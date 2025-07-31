import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import BackgroundScene from './components/BackgroundScene';
import Navbar from './components/Navbar';
import LoginModal from './components/LoginModal';
import PricingPage from './components/PricingPage';
import AboutPage from './components/AboutPage'; // ✅ import your new About page
import ChatInterface from "./components/ChatInterface";
import './styles/App.css';

function HomeContent({ setShowLoginModal }) {
  return (
    <>
      <div className="app-container">
        <BackgroundScene />

        {/* HEADER SECTION */}
        <div className="content-overlay">
          <h1>MindVerse</h1>
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

            <div className="hero-button-container">
              <button onClick={() => setShowLoginModal(true)}>Try Us</button>
            </div>
          </div>
        </div>



        {/* DIVINE SECTION */}
        <div className="content-overlay" style={{ marginTop: '120px' }}>
          <h1>Discover the Wisdom of the Cantos</h1>

          <div className="hero-glass">
            <div className="hero-section">
              <p>
                In the context of the Śrīmad-Bhāgavatam, a Canto is a spiritually rich chapter—each one a divine thread in the grand tapestry of creation, dharma, and devotion.
              </p>
              <p>
                Here you'll find beautifully distilled summaries of the Cantos, drawn from the sacred texts. These narratives—filled with divine incarnations, cosmic mysteries, and spiritual insights—are curated to guide modern readers through the timeless essence of Hindu wisdom.
              </p>
              <p>
                For students, seekers, and the curious alike, these stories are more than scripture—they are a guide to living with purpose, compassion, and clarity in a distracted world. They plant seeds of strength, character, and devotion that grow with you over time.
              </p>
            </div>

            <div className="hero-button-container">
              <button onClick={() => window.open("https://spiritualguidances.netlify.app/", "_blank")}>Explore Now</button>
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
          <a href="/">Home</a> | <a href="/about">About</a> | <a href="#contact">Contact</a>
        </p>
      </footer>
    </>
  );
}

function App() {
  const [showLoginModal, setShowLoginModal] = useState(false);

  return (
    <>
      <Navbar />

      {/* ROUTES */}
      <Routes>
        <Route
          path="/"
          element={<HomeContent setShowLoginModal={setShowLoginModal} />}
        />
        <Route path="/pricing" element={<PricingPage />} />
        <Route path="/about" element={<AboutPage />} /> {/* ✅ new About page route */}
        <Route path="/chat" element={<ChatInterface />} />
      </Routes>

      {/* ✅ Modal */}
      {showLoginModal && <LoginModal onClose={() => setShowLoginModal(false)} />}
    </>
  );
}

export default App;
