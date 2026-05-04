import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "./pages/NotFound.tsx";
import PetScan from "./pages/PetScan.tsx";
import AdminLayout from "./components/AdminLayout.tsx";
import PetsList from "./pages/admin/PetsList.tsx";
import PetCreate from "./pages/admin/PetCreate.tsx";
import PetDetail from "./pages/admin/PetDetail.tsx";
import PetQr from "./pages/admin/PetQr.tsx";

import Login from "./pages/Login.tsx";
import ProtectedRoute from "./components/ProtectedRoute.tsx";
import { isAdmin } from "./lib/auth";

const queryClient = new QueryClient();

const RootRedirect = () => <Navigate to={isAdmin() ? "/admin" : "/login"} replace />;

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<RootRedirect />} />
          <Route path="/pet/:id" element={<PetScan />} />
          <Route path="/login" element={<Login />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/admin" element={<AdminLayout />}>
              <Route index element={<PetsList />} />
              <Route path="new" element={<PetCreate />} />
              
              <Route path="pets/:id" element={<PetDetail />} />
              <Route path="pets/:id/qr" element={<PetQr />} />
            </Route>
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
