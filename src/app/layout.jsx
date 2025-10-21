import './globals.css';
import { Geist, Geist_Mono } from 'next/font/google';

const geist = Geist({ subsets: ['latin'], weight: '400' });
const geistMono = Geist_Mono({ subsets: ['latin'], weight: '400' });

export const metadata = {
  title: 'OSCC Prediction App',
  description: 'Predict N stage and ENE risk using clinical parameters',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={geist.className}>
      <body className="min-h-screen flex flex-col bg-gradient-to-br from-blue-50 via-teal-50 to-cyan-50">
        {/* Global Header */}
        <header className="bg-gradient-to-r from-blue-600 to-teal-600 text-white p-6 shadow-lg">
          <h1 className="text-3xl font-bold">OSCC Prediction Model</h1>
          <p className="text-blue-100 mt-1">
            Predict N stage and extranodal extension risk using clinical parameters
          </p>
        </header>

        {/* Page content */}
        <main className="flex-1 w-full max-w-6xl mx-auto p-4 md:p-8">
          {children}
        </main>

        {/* Global Footer */}
        <footer className="bg-gray-800 text-white p-4 text-center mt-auto">
          © {new Date().getFullYear()} OSCC Prediction App
        </footer>
      </body>
    </html>
  );
}
