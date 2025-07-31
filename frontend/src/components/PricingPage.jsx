import React from "react";
import BackgroundScene from "../components/BackgroundScene";
import "../styles/components/PricingPage.css";

const PricingPage = () => {
    return (
        <div className="pricing-container">
        <BackgroundScene />
        <div className="pricing-content">
            <h1 className="pricing-title">Our Plans</h1>
            <p className="pricing-subtitle">
            Choose a plan that fits your needs and level up your journey.
            </p>

            <div className="pricing-cards">
            {/* Free Plan */}
            <div className="pricing-card glass-card">
                <h2>Free</h2>
                <p className="price">$0 <span>/month</span></p>
                <ul>
                <li>✅ Explore basic features</li>
                <li>✅ Limited AI usage</li>
                <li>✅ Access on all devices</li>
                </ul>
                <button className="pricing-btn">Your Plan</button>
            </div>

            {/* Plus Plan */}
            <div className="pricing-card glass-card highlight">
                <h2>Plus</h2>
                <p className="price">$20 <span>/month</span></p>
                <ul>
                <li>✅ Everything in Free</li>
                <li>✅ Extended usage limits</li>
                <li>✅ Priority access</li>
                <li>✅ Access to advanced features</li>
                </ul>
                <button className="pricing-btn active">Get Plus</button>
            </div>

            {/* Pro Plan */}
            <div className="pricing-card glass-card">
                <h2>Pro</h2>
                <p className="price">$200 <span>/month</span></p>
                <ul>
                <li>✅ Everything in Plus</li>
                <li>✅ Unlimited AI access</li>
                <li>✅ Advanced analytics</li>
                <li>✅ Exclusive features</li>
                </ul>
                <button className="pricing-btn">Get Pro</button>
            </div>
            </div>
        </div>
        </div>
    );
};

export default PricingPage;
