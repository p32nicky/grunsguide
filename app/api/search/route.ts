import { getAllArticles } from "@/lib/articles";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const q = searchParams.get("q")?.toLowerCase() || "";
  const category = searchParams.get("category")?.toLowerCase() || "";
  const sort = searchParams.get("sort") || "relevance"; // relevance, newest, alphabetical
  const page = parseInt(searchParams.get("page") || "1");
  const limit = parseInt(searchParams.get("limit") || "12");

  let articles = getAllArticles();

  // Filter by search query
  if (q) {
    articles = articles.filter(
      (a) =>
        a.title.toLowerCase().includes(q) ||
        a.metaDescription.toLowerCase().includes(q) ||
        a.keywords.some((k) => k.toLowerCase().includes(q))
    );
  }

  // Filter by category
  if (category) {
    articles = articles.filter((a) =>
      a.keywords.some((k) => k.toLowerCase().includes(category))
    );
  }

  // Sort
  if (sort === "newest") {
    articles.sort((a, b) => new Date(b.generatedAt).getTime() - new Date(a.generatedAt).getTime());
  } else if (sort === "alphabetical") {
    articles.sort((a, b) => a.title.localeCompare(b.title));
  }
  // relevance is default (as returned from search filter)

  // Paginate
  const total = articles.length;
  const offset = (page - 1) * limit;
  const paginated = articles.slice(offset, offset + limit);
  const totalPages = Math.ceil(total / limit);

  return NextResponse.json({
    articles: paginated,
    pagination: { page, limit, total, totalPages, hasMore: page < totalPages },
  });
}
