'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';

const AFFILIATE = "https://www.gruns.co/pages/vip?snowball=NICK67621";

export default function ExitPopup() {
  const [shown, setShown] = useState(false);

  useEffect(() => {
    const handleMouseLeave = (e: MouseEvent) => {
      if (e.clientY <= 0 && !shown) {
        setShown(true);
      }
    };

    document.addEventListener('mouseleave', handleMouseLeave);
    return () => document.removeEventListener('mouseleave', handleMouseLeave);
  }, [shown]);

  if (!shown) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="bg-white rounded-2xl max-w-md w-full shadow-2xl overflow-hidden animate-in fade-in zoom-in-95">
        {/* Close button */}
        <button
          onClick={() => setShown(false)}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 z-10 text-2xl"
        >
          ✕
        </button>

        {/* Content */}
        <div className="bg-gradient-to-br from-green-700 to-green-900 text-white p-6 text-center">
          <h2 className="text-2xl font-bold mb-2">Hold on!</h2>
          <p className="text-green-100">Get Grüns at our exclusive VIP price before you go.</p>
        </div>

        <div className="p-6">
          <div className="flex justify-center mb-4">
            <Image
              src="/images/gruns-hero-product.jpg"
              alt="Grüns Gummies"
              width={150}
              height={150}
              className="w-32 h-auto rounded-lg"
            />
          </div>

          <p className="text-sm text-gray-700 mb-4 text-center">
            <strong>Superfoods, prebiotics & vitamins</strong> in one delicious daily gummy. No chalky powders.
          </p>

          <div className="bg-green-50 rounded-lg p-3 mb-4 text-center text-sm">
            <p className="text-green-900 font-semibold">✓ #1 Greens Brand</p>
            <p className="text-green-700 text-xs">4.8 stars from 100,000+ reviews</p>
          </div>

          <a
            href={AFFILIATE}
            target="_blank"
            rel="noopener noreferrer"
            onClick={() => setShown(false)}
            className="block w-full bg-green-700 hover:bg-green-800 text-white font-bold py-3 px-4 rounded-full transition-colors text-center mb-3"
          >
            Claim VIP Price Now →
          </a>

          <button
            onClick={() => setShown(false)}
            className="block w-full text-gray-500 hover:text-gray-700 text-sm py-2"
          >
            No thanks, continue browsing
          </button>
        </div>
      </div>
    </div>
  );
}
