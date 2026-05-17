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

  // Convert markdown to HTML if needed
  if (body.includes("## ") || body.includes("### ") || body.startsWith("# ") || body.includes("**")) {
    body = marked.parse(body) as string;
  }

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
