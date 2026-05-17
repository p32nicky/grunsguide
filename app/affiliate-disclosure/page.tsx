import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Affiliate Disclosure",
  description: "Grüns Guide affiliate disclosure — how we earn commissions and our commitment to honest reviews.",
};

export default function AffiliatePage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-12 prose prose-gray">
      <h1>Affiliate Disclosure</h1>
      <p><strong>Last updated: May 2026</strong></p>
      <p>
        Grüns Guide ("we," "us," or "our") participates in affiliate marketing programs. This means we may earn a commission when you click on links and make a purchase — at no extra cost to you.
      </p>
      <h2>How It Works</h2>
      <p>
        Some links on this site are affiliate links. When you click one and complete a purchase, we receive a small commission from the retailer. This helps us keep the site running and producing free content.
      </p>
      <h2>Our Commitment to Honesty</h2>
      <p>
        We only recommend products we genuinely believe in. Our reviews and guides reflect honest opinions — affiliate relationships do not influence our editorial content. We will always disclose when content contains affiliate links.
      </p>
      <h2>Grüns Affiliate Program</h2>
      <p>
        We are an affiliate of Grüns and earn a commission on qualifying purchases made through our links. This does not affect the price you pay.
      </p>
      <h2>Contact</h2>
      <p>
        Questions? Email us at <a href="mailto:nickdavies100@gmail.com">nickdavies100@gmail.com</a>.
      </p>
    </div>
  );
}
