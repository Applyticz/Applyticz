import { useEffect, useState } from "react";
import { useNavigate, Outlet } from "react-router-dom";
import useAuth from "./utils";

const ProtectedRoutes = ({ children }) => {
  const navigate = useNavigate();
  const [isVerified, setIsVerified] = useState(false);
  const { getValidToken } = useAuth();


  useEffect(() => {
    const verifyToken = async () => {
      const isValid = await getValidToken();
      if (!isValid) {
        navigate("/login");
      } else {
        setIsVerified(true);
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
