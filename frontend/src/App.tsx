import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ClerkProvider, SignedIn, SignedOut, useAuth } from '@clerk/clerk-react';

import { setupAxiosAuth } from './services/api';
import { DashboardLayout } from './layouts/DashboardLayout';
import { OverviewPage } from './pages/OverviewPage';
import { DocumentsPage } from './pages/DocumentsPage';
import { RAGAssistantPage } from './pages/RAGAssistantPage';
import { AdvisoryPage } from './pages/AdvisoryPage';
import { CardsPage } from './pages/CardsPage';
import { FraudPage } from './pages/FraudPage';
import { TrustPage } from './pages/TrustPage';
import { ModelsPage } from './pages/ModelsPage';
import { SignInPage } from './pages/SignInPage';
import { SignUpPage } from './pages/SignUpPage';

const CLERK_PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY || 'pk_test_demo_placeholder_key';

const AuthSetup: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { getToken } = useAuth();

  useEffect(() => {
    setupAxiosAuth(getToken);
  }, [getToken]);

  return <>{children}</>;
};

export const App: React.FC = () => {
  return (
    <ClerkProvider publishableKey={CLERK_PUBLISHABLE_KEY}>
      <AuthSetup>
        <BrowserRouter>
          <Routes>
            {/* Public Auth Routes */}
            <Route path="/sign-in/*" element={<SignInPage />} />
            <Route path="/sign-up/*" element={<SignUpPage />} />

            {/* Protected Dashboard Routes */}
            <Route
              path="/dashboard"
              element={
                <>
                  <SignedIn>
                    <DashboardLayout />
                  </SignedIn>
                  <SignedOut>
                    {/* Fallback to Dashboard in local test mode if Clerk key is dummy, otherwise redirect to /sign-in */}
                    {CLERK_PUBLISHABLE_KEY.includes('demo') ? (
                      <DashboardLayout />
                    ) : (
                      <Navigate to="/sign-in" replace />
                    )}
                  </SignedOut>
                </>
              }
            >
              <Route index element={<OverviewPage />} />
              <Route path="documents" element={<DocumentsPage />} />
              <Route path="rag" element={<RAGAssistantPage />} />
              <Route path="advisory" element={<AdvisoryPage />} />
              <Route path="cards" element={<CardsPage />} />
              <Route path="fraud" element={<FraudPage />} />
              <Route path="trust" element={<TrustPage />} />
              <Route path="models" element={<ModelsPage />} />
              <Route path="alerts" element={<OverviewPage />} />
            </Route>

            {/* Root redirect */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthSetup>
    </ClerkProvider>
  );
};

export default App;
