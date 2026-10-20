import React from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { UserButton, useUser } from '@clerk/clerk-react';
import { 
  LayoutDashboard, FileText, MessageSquareQuote, ShieldAlert, 
  CreditCard, Award, Activity, Bell 
} from 'lucide-react';

export const DashboardLayout: React.FC = () => {
  const location = useLocation();
  const { user } = useUser();

  const navItems = [
    { label: 'Overview', path: '/dashboard', icon: LayoutDashboard },
    { label: 'Document Vault', path: '/dashboard/documents', icon: FileText },
    { label: 'Grounded RAG', path: '/dashboard/rag', icon: MessageSquareQuote },
    { label: 'Advisory & Budget', path: '/dashboard/advisory', icon: Activity },
    { label: 'Card Recommender', path: '/dashboard/cards', icon: CreditCard },
    { label: 'Threat & URL Fraud', path: '/dashboard/fraud', icon: ShieldAlert },
    { label: 'Trust Scoring', path: '/dashboard/trust', icon: Award },
    { label: 'Model Registry', path: '/dashboard/models', icon: Activity },
  ];

  return (
    <div className="flex h-screen bg-slate-100">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-slate-100 flex flex-col shadow-lg">
        <div className="p-5 border-b border-slate-800 flex items-center space-x-3">
          <div className="w-8 h-8 rounded bg-emerald-500 flex items-center justify-center font-bold text-white">
            FX
          </div>
          <div>
            <h1 className="font-bold text-lg tracking-tight">FinoAddWise-X</h1>
            <p className="text-xs text-slate-400">Financial Co-Pilot</p>
          </div>
        </div>

        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-emerald-600 text-white'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <Icon className="w-4 h-4 mr-3" />
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-slate-800 flex items-center justify-between">
          <div className="flex items-center space-x-3 overflow-hidden">
            <UserButton afterSignOutUrl="/sign-in" />
            <div className="text-xs truncate">
              <p className="font-medium text-white truncate">{user?.fullName || 'User Profile'}</p>
              <p className="text-slate-400 truncate">{user?.primaryEmailAddress?.emailAddress || 'Verified Identity'}</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between shadow-sm">
          <div className="flex items-center space-x-2 text-sm text-slate-600">
            <span className="font-semibold text-slate-800">Co-Pilot Mode:</span>
            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-100 text-emerald-800">
              Low-Hallucination & AES-256 Vault
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <Link to="/dashboard/alerts" className="text-slate-500 hover:text-slate-700 relative">
              <Bell className="w-5 h-5" />
            </Link>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto p-6 bg-slate-50">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
