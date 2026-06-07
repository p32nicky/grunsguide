import { getArticleBySlug, getAllSlugs, getRelatedArticles } from "@/lib/articles";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Image from "next/image";

const AFFILIATE = "https://www.gruns.co/pages/vip?snowball=NICK67621";
const SITE = "https://grunsgummies.site";

interface Props { params: Promise<{ slug: string }> }

export async function generateStaticParams() {
  return getAllSlugs().map((slug) => ({ slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const article = getArticleBySlug(slug);
  if (!article) return {};
  return {
    title: article.title,
    description: article.metaDescription,
    keywords: article.keywords,
    openGraph: { title: article.title, description: article.metaDescription, type: "article" },
    alternates: { canonical: `/articles/${slug}` },
  };
}

export default async function ArticlePage({ params }: Props) {
  const { slug } = await params;
  const article = getArticleBySlug(slug);
  if (!article) notFound();

  const articleJsonLd = {
    "@context": "https://schema.org", "@type": "Article",
    headline: article.title, description: article.metaDescription,
    keywords: article.keywords.join(", "),
    datePublished: article.generatedAt, dateModified: article.generatedAt,
    author: { "@type": "Organization", name: "Grüns Guide", url: SITE },
    publisher: { "@type": "Organization", name: "Grüns Guide", url: SITE },
    mainEntityOfPage: { "@type": "WebPage", "@id": `${SITE}/articles/${slug}` },
  };

  const breadcrumbJsonLd = {
    "@context": "https://schema.org", "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Home", item: SITE },
      { "@type": "ListItem", position: 2, name: article.title, item: `${SITE}/articles/${slug}` },
    ],
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(articleJsonLd) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbJsonLd) }} />
      <div className="max-w-3xl mx-auto px-4 py-12">
        <nav className="text-sm text-gray-500 mb-6">
          <ol className="flex items-center gap-2">
            <li><a href="/" className="hover:text-green-700">Home</a></li>
            <li>›</li>
            <li className="text-gray-400">{article.title}</li>
          </ol>
        </nav>

        <h1 className="text-4xl lg:text-5xl font-bold text-gray-900 mb-6">{article.title}</h1>

        <div className="mb-8 flex justify-center">
          <Image
            src="/images/article-hero.webp"
            alt={article.title}
            width={400}
            height={250}
            className="w-full max-w-sm h-auto rounded-lg"
            priority
          />
        </div>

        <div className="bg-green-50 border border-green-200 rounded-xl p-4 mb-8 flex items-center justify-between gap-4 flex-wrap">
          <p className="text-sm text-gray-700 font-medium">Get Grüns at VIP price — superfoods in a gummy.</p>
          <a href={AFFILIATE} target="_blank" rel="noopener noreferrer"
            className="bg-green-700 hover:bg-green-800 text-white text-sm font-bold px-5 py-2 rounded-full transition-colors whitespace-nowrap">
            Try Grüns VIP →
          </a>
        </div>

        <article
          className="prose prose-gray prose-headings:font-bold prose-a:text-green-700 prose-a:no-underline hover:prose-a:underline max-w-none"
          dangerouslySetInnerHTML={{ __html: article.body }}
        />

        <div className="mt-12 bg-gradient-to-br from-green-700 to-green-900 rounded-2xl p-8 text-center text-white">
          <h2 className="text-2xl font-bold mb-3">Ready to Try Grüns?</h2>
          <p className="mb-6 text-green-100">Superfoods, prebiotics, and vitamins in one daily gummy. Fresh, sweet taste. No chalky powders.</p>
          <a href={AFFILIATE} target="_blank" rel="noopener noreferrer"
            className="inline-block bg-yellow-400 hover:bg-yellow-300 text-green-900 font-bold px-8 py-3 rounded-full transition-colors">
            Get VIP Access to Grüns →
          </a>
          <p className="text-xs text-green-300 mt-3">28 daily packs · Sugar free · #1 Greens Brand</p>
        </div>

        {/* Taste Profile */}
        <div className="mt-12 mb-12">
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

        <div className="mt-12 border-t border-gray-200 pt-8">
          <h2 className="text-xl font-bold mb-6 text-gray-900">Related Guides</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {getRelatedArticles(slug, 3).map((related) => (
              <a
                key={related.slug}
                href={`/articles/${related.slug}`}
                className="block p-4 border border-gray-200 rounded-lg hover:border-green-500 hover:shadow-md transition-all"
              >
                <h3 className="font-semibold text-gray-900 hover:text-green-700 line-clamp-2">{related.title}</h3>
                <p className="text-xs text-gray-500 mt-2 line-clamp-1">{related.metaDescription}</p>
              </a>
            ))}
          </div>
        </div>

        <div className="mt-8 text-center">
          <a href="/" className="text-sm text-gray-500 hover:text-gray-700 underline">← All Grüns guides</a>
        </div>
      </div>
    </>
  );
}
