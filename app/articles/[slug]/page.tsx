import { getArticleBySlug, getAllSlugs } from "@/lib/articles";
import type { Metadata } from "next";
import { notFound } from "next/navigation";

const AFFILIATE = "https://www.gruns.co/pages/vip?snowball=NICK67621";
const AMAZON = "https://amzn.to/4tHu3gL";
const SITE = "https://grunsguide.vercel.app";

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

        {/* Amazon product card */}
        <div className="border border-gray-200 rounded-xl p-4 mb-4 flex items-center gap-4 bg-white shadow-sm">
          <div className="text-4xl">🐻</div>
          <div className="flex-1 min-w-0">
            <p className="text-xs text-gray-500 font-medium uppercase tracking-wide mb-1">Featured Product</p>
            <p className="font-bold text-gray-900 text-sm leading-snug">Grüns Superfoods Greens Gummies — 28 Daily Packs</p>
            <p className="text-xs text-gray-500 mt-1">Gut Health · Energy · Immunity · Sugar Free</p>
          </div>
          <a href={AMAZON} target="_blank" rel="noopener noreferrer sponsored"
            className="shrink-0 bg-yellow-400 hover:bg-yellow-300 text-gray-900 text-xs font-bold px-4 py-2 rounded-full transition-colors whitespace-nowrap">
            View on Amazon →
          </a>
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
          <a href={AMAZON} target="_blank" rel="noopener noreferrer sponsored"
            className="inline-block mt-4 bg-yellow-400 hover:bg-yellow-300 text-gray-900 text-sm font-bold px-6 py-2 rounded-full transition-colors">
            Also Available on Amazon →
          </a>
        </div>

        <div className="mt-8 text-center">
          <a href="/" className="text-sm text-gray-500 hover:text-gray-700 underline">← All Grüns guides</a>
        </div>
      </div>
    </>
  );
}
