"use client";
import Link from "next/link";
import { useState, useEffect } from "react";
import { Stethoscope, Menu, X, LogOut } from "lucide-react";
import { usePathname, useRouter } from "next/navigation";

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const [isDoctorLoggedIn, setIsDoctorLoggedIn] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const token = localStorage.getItem("doctor_token");
    setIsDoctorLoggedIn(!!token);
  }, [pathname]);

  const handleLogout = () => {
    localStorage.removeItem("doctor_token");
    setIsDoctorLoggedIn(false);
    router.push("/");
  };

  const patientLinks = [
    { href: "/", label: "Home" },
    { href: "/search", label: "Find Doctor" },
  ];

  const loggedOutLinks = [
    { href: "/doctor/login", label: "Doctor Login" },
    { href: "/doctor/register", label: "Doctor Register" },
  ];

  const loggedInLinks = [
    { href: "/dashboard/doctor", label: "Dashboard" },
    { href: "/doctor/profile", label: "Profile" },
  ];

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-sky-500 rounded-lg flex items-center justify-center">
              <Stethoscope className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-slate-900 text-sm sm:text-base">
              Smart Doctor Connect <span className="text-sky-500">AI</span>
            </span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-6">
            {isDoctorLoggedIn ? (
              <>
                {loggedInLinks.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    className="text-sm font-medium text-slate-600 hover:text-sky-600 transition-colors"
                  >
                    {link.label}
                  </Link>
                ))}
                <button
                  onClick={handleLogout}
                  className="text-sm font-medium text-slate-600 hover:text-red-500 transition-colors flex items-center gap-1"
                >
                  <LogOut className="w-4 h-4" /> Logout
                </button>
              </>
            ) : (
              <>
                {patientLinks.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    className="text-sm font-medium text-slate-600 hover:text-sky-600 transition-colors"
                  >
                    {link.label}
                  </Link>
                ))}
                {loggedOutLinks.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    className="text-sm font-medium text-slate-600 hover:text-sky-600 transition-colors"
                  >
                    {link.label}
                  </Link>
                ))}
              </>
            )}

            {!isDoctorLoggedIn && (
              <Link
                href="/search"
                className="bg-sky-500 hover:bg-sky-600 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-colors ml-2"
              >
                Find a Doctor
              </Link>
            )}
          </div>

          {/* Mobile toggle */}
          <button
            onClick={() => setOpen(!open)}
            className="md:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100"
            aria-label="Toggle menu"
          >
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

        {/* Mobile nav */}
        {open && (
          <div className="md:hidden pb-4 flex flex-col gap-2">
            {[...(isDoctorLoggedIn ? loggedInLinks : [...patientLinks, ...loggedOutLinks])].map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setOpen(false)}
                className="px-3 py-2 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-100"
              >
                {link.label}
              </Link>
            ))}
            {isDoctorLoggedIn && (
              <button
                onClick={() => {
                  setOpen(false);
                  handleLogout();
                }}
                className="px-3 py-2 rounded-lg text-sm font-medium text-red-600 hover:bg-red-50 text-left"
              >
                Logout
              </button>
            )}
          </div>
        )}
      </div>
    </nav>
  );
}
