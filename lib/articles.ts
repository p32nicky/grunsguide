import fs from "fs";
import path from "path";
import { marked } from "marked";

const AFFILIATE = "https://www.gruns.co/pages/vip?snowball=NICK67621";
const CTA_HTML = `<a href="${AFFILIATE}" target="_blank" rel="noopener noreferrer" style="display:inline-block;background:#15803d;color:white;font-weight:700;font-size:13px;padding:8px 18px;border-radius:999px;text-decoration:none;margin:4px 0">Try Grüns VIP →</a>`;

export interface Article {
  slug: string;
  title: string;
  metaDescription: string;
  keywords: string[];
  body: string;
  generatedAt: string;
  error?: string;
}

const ARTICLES_DIR = path.join(process.cwd(), "content", "articles");

function processBody(raw: string): string {
  // Strip META/KEYWORDS lines
  let body = raw
    .replace(/\*?\*?Meta Description:?\*?\*?.*\n?/gi, "")
    .replace(/\*?\*?Keywords?:?\*?\*?.*\n?/gi, "")
    .replace(/META:\s*.+\n?/g, "")
    .replace(/KEYWORDS:\s*.+\n?/g, "");

  // Convert Cerebras "H2." / "H3." heading format to HTML
  body = body
    .replace(/^H1\.\s*(.+)$/gim, "<h1>$1</h1>")
    .replace(/^H2\.\s*(.+)$/gim, "<h2>$1</h2>")
    .replace(/^H3\.\s*(.+)$/gim, "<h3>$1</h3>")
    .replace(/^H4\.\s*(.+)$/gim, "<h4>$1</h4>");

  // Convert markdown to HTML if needed
  if (body.includes("## ") || body.includes("### ") || body.startsWith("# ") || body.includes("**")) {
    body = marked.parse(body) as string;
  }

  // Strip References/Sources/Citations sections Cerebras adds
  body = body
    .replace(/<h[123][^>]*>\s*References\s*<\/h[123]>[\s\S]*/gi, "")
    .replace(/<h[123][^>]*>\s*Sources\s*<\/h[123]>[\s\S]*/gi, "")
    .replace(/<h[123][^>]*>\s*Citations\s*<\/h[123]>[\s\S]*/gi, "")
    .replace(/\n##\s*References[\s\S]*/gi, "")
    .replace(/\n##\s*Sources[\s\S]*/gi, "")
    .replace(/H2\.\s*References[\s\S]*/gi, "");

  // Strip any CTA artifacts (old articles)
  body = body
    .replace(/\[CTA\][^\n<]*/gi, "")
    .replace(/\[CTA[^\]]*\]/gi, "")
    .replace(/\[\/CTA\]/gi, "")
    .replace(/&#x5B;CTA[^&]*?&#x5D;/gi, "");

  // Strip stray CTA text lines
  body = body
    .replace(/<p>\s*Try Gr[uü]ns[^<]*<\/p>/gi, "")
    .replace(/<p>\s*Get Gr[uü]ns[^<]*<\/p>/gi, "")
    .replace(/<p>\s*Shop Gr[uü]ns[^<]*<\/p>/gi, "")
    .replace(/<p>\s*Learn More[^<]*<\/p>/gi, "");

  // Inject one CTA button after the second </h2> tag
  let h2Count = 0;
  body = body.replace(/<\/h2>/gi, (match) => {
    h2Count++;
    return h2Count === 2 ? `</h2>${CTA_HTML}` : match;
  });

  return body;
}

export function getAllArticles(): Article[] {
  if (!fs.existsSync(ARTICLES_DIR)) return [];
  return fs.readdirSync(ARTICLES_DIR)
    .filter((f) => f.endsWith(".json"))
    .map((f) => {
      const a = JSON.parse(fs.readFileSync(path.join(ARTICLES_DIR, f), "utf-8")) as Article;
      return { ...a, body: processBody(a.body) };
    })
    .filter((a) => !a.error)
    .sort((a, b) => a.title.localeCompare(b.title));
}

export function getArticleBySlug(slug: string): Article | null {
  const filePath = path.join(ARTICLES_DIR, `${slug}.json`);
  if (!fs.existsSync(filePath)) return null;
  const a = JSON.parse(fs.readFileSync(filePath, "utf-8")) as Article;
  return { ...a, body: processBody(a.body) };
}

export function getAllSlugs(): string[] {
  if (!fs.existsSync(ARTICLES_DIR)) return [];
  return fs.readdirSync(ARTICLES_DIR).filter((f) => f.endsWith(".json")).map((f) => f.replace(".json", ""));
}

export function getRelatedArticles(slug: string, limit: number = 5): Article[] {
  const current = getArticleBySlug(slug);
  if (!current) return [];

  const all = getAllSlugs()
    .map((s) => getArticleBySlug(s))
    .filter((a) => a && a.slug !== slug) as Article[];

  // Score articles by keyword overlap
  const scored = all.map((article) => {
    const overlap = article.keywords.filter((k) =>
      current.keywords.some((ck) => k.toLowerCase().includes(ck.toLowerCase()) || ck.toLowerCase().includes(k.toLowerCase()))
    ).length;
    return { article, score: overlap };
  });

  return scored
    .filter((s) => s.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map((s) => s.article);
}

export function getAllCategories(): string[] {
  const all = getAllArticles();
  const categories = new Set<string>();

  all.forEach((article) => {
    article.keywords.forEach((keyword) => {
      // Clean up keyword - remove special prefix characters
      let clean = keyword
        .replace(/^[:=>\-*]+\s*/, '') // Remove leading special chars
        .replace(/\s*[:=>\-*]+$/, '') // Remove trailing special chars
        .toLowerCase()
        .trim();

      // Extract main categories from keywords
      if (clean.length > 2 && clean.length < 50 && !/^[:\-=*>]/.test(clean)) {
        categories.add(clean);
      }
    });
  });

  return Array.from(categories)
    .filter((c) => c.length > 3 && !/^[:\-=*>]/.test(c) && c !== "amazon")
    .sort()
    .slice(0, 20); // Limit to top 20
}
