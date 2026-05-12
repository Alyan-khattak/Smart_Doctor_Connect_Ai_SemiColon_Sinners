import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata: Metadata = {
  title: "Smart Doctor Connect AI — Find the Right Doctor in Pakistan",
  description:
    "AI-powered doctor discovery, appointment booking, and patient support system for Pakistan. Find the right specialist in your city instantly.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen bg-slate-50">
        <Navbar />
        <main className="min-h-[calc(100vh-4rem)]">{children}</main>
        <footer className="bg-slate-900 text-slate-400 py-8 mt-12">
          <div className="max-w-7xl mx-auto px-4 text-center text-sm">
            <p className="font-semibold text-white mb-1">Smart Doctor Connect AI</p>
            <p>AI-powered doctor discovery for Pakistan — Hackathon MVP 2026</p>
            <p className="mt-2 text-xs text-slate-500">
              This system helps find doctors. It does not provide diagnosis or emergency medical care.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
