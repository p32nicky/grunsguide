/**
 * Canonical origin for this site.
 *
 * It was https://grunsgummies.site, which does not resolve and is not attached
 * to either Vercel project. Every page therefore canonicalised to a dead host,
 * and the sitemap in robots.txt pointed at a URL Google cannot fetch.
 *
 * Both the `grunssite` and `grunsguide` Vercel projects build from this one
 * repo, so they served identical, separately-indexed copies of all 610
 * articles. Canonicalising both to the origin that actually has search traffic
 * (grunssite.vercel.app, per Search Console) resolves that too: the twin now
 * points at this one instead of competing with it.
 *
 * If a real domain is attached later, change this single value.
 */
export const SITE_URL = "https://grunssite.vercel.app";
