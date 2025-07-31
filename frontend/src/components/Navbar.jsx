import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "../styles/components/Navbar.css";

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const navbarLinks = document.querySelectorAll(".navbar-link");
    navbarLinks.forEach(link => {
      link.addEventListener("mouseenter", () => {
        navbarLinks.forEach(otherLink => {
          if (otherLink !== link) {
            otherLink.classList.add("blur");
          }
        });
      });

      link.addEventListener("mouseleave", () => {
        navbarLinks.forEach(otherLink => {
          otherLink.classList.remove("blur");
        });
      });
    });
  }, []);

  return (
    <nav className="navbar" data-navbar>
      <div className="navbar-top">
        <Link to="/" className="logo">
          MindVerse
        </Link>
        <div
          className={`hamburger ${menuOpen ? "active" : ""}`}
          onClick={() => setMenuOpen(!menuOpen)}
        >
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>

      <ul className={`navbar-list ${menuOpen ? "show" : ""}`}>
        <li className="navbar-item">
          <Link to="/" className="navbar-link">Home</Link>
        </li>
        <li className="navbar-item">
          <Link to="/about" className="navbar-link">About</Link>
        </li>
        <li className="navbar-item">
          <Link to="/pricing" className="navbar-link">Pricing</Link>
        </li>
      </ul>
    </nav>
  );
}
