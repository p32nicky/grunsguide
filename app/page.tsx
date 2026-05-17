import { getAllArticles } from "@/lib/articles";
import type { Metadata } from "next";
import Link from "next/link";

const AFFILIATE = "https://www.gruns.co/pages/vip?snowball=NICK67621";

export const metadata: Metadata = {
  title: "Grüns Gummies Reviews, Benefits & Complete Guide",
  description: "500+ honest guides about Grüns greens gummies — reviews, ingredients, benefits, comparisons, and tips to get the most from your daily greens.",
};

const websiteJsonLd = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "Grüns Guide",
  url: "https://grunsguide.vercel.app",
  description: "Honest reviews and guides for Grüns superfoods greens gummies.",
  potentialAction: { "@type": "SearchAction", target: "https://grunsguide.vercel.app/?q={search_term_string}", "query-input": "required name=search_term_string" },
};

const orgJsonLd = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Grüns Guide",
  url: "https://grunsguide.vercel.app",
};

export default function HomePage() {
  const articles = getAllArticles();
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteJsonLd) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(orgJsonLd) }} />

      {/* Hero */}
      <div className="bg-gradient-to-br from-green-700 to-green-900 text-white">
        <div className="max-w-5xl mx-auto px-4 py-16 flex flex-col lg:flex-row items-center gap-10">
          <div className="flex-1 text-center lg:text-left">
            <h1 className="text-4xl lg:text-5xl font-bold mb-4 leading-tight">
              The #1 Greens Brand — <span className="text-yellow-300">In Gummy Form</span>
            </h1>
            <p className="text-green-100 text-lg mb-6 max-w-xl">
              Grüns packs superfoods, prebiotics, and vitamins into a delicious daily gummy. No chalky powders, no bad taste — just real nutrition that actually tastes good.
            </p>
            <a href={AFFILIATE} target="_blank" rel="noopener noreferrer"
              className="inline-block bg-yellow-400 hover:bg-yellow-300 text-green-900 font-bold px-8 py-3 rounded-full text-lg transition-colors">
              Try Grüns — VIP Offer →
            </a>
            <p className="text-green-300 text-sm mt-3">Superfoods · Prebiotics · Vitamins · Sugar Free</p>
          </div>
          <div className="flex-1 flex justify-center">
            <div className="bg-green-600 rounded-3xl p-8 text-center shadow-xl">
              <div className="text-7xl mb-3">🐻</div>
              <div className="text-yellow-300 font-bold text-2xl">grüns</div>
              <div className="text-green-200 text-sm mt-1">Superfoods · Prebiotics · Vitamins</div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats bar */}
      <div className="bg-gray-50 py-10">
        <div className="max-w-5xl mx-auto px-4 grid grid-cols-3 gap-6 text-center">
          <div><div className="text-3xl font-bold text-green-700">#1</div><div className="text-sm text-gray-600">Greens Brand</div></div>
          <div><div className="text-3xl font-bold text-green-700">28</div><div className="text-sm text-gray-600">Daily Packs</div></div>
          <div><div className="text-3xl font-bold text-green-700">0g</div><div className="text-sm text-gray-600">Sugar</div></div>
        </div>
      </div>

      {/* What is Grüns */}
      <div className="max-w-5xl mx-auto px-4 py-12">
        <div className="bg-green-50 border border-green-100 rounded-2xl p-8 mb-12 text-center">
          <h2 className="text-2xl font-bold mb-3 text-green-900">What Is Grüns?</h2>
          <p className="text-gray-700 max-w-2xl mx-auto mb-4">
            Grüns is a comprehensive nutrition supplement that combines superfoods, greens, prebiotics, and vitamins into a convenient, great-tasting gummy. Each daily pack supports gut health, energy, immunity, recovery, beauty, and cognition — no mixing, no powder, no excuses.
          </p>
          <a href={AFFILIATE} target="_blank" rel="noopener noreferrer" className="text-green-700 font-semibold hover:underline">
            Shop Grüns VIP →
          </a>
        </div>

        {/* Articles */}
        <h2 className="text-2xl font-bold mb-6">
          {articles.length > 0 ? `${articles.length} Grüns Guides & Reviews` : "Guides Loading..."}
        </h2>
        {articles.length === 0 ? (
          <div className="text-center py-16 text-gray-500">
            <p className="text-lg">Articles being generated. Check back soon.</p>
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {articles.map((article) => (
              <Link key={article.slug} href={`/articles/${article.slug}`}
                className="block p-5 border border-gray-200 rounded-xl hover:border-green-300 hover:shadow-sm transition-all group">
                <h3 className="font-semibold text-gray-900 group-hover:text-green-700 leading-snug mb-2">{article.title}</h3>
                <p className="text-sm text-gray-500 line-clamp-2">{article.metaDescription}</p>
              </Link>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
