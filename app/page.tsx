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
        <div className="max-w-5xl mx-auto px-4 py-8 lg:py-12 flex flex-col lg:flex-row items-center gap-10">
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
            <Image
              src="/images/gruns-hero-lede.webp"
              alt="Grüns Gummies - Complete Nutrition Guide"
              width={240}
              height={180}
              className="w-full max-w-[240px] h-auto rounded-lg"
              priority
            />
          </div>
        </div>
      </div>

      {/* Articles */}
      <div className="max-w-5xl mx-auto px-4 py-12">
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
        <div className="overflow-hidden flex justify-center">
          <Image
            src="/images/gruns-hero-product.jpg"
            alt="Grüns Gummies - Product"
            width={280}
            height={280}
            className="w-full max-w-[280px] h-auto"
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

        {/* What's Packed With */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-8 text-center text-gray-900">What's Packed Inside</h2>
          <div className="flex justify-center gap-3 overflow-x-auto pb-2">
            <div className="text-center flex-shrink-0"><div className="text-2xl mb-1">🥦</div><p className="text-xs font-semibold text-gray-900 whitespace-nowrap">Whole Veggies</p></div>
            <div className="text-center flex-shrink-0"><div className="text-2xl mb-1">🍇</div><p className="text-xs font-semibold text-gray-900 whitespace-nowrap">Whole Fruits</p></div>
            <div className="text-center flex-shrink-0"><div className="text-2xl mb-1">💊</div><p className="text-xs font-semibold text-gray-900 whitespace-nowrap">Vitamins & Minerals</p></div>
            <div className="text-center flex-shrink-0"><div className="text-2xl mb-1">🧠</div><p className="text-xs font-semibold text-gray-900 whitespace-nowrap">Adaptogens</p></div>
            <div className="text-center flex-shrink-0"><div className="text-2xl mb-1">🌿</div><p className="text-xs font-semibold text-gray-900 whitespace-nowrap">Herbs</p></div>
            <div className="text-center flex-shrink-0"><div className="text-2xl mb-1">🛡️</div><p className="text-xs font-semibold text-gray-900 whitespace-nowrap">Antioxidants</p></div>
            <div className="text-center flex-shrink-0"><div className="text-2xl mb-1">🦠</div><p className="text-xs font-semibold text-gray-900 whitespace-nowrap">Prebiotics</p></div>
            <div className="text-center flex-shrink-0"><div className="text-2xl mb-1">🍄</div><p className="text-xs font-semibold text-gray-900 whitespace-nowrap">Super Mushrooms</p></div>
            <div className="text-center flex-shrink-0"><div className="text-2xl mb-1">✨</div><p className="text-xs font-semibold text-gray-900 whitespace-nowrap">& More</p></div>
          </div>
        </div>

        {/* 3rd Party Testing */}
        <div className="bg-blue-50 border border-blue-200 rounded-2xl p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6 text-blue-900 text-center">Clinically & 3rd Party Tested</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h3 className="font-bold text-gray-900 mb-4">Rigorous Testing for Safety</h3>
              <p className="text-gray-700 mb-4">Every batch tested for purity, potency, and safety. We screen for:</p>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>✓ 70+ different pesticides</li>
                <li>✓ 4 types of heavy metals</li>
                <li>✓ 16 different contaminants</li>
                <li>✓ 9 microbial contaminants</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-gray-900 mb-4">Clinical Validation</h3>
              <p className="text-gray-700 mb-4">Clinically tested for nutrient absorption with proven results:</p>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>✓ Vitamin C levels improved after 90 days</li>
                <li>✓ Folate levels improved after 90 days</li>
                <li>✓ HSA/FSA eligible</li>
                <li>✓ 30-day money-back guarantee</li>
              </ul>
            </div>
          </div>
        </div>

        {/* What to Expect Timeline */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-8 text-center text-gray-900">What to Expect in 30+ Days</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="border border-gray-200 rounded-lg p-6 text-center">
              <div className="text-4xl font-bold text-green-700 mb-2">7-14</div>
              <p className="font-semibold text-gray-900 mb-2">Days</p>
              <p className="text-sm text-gray-600">Increased energy levels & better digestion noticed by most users</p>
            </div>
            <div className="border border-gray-200 rounded-lg p-6 text-center">
              <div className="text-4xl font-bold text-green-700 mb-2">30</div>
              <p className="font-semibold text-gray-900 mb-2">Days</p>
              <p className="text-sm text-gray-600">Improved mental clarity, immunity support, and overall vitality</p>
            </div>
            <div className="border border-gray-200 rounded-lg p-6 text-center">
              <div className="text-4xl font-bold text-green-700 mb-2">90</div>
              <p className="font-semibold text-gray-900 mb-2">Days</p>
              <p className="text-sm text-gray-600">Clinically validated improvements in Vitamin C & Folate levels</p>
            </div>
          </div>
        </div>

        {/* Flavor Variants */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-8 mb-12">
          <h2 className="text-2xl font-bold mb-6 text-yellow-900 text-center">Choose Your Flavor</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white border border-yellow-100 rounded-lg p-6">
              <h3 className="font-bold text-lg text-gray-900 mb-2">Original</h3>
              <p className="text-gray-600 mb-4">Where fresh strawberries meets clean greens. Our signature blend that started it all.</p>
              <p className="text-sm font-semibold text-yellow-700">Available in Low Sugar & Sugar-Free</p>
            </div>
            <div className="bg-white border border-yellow-100 rounded-lg p-6">
              <h3 className="font-bold text-lg text-gray-900 mb-2">Popsicle® Firecracker</h3>
              <p className="text-gray-600 mb-4">Limited time flavor. Bold, refreshing taste that brings the fun back to daily nutrition.</p>
              <p className="text-sm font-semibold text-red-600">LIMITED TIME OFFER</p>
            </div>
          </div>
        </div>

        {/* Taste Profile */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold mb-8 text-center text-gray-900">Tastes Like a Treat. Works Like a Supplement.</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-5xl mb-3">🍓</div>
              <h3 className="font-bold text-gray-900 mb-2">Fresh & Light</h3>
              <p className="text-sm text-gray-600">Crisp, refreshing flavor without any chalky aftertaste</p>
            </div>
            <div className="text-center">
              <div className="text-5xl mb-3">🍓</div>
              <h3 className="font-bold text-gray-900 mb-2">Strawberry</h3>
              <p className="text-sm text-gray-600">Natural strawberry sweetness you'll actually crave</p>
            </div>
            <div className="text-center">
              <div className="text-5xl mb-3">🥬</div>
              <h3 className="font-bold text-gray-900 mb-2">Sweet Greens</h3>
              <p className="text-sm text-gray-600">Clean, green taste with just the right balance</p>
            </div>
          </div>
        </div>

        {/* Guarantees */}
        <div className="bg-green-50 border border-green-200 rounded-2xl p-8 mb-12">
          <h2 className="text-2xl font-bold mb-8 text-green-900 text-center">Why You'll Love Grüns</h2>
          <div className="grid md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-4xl mb-3">💰</div>
              <h3 className="font-bold text-gray-900 mb-2">30-Day Money-Back</h3>
              <p className="text-sm text-gray-600">Not satisfied? Full refund, no questions asked.</p>
            </div>
            <div>
              <div className="text-4xl mb-3">⚡</div>
              <h3 className="font-bold text-gray-900 mb-2">FAST & FREE Shipping</h3>
              <p className="text-sm text-gray-600">On first order. Convenient delivery to your door.</p>
            </div>
            <div>
              <div className="text-4xl mb-3">🏥</div>
              <h3 className="font-bold text-gray-900 mb-2">HSA/FSA Eligible</h3>
              <p className="text-sm text-gray-600">Use your medical savings account with Truemed.</p>
            </div>
          </div>
        </div>

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
