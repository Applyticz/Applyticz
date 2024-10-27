import { useNavigate } from 'react-router-dom';
import PublicHeader from './PublicHeader';
import './LandingPage.css'; // Import the new CSS file

function LandingPage(){
    const navigate = useNavigate();

    return(
        <>
            <PublicHeader />
            <div className="landing-container">
                <h1 className="main-title">Complete Autonomy</h1>
                <p className="description">Applytics allows you to connect your gmail account so that you never have to manually track applications again! Our software automatically
                    parses your email inbox for job applications, updates, and responses, allowing you to focus on what really matters - Landing your dream job
                </p>
                
                <h1 className="main-title">Powered By Data</h1>
                <p className="description">Every tracked application goes through our carefully curated metrics algorithm to ensure personalized data based on your own results</p>

                <h1 className="main-title">Tracking Made Easy</h1>
                <p className="description">Easily navigate through a variety of application statuses, interview stages, offers, and more!</p>

                <h1 className="main-title">Applytics</h1>
                <p className="cta">Start today! It's 100% FREE</p>
                <button className="register-button" onClick={() => navigate("/register")}>Register</button>
            </div>
        </>
    );
}

export default LandingPage;
