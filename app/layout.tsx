import type { Metadata } from "next";
import { Geist } from "next/font/google";
import ExitPopup from "./components/ExitPopup";
import "./globals.css";

const geist = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
import { SITE_URL } from "@/lib/site";
const AFFILIATE = "https://www.gruns.co/pages/vip?snowball=NICK67621";

export const metadata: Metadata = {
  // Site identity deliberately carries no brand name. "Grüns Guide" on a
  // grunssite.vercel.app domain read as an official property, which is what
  // the Marq Vision IP notice (2026-10-28) objected to. Reviewing the product
  // by name inside articles is nominative use and stays; naming the SITE after
  // someone else's trademark is not. Do not put "Grüns" back in the site name,
  // domain, or og:siteName.
  title: {
    default: "Greens Gummy Guide — Independent Reviews & Comparisons",
    template: "%s | Greens Gummy Guide",
  },
  description: "Independent reviews, ingredient breakdowns and comparisons of greens gummy supplements. Not affiliated with any brand we cover.",
  metadataBase: new URL(SITE_URL),
  openGraph: {
    siteName: "Greens Gummy Guide",
    type: "website",
    locale: "en_US",
    title: "Greens Gummy Guide — Independent Reviews & Comparisons",
    description: "Independent guides to greens gummy supplements — reviews, ingredients, benefits and comparisons.",
    // No og:image — the previous one was the brand's own product photo,
    // removed 2026-10-28 after an IP notice. Do not point this at any
    // Grüns-owned asset.
  },
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
        <ExitPopup />
        {/* Sticky CTA. The previous version used the brand's product photo
            plus their lowercase "grüns" wordmark in their own yellow — i.e.
            reproducing their logo treatment. Removed 2026-10-28 after the
            Marq Vision IP notice. Text-only CTA, no brand styling. */}
        <div className="hidden lg:block fixed right-6 top-32 z-20 w-56">
          <div className="bg-white border border-gray-200 rounded-2xl p-4 text-center shadow-xl sticky top-32">
            <p className="text-gray-900 text-sm mb-1 font-bold">Greens gummies</p>
            <p className="text-gray-600 text-xs mb-4">Compare options and current pricing.</p>
            <a href={AFFILIATE} target="_blank" rel="noopener noreferrer sponsored nofollow"
              className="inline-block w-full bg-green-700 hover:bg-green-800 text-white font-bold py-2 px-3 rounded-full text-sm transition-colors">
              See pricing →
            </a>
            <p className="text-[10px] text-gray-400 mt-2">Affiliate link</p>
          </div>
        </div>
        <header className="border-b border-gray-100 bg-white sticky top-0 z-10">
          <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
            <a href="/" className="font-bold text-lg text-green-700 hover:text-green-800">Greens Gummy Guide</a>
            <a href={AFFILIATE} target="_blank" rel="noopener noreferrer sponsored nofollow"
              className="text-sm bg-green-700 hover:bg-green-800 text-white font-semibold px-4 py-2 rounded-full transition-colors">
              See pricing →
            </a>
          </div>
        </header>
        <main>{children}</main>
        <footer className="border-t border-gray-100 mt-16 py-8 text-center text-sm text-gray-500">
          <p className="max-w-3xl mx-auto px-4"><strong>Not affiliated with or endorsed by Grüns Nutrition, Inc.</strong> Greens Gummy Guide is an independent review site. All product names, logos and brands are property of their respective owners and are used here for identification and commentary only.</p>
          <p className="mt-2"><strong>Affiliate Disclosure:</strong> We may earn a commission when you purchase through our links, at no extra cost to you.</p>
          <p className="mt-2 flex items-center justify-center gap-4">
            <a href="/" className="underline hover:text-gray-700">All Guides</a>
            <a href="/affiliate-disclosure" className="underline hover:text-gray-700">Affiliate Disclosure</a>
            <a href="/privacy-policy" className="underline hover:text-gray-700">Privacy Policy</a>
          </p>
        </footer>
      </body>
    </html>
  );
}
