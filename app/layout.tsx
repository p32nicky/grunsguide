import type { Metadata } from "next";
import { Geist } from "next/font/google";
import "./globals.css";

const geist = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const SITE_URL = "https://grunsgummies.site";
const AFFILIATE = "https://www.gruns.co/pages/vip?snowball=NICK67621";

export const metadata: Metadata = {
  title: { default: "Grüns Gummies Reviews, Benefits & Guides", template: "%s | Grüns Guide" },
  description: "Honest Grüns greens gummies reviews, ingredient breakdowns, benefits, comparisons, and health guides. Everything you need to know before buying.",
  metadataBase: new URL(SITE_URL),
  openGraph: { siteName: "Grüns Guide", type: "website", locale: "en_US" },
  twitter: { card: "summary_large_image" },
  robots: { index: true, follow: true, googleBot: { index: true, follow: true } },
  verification: { google: "0MHHKj96WNxC1aqgbOWyWS5d-flt0865XhT2Ly4Lopg" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={geist.variable}>
      <head>
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-EHW9Q0YYJN"></script>
        <script dangerouslySetInnerHTML={{ __html: `
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'G-EHW9Q0YYJN');
        ` }} />
      </head>
      <body className="min-h-screen bg-white text-gray-900 antialiased">
        {/* Sticky Bear Sidebar */}
        <div className="hidden lg:flex fixed right-6 top-1/3 flex-col items-center z-20">
          <div className="bg-green-600 rounded-2xl p-4 text-center shadow-lg sticky top-1/3">
            <div className="text-5xl mb-2">🐻</div>
            <div className="text-yellow-300 font-bold text-lg">grüns</div>
          </div>
        </div>
        <header className="border-b border-gray-100 bg-white sticky top-0 z-10">
          <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
            <a href="/" className="font-bold text-lg text-green-700 hover:text-green-800">🐻 Grüns Guide</a>
            <a href={AFFILIATE} target="_blank" rel="noopener noreferrer"
              className="text-sm bg-green-700 hover:bg-green-800 text-white font-semibold px-4 py-2 rounded-full transition-colors">
              Try Grüns →
            </a>
          </div>
        </header>
        <div className="bg-yellow-50 border-b border-yellow-200 text-center text-xs text-yellow-800 py-2 px-4">
          <strong>Affiliate Disclosure:</strong> We may earn a commission when you purchase through our links, at no extra cost to you.
        </div>
        <main>{children}</main>
        <footer className="border-t border-gray-100 mt-16 py-8 text-center text-sm text-gray-500">
          <p>Grüns Guide is an independent review site. We may earn a commission when you use our links.</p>
          <p className="mt-2 flex items-center justify-center gap-4">
            <a href="/" className="underline hover:text-gray-700">All Guides</a>
            <a href="/affiliate-disclosure" className="underline hover:text-gray-700">Affiliate Disclosure</a>
            <a href="/privacy-policy" className="underline hover:text-gray-700">Privacy Policy</a>
          </p>
          <p className="mt-3">
            <strong>Contact:</strong> <a href="mailto:nickdavies100@gmail.com" className="text-green-700 hover:text-green-800 underline">nickdavies100@gmail.com</a>
          </p>
        </footer>
      </body>
    </html>
  );
}
