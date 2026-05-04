import { Navigate, Outlet, useLocation } from "react-router-dom";
import { isAdmin } from "@/lib/auth";

export default function ProtectedRoute() {
  const location = useLocation();
  if (!isAdmin()) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }
  return <Outlet />;
}
