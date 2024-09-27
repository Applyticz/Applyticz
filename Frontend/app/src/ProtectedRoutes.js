import { useEffect, useState } from "react";
import { useNavigate, Outlet } from "react-router-dom";

const ProtectedRoutes = ({ children }) => {
  const navigate = useNavigate();
  const [isVerified, setIsVerified] = useState(false);

  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem('access_token');
      //console.log(token);
      try {
        const response = await fetch(`http://localhost:8000/auth/verify-token/${token}`);
        if (!response.ok) {
          throw new Error('Token verification failed');
        }
        setIsVerified(true);
      } catch (error) {
        localStorage.removeItem('access_token');
        navigate('/login');
      }
    };
    verifyToken();
  }, [navigate]);

  if (!isVerified) {
    return null; // or a loading spinner
  }

  return (
    <>
      {children}
      <Outlet />
    </>
  );
};

export default ProtectedRoutes;
