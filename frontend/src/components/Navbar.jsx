import React, { useEffect, useState } from "react";
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
        <a href="#" className="logo">
          Jujutsu Kaisen
        </a>
        {/* Hamburger */}
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
          <a href="#Sukuna" className="navbar-link" data-navbar-link>
            Home
          </a>
        </li>
        <li className="navbar-item">
          <a href="/gojo.html" className="navbar-link" data-navbar-link>
            About
          </a>
        </li>
        <li className="navbar-item">
          <a href="#Toji" className="navbar-link" data-navbar-link>
            Therapy
          </a>
        </li>
        <li className="navbar-item">
          <a href="#Itadori" className="navbar-link" data-navbar-link>
            Login
          </a>
        </li>
      </ul>
    </nav>
  );
}
