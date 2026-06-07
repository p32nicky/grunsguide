import { getAllArticles, getAllCategories } from "@/lib/articles";
import type { Metadata } from "next";
import Image from "next/image";
import ArticlesList from "./articles-list";

const AFFILIATE = "https://www.gruns.co/pages/vip?snowball=NICK67621";

export const metadata: Metadata = {
  title: "Grüns Gummies Reviews, Benefits & Complete Guide",
  description: "500+ honest guides about Grüns greens gummies — reviews, ingredients, benefits, comparisons, and tips to get the most from your daily greens.",
};

const websiteJsonLd = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "Grüns Guide",
  url: "https://grunsgummies.site",
  description: "Honest reviews and guides for Grüns superfoods greens gummies.",
  potentialAction: { "@type": "SearchAction", target: "https://grunsgummies.site/?q={search_term_string}", "query-input": "required name=search_term_string" },
};

const orgJsonLd = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Grüns Guide",
  url: "https://grunsgummies.site",
};

const faqJsonLd = {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  mainEntity: [
    {
      "@type": "Question",
      name: "What are Grüns greens gummies?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Grüns are comprehensive nutrition supplements that combine superfoods, greens, prebiotics, and vitamins into convenient, great-tasting gummies.",
      },
    },
    {
      "@type": "Question",
      name: "Are Grüns gummies safe?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Yes, Grüns undergo third-party testing for purity, potency, and safety. They are made with natural ingredients and are free from artificial colors and flavors.",
      },
    },
    {
      "@type": "Question",
      name: "How many Grüns gummies should I take per day?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "The recommended serving is one daily pack of Grüns gummies. Each pack contains a full day's worth of superfoods and nutrients.",
      },
    },
    {
      "@type": "Question",
      name: "Are Grüns gummies sugar-free?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Yes, Grüns gummies are sugar-free and use stevia as a sweetener instead. They contain zero grams of sugar per serving.",
      },
    },
    {
      "@type": "Question",
      name: "Can I take Grüns with other supplements?",
      acceptedAnswer: {
        "@type": "Answer",
        text: "Yes, Grüns can be taken with most other supplements. However, consult with a healthcare provider if you're taking medications or have specific health concerns.",
      },
    },
  ],
};

export default function HomePage() {
  const articles = getAllArticles();
  const categories = getAllCategories();
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteJsonLd) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(orgJsonLd) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }} />

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

      {/* Trust & Stats */}
      <div className="bg-gray-50 py-12">
        <div className="max-w-5xl mx-auto px-4">
          <div className="text-center mb-10">
            <p className="text-lg font-semibold text-gray-900">⭐ 4.8 stars from 100,000+ reviews | 1,000,000+ members</p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div><div className="text-3xl font-bold text-green-700">60+</div><div className="text-sm text-gray-600">Ingredients</div></div>
            <div><div className="text-3xl font-bold text-green-700">21</div><div className="text-sm text-gray-600">Vitamins & Minerals</div></div>
            <div><div className="text-3xl font-bold text-green-700">6g</div><div className="text-sm text-gray-600">Prebiotic Fiber</div></div>
            <div><div className="text-3xl font-bold text-green-700">30-Day</div><div className="text-sm text-gray-600">Money-Back Guarantee</div></div>
          </div>
        </div>
      </div>

      {/* Product Showcase */}
      <div className="max-w-5xl mx-auto px-4 py-12">
        <div className="overflow-hidden">
          <Image
            src="/images/gruns-product-showcase.png"
            alt="Grüns Superfood Greens Gummies - Product Showcase with Ingredients"
            width={900}
            height={600}
            className="w-full h-auto"
            priority
          />
        </div>
      </div>

      {/* Key Benefits */}
      <div className="max-w-5xl mx-auto px-4 py-12">
        <h2 className="text-2xl font-bold mb-8 text-center text-gray-900">How Grüns Supports Your Health</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <div className="text-center">
            <div className="text-4xl mb-3">🫘</div>
            <h3 className="font-bold text-gray-900 mb-2">Gut Health</h3>
            <p className="text-sm text-gray-600">Prebiotics feed good bacteria to boost nutrient absorption and digestion.</p>
          </div>
          <div className="text-center">
            <div className="text-4xl mb-3">🛡️</div>
            <h3 className="font-bold text-gray-900 mb-2">Immunity</h3>
            <p className="text-sm text-gray-600">Vitamin C, D, Zinc, antioxidants, and adaptogens support immune function.</p>
          </div>
          <div className="text-center">
            <div className="text-4xl mb-3">⚡</div>
            <h3 className="font-bold text-gray-900 mb-2">Energy & Body</h3>
            <p className="text-sm text-gray-600">Support recovery, strength, weight management, and metabolism naturally.</p>
          </div>
          <div className="text-center">
            <div className="text-4xl mb-3">🧠</div>
            <h3 className="font-bold text-gray-900 mb-2">Brain Health</h3>
            <p className="text-sm text-gray-600">B-Vitamins, Vitamin C, and Vitamin D support mental clarity and focus.</p>
          </div>
        </div>

        {/* What is Grüns */}
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
          <ArticlesList initialArticles={articles} categories={categories} />
        )}

        {/* Stats & Results */}
        <div className="mt-16 mb-12">
          <h2 className="text-2xl font-bold mb-8 text-center text-gray-900">Why Grüns Works</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Filling the Nutrition Gap</h3>
              <div className="space-y-3">
                <div>
                  <div className="text-3xl font-bold text-yellow-600">90%</div>
                  <p className="text-sm text-gray-600">of U.S. adults don't meet recommended daily nutrient intake</p>
                </div>
                <div>
                  <div className="text-3xl font-bold text-yellow-600">61%</div>
                  <p className="text-sm text-gray-600">of Americans experience weekly digestive issues</p>
                </div>
              </div>
            </div>
            <div className="bg-green-50 border border-green-200 rounded-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Real Customer Results (3+ months)</h3>
              <div className="space-y-3">
                <div><span className="text-2xl font-bold text-green-700">95%</span><span className="text-sm text-gray-600 ml-2">take Grüns 4-6x per week</span></div>
                <div><span className="text-2xl font-bold text-green-700">67%</span><span className="text-sm text-gray-600 ml-2">report improved health & well-being</span></div>
                <div><span className="text-2xl font-bold text-green-700">67%</span><span className="text-sm text-gray-600 ml-2">experience better digestion</span></div>
                <div><span className="text-2xl font-bold text-green-700">52%</span><span className="text-sm text-gray-600 ml-2">feel more energized daily</span></div>
              </div>
            </div>
          </div>
        </div>

        {/* Testimonials */}
        <div className="mt-12 mb-16">
          <h2 className="text-2xl font-bold mb-8 text-center text-gray-900">What Customers Say</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="border border-gray-200 rounded-lg p-6">
              <p className="text-sm text-gray-700 mb-3">"The convenience and taste are huge! Like mixed berries! Plus not having to clean a shaker bottle or extra dishes is absolutely excellent!"</p>
              <p className="font-semibold text-gray-900">Dustin O.</p>
              <p className="text-xs text-yellow-600">⭐⭐⭐⭐⭐</p>
            </div>
            <div className="border border-gray-200 rounded-lg p-6">
              <p className="text-sm text-gray-700 mb-3">"These gummies are shockingly delicious, like strawberries! We canceled our subscription but quickly resubscribed because we love Grüns so much!"</p>
              <p className="font-semibold text-gray-900">Kate S.</p>
              <p className="text-xs text-yellow-600">⭐⭐⭐⭐⭐</p>
            </div>
            <div className="border border-gray-200 rounded-lg p-6">
              <p className="text-sm text-gray-700 mb-3">"In eight years of testing powders, pills, and potions, there's only one that I liked enough to then spend my own money on: Grüns."</p>
              <p className="font-semibold text-gray-900">Kevin M.</p>
              <p className="text-xs text-yellow-600">⭐⭐⭐⭐⭐</p>
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="mt-8 bg-green-50 border border-green-100 rounded-2xl p-8">
          <h2 className="text-2xl font-bold mb-8 text-green-900">Frequently Asked Questions</h2>
          <div className="space-y-6 max-w-2xl">
            {[
              { q: "What are Grüns greens gummies?", a: "Grüns are comprehensive nutrition supplements that combine superfoods, greens, prebiotics, and vitamins into convenient, great-tasting gummies." },
              { q: "Are Grüns gummies safe?", a: "Yes, Grüns undergo third-party testing for purity, potency, and safety. They are made with natural ingredients and free from artificial colors and flavors." },
              { q: "How many Grüns should I take per day?", a: "The recommended serving is one daily pack of Grüns gummies. Each pack contains a full day's worth of superfoods and nutrients." },
              { q: "Are Grüns sugar-free?", a: "Yes, Grüns are sugar-free and use stevia as a sweetener. They contain zero grams of sugar per serving." },
              { q: "Can I take Grüns with other supplements?", a: "Yes, Grüns can be taken with most other supplements. Consult a healthcare provider if you're on medications." },
            ].map((item, idx) => (
              <details key={idx} className="group">
                <summary className="cursor-pointer font-semibold text-gray-900 hover:text-green-700">
                  {item.q}
                </summary>
                <p className="mt-2 text-gray-700 ml-4 text-sm">{item.a}</p>
              </details>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
