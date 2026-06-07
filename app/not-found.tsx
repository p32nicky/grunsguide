import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-green-100 px-4">
      <div className="text-center max-w-md">
        <h1 className="text-6xl font-bold text-green-700 mb-2">404</h1>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Page Not Found</h2>
        <p className="text-gray-600 mb-8">
          Sorry! We couldn't find the page you're looking for. It might have been moved or removed.
        </p>
        <div className="flex flex-col gap-3">
          <Link href="/" className="inline-block bg-green-700 hover:bg-green-800 text-white font-bold px-6 py-3 rounded-full transition-colors">
            ← Back to Home
          </Link>
          <a href="https://www.gruns.co/pages/vip?snowball=NICK67621" target="_blank" rel="noopener noreferrer"
            className="inline-block bg-yellow-400 hover:bg-yellow-300 text-green-900 font-bold px-6 py-3 rounded-full transition-colors">
            Try Grüns VIP →
          </a>
        </div>
      </div>
    </div>
  );
}
