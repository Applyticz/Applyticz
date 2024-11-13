import { useNavigate } from 'react-router-dom';
import PublicHeader from './PublicHeader';
import './LandingPage.css'; // Import the new CSS file
import { FaRocket, FaChartLine, FaClipboardList, FaUserCheck } from 'react-icons/fa'; // Import icons

function LandingPage(){
    const navigate = useNavigate();

    return(
        <>
            <PublicHeader />
            <div className="landing-container" style={{ backgroundImage: 'url("/path/to/your/background.jpg")', backgroundSize: 'cover', color: '#fff', padding: '50px 20px' }}>
                <h1 className="main-title" style={{ fontSize: '3.5rem', textShadow: '2px 2px 4px rgba(0, 0, 0, 0.7)' }}>Complete Autonomy</h1>
                <p className="description" style={{ fontSize: '1.3rem', marginBottom: '30px' }}>Applytics allows you to connect your Gmail and Outlook account so that you never have to manually track applications again! Our software automatically parses your email inbox for job applications, updates, and responses, allowing you to focus on what really matters - landing your dream job.</p>
                
                <div className="feature" style={{ backgroundColor: '#f0f0f0', padding: '15px', borderRadius: '5px', margin: '10px 0' }}>
                    <FaRocket size={50} color="#ff5722" />
                    <h2 className="feature-title" style={{ color: '#333' }}>Powered By Data</h2>
                    <p className="feature-description" style={{ color: '#555' }}>Every tracked application goes through our carefully curated metrics algorithm to ensure personalized data based on your own results.</p>
                </div>

                <div className="feature" style={{ backgroundColor: '#f0f0f0', padding: '15px', borderRadius: '5px', margin: '10px 0' }}>
                    <FaChartLine size={50} color="#ff5722" />
                    <h2 className="feature-title" style={{ color: '#333' }}>Tracking Made Easy</h2>
                    <p className="feature-description" style={{ color: '#555' }}>Easily navigate through a variety of application statuses, interview stages, offers, and more!</p>
                </div>

                <div className="feature" style={{ backgroundColor: '#f0f0f0', padding: '15px', borderRadius: '5px', margin: '10px 0' }}>
                    <FaClipboardList size={50} color="#ff5722" />
                    <h2 className="feature-title" style={{ color: '#333' }}>Stay Organized</h2>
                    <p className="feature-description" style={{ color: '#555' }}>Keep all your applications in one place and never miss an opportunity again.</p>
                </div>

                <h1 className="cta-title" style={{ fontSize: '3rem', textShadow: '2px 2px 4px rgba(0, 0, 0, 0.7)', marginTop: '40px' }}>Start Today! It's 100% FREE</h1>
                <button className="register-button" style={{ padding: '15px 30px', fontSize: '1.5rem', backgroundColor: '#ff5722', color: '#fff', borderRadius: '5px', transition: 'background-color 0.3s' }} onClick={() => navigate("/register")}>Register Now</button>
                <p className="login-cta" style={{ marginTop: '20px' }}>Already have an account?</p>
                <button className="register-button" style={{ padding: '10px 20px', fontSize: '1.2rem', backgroundColor: '#007BFF', color: '#fff', borderRadius: '5px', transition: 'background-color 0.3s' }} onClick={() => navigate("/login")}>Login</button>
            </div>
        </>
    );
}

export default LandingPage;
