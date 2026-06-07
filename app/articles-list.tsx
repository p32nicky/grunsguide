"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Article {
  slug: string;
  title: string;
  metaDescription: string;
}

interface SearchResponse {
  articles: Article[];
  pagination: { page: number; limit: number; total: number; totalPages: number; hasMore: boolean };
}

export default function ArticlesList({ initialArticles, categories }: { initialArticles: Article[]; categories: string[] }) {
  const [articles, setArticles] = useState<Article[]>(initialArticles);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(initialArticles.length);
  const [totalPages, setTotalPages] = useState(1);
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [sort, setSort] = useState("relevance");
  const [loading, setLoading] = useState(false);

  const limit = 12;

  useEffect(() => {
    const search = async () => {
      setLoading(true);
      const params = new URLSearchParams({
        q: query,
        category,
        sort,
        page: String(page),
        limit: String(limit),
      });

      const res = await fetch(`/api/search?${params}`);
      const data: SearchResponse = await res.json();
      setArticles(data.articles);
      setTotal(data.pagination.total);
      setTotalPages(data.pagination.totalPages);
      setLoading(false);
    };

    search();
  }, [query, category, sort, page]);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
    setPage(1);
  };

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setCategory(e.target.value);
    setPage(1);
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSort(e.target.value);
    setPage(1);
  };

  return (
    <div>
      {/* Search & Filters */}
      <div className="mb-8 space-y-4">
        <div className="flex flex-col md:flex-row gap-4">
          <input
            type="text"
            placeholder="Search guides..."
            value={query}
            onChange={handleSearch}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <select
            value={category}
            onChange={handleCategoryChange}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat.replace(/-/g, ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
              </option>
            ))}
          </select>
          <select
            value={sort}
            onChange={handleSortChange}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            <option value="relevance">Most Relevant</option>
            <option value="newest">Newest</option>
            <option value="alphabetical">A-Z</option>
          </select>
        </div>
        <p className="text-sm text-gray-500">{total} guides found</p>
      </div>

      {/* Articles Grid */}
      {loading ? (
        <div className="text-center py-12 text-gray-500">Loading...</div>
      ) : articles.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No articles found. Try different search terms.</div>
      ) : (
        <>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 mb-8">
            {articles.map((article) => (
              <Link key={article.slug} href={`/articles/${article.slug}`}
                className="block p-5 border border-gray-200 rounded-xl hover:border-green-300 hover:shadow-sm transition-all group">
                <h3 className="font-semibold text-gray-900 group-hover:text-green-700 leading-snug mb-2">{article.title}</h3>
                <p className="text-sm text-gray-500 line-clamp-2">{article.metaDescription}</p>
              </Link>
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2 py-8">
              <button
                onClick={() => setPage(Math.max(1, page - 1))}
                disabled={page === 1}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                ← Previous
              </button>
              <div className="text-sm text-gray-600">
                Page {page} of {totalPages}
              </div>
              <button
                onClick={() => setPage(Math.min(totalPages, page + 1))}
                disabled={page === totalPages}
                className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
