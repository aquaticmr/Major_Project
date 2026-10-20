import React from 'react';
import { SignIn } from '@clerk/clerk-react';

export const SignInPage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-6">
          <div className="inline-block p-3 rounded-2xl bg-emerald-500 text-white font-bold text-2xl mb-2">
            FX
          </div>
          <h1 className="text-2xl font-bold text-white">Sign In to FinoAddWise-X</h1>
          <p className="text-sm text-slate-400 mt-1">Grounded Financial Advisory & Threat Detection Co-Pilot</p>
        </div>
        <div className="flex justify-center">
          <SignIn routing="path" path="/sign-in" signUpUrl="/sign-up" redirectUrl="/dashboard" />
        </div>
      </div>
    </div>
  );
};
