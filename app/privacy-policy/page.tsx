import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: "Grüns Guide privacy policy — how we collect, use, and protect your data.",
};

export default function PrivacyPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-12 prose prose-gray">
      <h1>Privacy Policy</h1>
      <p><strong>Last updated: May 2026</strong></p>
      <p>
        Grüns Guide ("we," "us," or "our") respects your privacy. This policy explains how we handle information when you visit our site.
      </p>
      <h2>Information We Collect</h2>
      <p>
        We do not collect personal information directly. However, third-party services we use (such as Google Analytics) may collect anonymized usage data including pages visited, time on site, and general location.
      </p>
      <h2>Google Analytics</h2>
      <p>
        We use Google Analytics to understand how visitors use our site. Google may collect anonymized data per their own <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">privacy policy</a>. You can opt out via <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener noreferrer">Google's opt-out tool</a>.
      </p>
      <h2>Cookies</h2>
      <p>
        Our site may use cookies for analytics purposes. You can disable cookies in your browser settings at any time.
      </p>
      <h2>Affiliate Links</h2>
      <p>
        We participate in affiliate programs. Clicking affiliate links may place cookies on your device per the retailer's privacy policy.
      </p>
      <h2>Third Party Links</h2>
      <p>
        Our site contains links to external websites. We are not responsible for the privacy practices of those sites.
      </p>
      <h2>Changes to This Policy</h2>
      <p>
        We may update this policy occasionally. Continued use of the site constitutes acceptance of any changes.
      </p>
      <h2>Contact</h2>
      <p>
        Questions? Email us at <a href="mailto:nickdavies100@gmail.com">nickdavies100@gmail.com</a>.
      </p>
    </div>
  );
}
