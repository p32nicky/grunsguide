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

  // Convert markdown to HTML first if needed
  if (body.includes("## ") || body.includes("### ") || body.startsWith("# ") || body.includes("**")) {
    body = marked.parse(body) as string;
  }

  // Replace [CTA...] placeholders and strip [/CTA] closing tags + trailing text
  body = body
    .replace(/\[CTA[^\]]*\]/gi, CTA_HTML)
    .replace(/&#x5B;CTA[^&]*?&#x5D;/gi, CTA_HTML)
    .replace(/\s*Try Gr[uü]ns VIP\s*\[\/CTA\]/gi, "")
    .replace(/\s*Get Gr[uü]ns Now\s*\[\/CTA\]/gi, "")
    .replace(/\[\/CTA\]/gi, "");

  // Remove stray CTA text lines Cerebras adds after [CTA]
  const ctaTextPatterns = [
    /^<p>Try Gr[uü]ns VIP\s*<\/p>$/gim,
    /^<p>Get Gr[uü]ns Now\s*<\/p>$/gim,
    /^<p>Learn More About Gr[uü]ns\s*<\/p>$/gim,
    /^<p>Shop Gr[uü]ns\s*<\/p>$/gim,
    /^<p>Order Gr[uü]ns\s*<\/p>$/gim,
    /^Try Gr[uü]ns VIP\s*$/gim,
    /^Get Gr[uü]ns Now\s*$/gim,
    /^Learn More About Gr[uü]ns\s*$/gim,
    /^Shop Gr[uü]ns\s*$/gim,
  ];
  ctaTextPatterns.forEach((p) => { body = body.replace(p, ""); });

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
