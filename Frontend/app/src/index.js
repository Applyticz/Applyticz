import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { AuthProvider } from "./authContext";

const root = ReactDOM.createRoot(document.getElementById("root")); // Create a root.

root.render(
  <AuthProvider>
    <App />
  </AuthProvider>
);
