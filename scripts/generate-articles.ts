/**
 * Generates 500 SEO articles about Grüns greens gummies.
 * Groq first, falls back to Cerebras when daily limit hit.
 */

import Groq from "groq-sdk";
import Cerebras from "@cerebras/cerebras_cloud_sdk";
import { marked } from "marked";
import fs from "fs";
import path from "path";

let useGroq = true;
let useCerebras = true;

const AFFILIATE = "https://www.gruns.co/pages/vip?snowball=NICK67621";

const ARTICLE_TOPICS = [
  // Core reviews
  "Grüns Review: Are These Greens Gummies Worth It?",
  "Grüns Gummies Honest Review: What Nobody Tells You",
  "Grüns Review Reddit: What Real Users Are Saying",
  "Is Grüns Worth It? Complete Cost vs Value Analysis",
  "Grüns vs Athletic Greens: Which Greens Supplement Wins?",
  "Grüns vs Organifi: Full Comparison",
  "Grüns vs Amazing Grass: Which Is Better?",
  "Grüns vs Garden of Life: Greens Supplement Showdown",
  "Grüns vs Bloom Greens: Which Should You Buy?",
  "Grüns vs Super Greens Powder: Gummy vs Powder",
  "Grüns vs Huel Greens: Complete Comparison",
  "Grüns vs Nested Naturals Super Greens: Review",
  "Grüns vs Green Vibrance: Which Is Better?",
  "Grüns vs Vital Proteins Collagen Greens: Comparison",
  "Grüns vs Ritual Multivitamin: What's the Difference?",
  "Grüns vs Olly Vitamins: Which Daily Supplement Wins?",
  "Grüns vs SmartyPants Gummies: Full Review",
  "Grüns vs Goli Supergreens Gummies: Head to Head",
  "Grüns vs Nature's Way Alive: Comparison Guide",
  "Grüns Alternatives: Best Greens Supplements Ranked",

  // Ingredients & nutrition
  "Grüns Ingredients: Full Breakdown of Every Component",
  "Grüns Superfoods List: What's Actually Inside",
  "Grüns Prebiotics: How They Support Gut Health",
  "Grüns Vitamins: Which Ones Are Included and Why",
  "Grüns Greens Blend: Every Superfood Explained",
  "Is Grüns Sugar Free? What Sweeteners Do They Use?",
  "Grüns Calories: How Many Per Serving?",
  "Grüns Nutrition Label: Full Analysis",
  "Are Grüns Gummies Vegan?",
  "Are Grüns Gummies Gluten Free?",
  "Grüns Heavy Metals Testing: Are They Safe?",
  "Grüns Third Party Testing: What You Should Know",
  "Grüns Spirulina Content: Benefits and Dosage",
  "Grüns Ashwagandha: What Does It Do?",
  "Grüns Probiotics vs Prebiotics: Understanding the Difference",
  "Grüns Vitamin C Content: Is It Enough?",
  "Grüns B Vitamins: Energy and Benefits Explained",
  "Grüns Zinc: Immunity Benefits Explained",
  "Grüns Magnesium: Sleep and Recovery Benefits",
  "Grüns Antioxidants: How They Protect Your Body",

  // Health benefits
  "Grüns for Gut Health: What the Research Says",
  "Grüns for Energy: Does It Actually Work?",
  "Grüns for Immunity: Can Greens Gummies Boost Immunity?",
  "Grüns for Skin: Beauty Benefits of Daily Greens",
  "Grüns for Weight Loss: Can It Help You Lose Weight?",
  "Grüns for Brain Health and Cognition",
  "Grüns for Recovery After Exercise",
  "Grüns for Bloating: Does It Help with Digestion?",
  "Grüns for Hair Growth: What to Expect",
  "Grüns for Inflammation: Anti-Inflammatory Benefits",
  "Grüns for Sleep: Can Superfoods Improve Sleep Quality?",
  "Grüns for Detox: Do Greens Gummies Detoxify?",
  "Grüns for Hormonal Balance",
  "Grüns for Mental Clarity and Focus",
  "Grüns for Aging: Anti-Aging Benefits of Superfoods",
  "Grüns for Athletes: Performance and Recovery",
  "Grüns for Vegetarians and Vegans",
  "Grüns for People Who Hate Vegetables",
  "Grüns for Busy Professionals",
  "Grüns for Seniors: Benefits of Daily Greens After 50",

  // Audience-specific
  "Grüns for Women: Benefits and What to Expect",
  "Grüns for Men: How Superfoods Support Male Health",
  "Grüns for Kids: Is It Safe for Children?",
  "Grüns for Pregnant Women: Safety and Benefits",
  "Grüns for College Students: Daily Nutrition on a Budget",
  "Grüns for Runners: Endurance and Recovery",
  "Grüns for Gym-Goers: Does It Replace a Multivitamin?",
  "Grüns for Keto Diet: Are They Keto Friendly?",
  "Grüns for Intermittent Fasting: Can You Take Them While Fasting?",
  "Grüns for Diabetics: Blood Sugar Impact",
  "Grüns for People with IBS: Gut Health Guide",
  "Grüns for Vegans: Complete Nutrition Review",
  "Grüns for Paleo Diet: Are They Paleo Friendly?",
  "Grüns for People with Food Allergies",
  "Grüns for Shift Workers: Managing Energy Naturally",
  "Grüns for Remote Workers: Fighting Afternoon Slumps",
  "Grüns for Parents: Getting Nutrients While Busy",
  "Grüns for Travelers: Staying Healthy on the Road",
  "Grüns for Night Owls: Supporting Health Despite Poor Sleep",
  "Grüns for People Who Struggle with Pills",

  // How to use
  "How to Take Grüns: Best Time of Day",
  "How Many Grüns Gummies Per Day?",
  "Can You Take Grüns on an Empty Stomach?",
  "Grüns Before or After Workout: Which Is Better?",
  "Can You Take Grüns with Other Supplements?",
  "Grüns and Coffee: Can You Take Them Together?",
  "Grüns Storage: How to Keep Them Fresh",
  "What to Expect in Your First Week Taking Grüns",
  "Grüns 30-Day Results: What to Expect",
  "Grüns 90-Day Review: Long Term Results",
  "How Long Until You Feel Grüns Working?",
  "Grüns Side Effects: What to Watch Out For",
  "Can You Take Too Many Grüns Gummies?",
  "Grüns and Medication Interactions: What to Know",
  "Grüns Taste Review: What Do They Actually Taste Like?",
  "Grüns Texture: Are They Chewy or Hard?",
  "Grüns Serving Size: Is One Pack Enough?",
  "Grüns Subscription: Is It Worth Subscribing?",
  "Grüns Discount Codes: How to Save Money",
  "How to Cancel Grüns Subscription",

  // Purchasing & pricing
  "Grüns Price: Is It Worth the Cost?",
  "Grüns Cost Per Day: Breaking Down the Math",
  "Where to Buy Grüns Gummies",
  "Grüns on Amazon: Is It Legit?",
  "Grüns Free Trial: Does It Exist?",
  "Grüns Money Back Guarantee: How It Works",
  "Grüns VIP Program: What You Get",
  "Grüns Referral Code: How to Get Discounts",
  "Grüns Bulk Buying: Save Money on Large Orders",
  "Is Grüns on Sale? How to Find Deals",
  "Grüns vs Buying Vegetables: Is It Actually Cheaper?",
  "Grüns Gift Options: Buying for Someone Else",
  "Grüns Subscription vs One-Time Purchase",
  "Grüns Black Friday Deals",
  "Grüns Coupon: Current Offers",

  // Greens supplements general
  "What Are Greens Supplements and Do They Work?",
  "Greens Powders vs Greens Gummies: Which Is Better?",
  "Best Greens Supplements Ranked",
  "Do Greens Supplements Replace Vegetables?",
  "Benefits of Taking a Daily Greens Supplement",
  "How to Choose the Best Greens Supplement",
  "Greens Supplements for Gut Health: Top Picks",
  "Greens Supplements for Energy: What Actually Works",
  "Are Greens Supplements Safe?",
  "Greens Supplements Side Effects: What to Know",
  "Best Time to Take Greens Supplements",
  "Greens Supplements and Bloating: What Causes It",
  "Greens Supplements for Weight Loss: Do They Work?",
  "Greens Supplements vs Multivitamins: Which to Choose",
  "Greens Supplements for Athletes: Performance Benefits",
  "Greens Supplements During Pregnancy: Safety Guide",
  "Greens Supplements for Kids: Are They Safe?",
  "Greens Supplements for Seniors: Top Recommendations",
  "Greens Supplements on Keto: What You Need to Know",
  "Greens Supplements and Fasting: Safe to Combine?",

  // Superfoods content
  "What Are Superfoods and Why Do They Matter?",
  "Top 10 Superfoods Supported by Science",
  "Spirulina Benefits: Why It's in Every Greens Supplement",
  "Chlorella Benefits: The Ultimate Detox Superfood",
  "Wheatgrass Benefits: What the Research Shows",
  "Kale Benefits: Why It's Called a Superfood",
  "Spinach Nutrition: Benefits of Eating More Greens",
  "Matcha Benefits: Energy Without the Jitters",
  "Ashwagandha Benefits: Stress and Adaptogen Guide",
  "Turmeric Benefits: Anti-Inflammatory Power",
  "Ginger Benefits: Digestion and Immunity",
  "Beet Root Benefits: Circulation and Performance",
  "Maca Root Benefits: Energy and Hormones",
  "Lion's Mane Benefits: Brain Health Superfood",
  "Reishi Mushroom Benefits: Immunity and Stress",
  "Elderberry Benefits: Natural Immunity Support",
  "Acai Benefits: Antioxidant Superfood Guide",
  "Blueberry Benefits: Brain and Antioxidant Powerhouse",
  "Prebiotic Foods: How to Feed Your Gut Bacteria",
  "Probiotic vs Prebiotic: What's the Real Difference?",

  // Gut health deep dives
  "The Gut-Brain Connection: How Your Microbiome Affects Mood",
  "Signs Your Gut Health Is Poor",
  "How to Improve Gut Health Naturally",
  "Best Foods for Gut Health",
  "How Prebiotics Support a Healthy Microbiome",
  "Leaky Gut Syndrome: Causes and Natural Solutions",
  "Gut Health and Immunity: The Connection Explained",
  "Gut Health and Skin: How They're Related",
  "Gut Health and Weight: Does the Microbiome Affect Weight?",
  "Gut Health and Sleep: The Connection Explained",
  "Foods That Destroy Gut Health",
  "How Long Does It Take to Heal Gut Health?",
  "Gut Health Supplements: What Actually Works",
  "Gut Health for Athletes: Performance and Recovery",
  "Gut Health After Antibiotics: How to Recover",

  // Nutrition & wellness
  "How to Get More Greens in Your Diet",
  "Why Most People Are Nutrient Deficient",
  "The Best Daily Supplements for Overall Health",
  "How to Build a Daily Supplement Routine",
  "Vitamins vs Supplements: What's the Difference?",
  "Bioavailability: Why How You Take Supplements Matters",
  "Whole Foods vs Supplements: Can You Replace One?",
  "How to Read a Supplement Label",
  "Red Flags in Supplement Marketing to Watch Out For",
  "Third Party Tested Supplements: Why It Matters",
  "Synthetic vs Natural Vitamins: Which Is Better?",
  "Micronutrient Deficiencies: Signs and Solutions",
  "The Best Supplements for Immune System Support",
  "Supplements for Stress and Anxiety",
  "Supplements for Better Sleep",
  "Supplements for Hormonal Balance",
  "Supplements for Healthy Hair and Nails",
  "Supplements for Clear Skin",
  "Supplements for Muscle Recovery",
  "The Best Anti-Aging Supplements",

  // Lifestyle angles
  "How to Stay Healthy When You Hate Cooking",
  "Nutrition Hacks for Busy People",
  "How to Eat Healthier Without Changing Your Diet",
  "Easy Ways to Get More Nutrients Every Day",
  "Morning Routine for Better Health and Energy",
  "How to Build Sustainable Healthy Habits",
  "The 80/20 Rule for Nutrition: What It Means",
  "Nutrition Myths Debunked by Science",
  "How to Boost Energy Without Caffeine",
  "Natural Ways to Improve Digestion",
  "How to Reduce Bloating Naturally",
  "How to Strengthen Your Immune System",
  "How to Improve Focus and Concentration Naturally",
  "How to Reduce Inflammation Through Diet",
  "How to Support Detoxification Naturally",

  // FAQ-style
  "Are Grüns Gummies FDA Approved?",
  "Are Grüns Gummies Safe?",
  "Do Grüns Gummies Actually Work?",
  "Can Grüns Replace a Multivitamin?",
  "Are Grüns Gummies Good for You?",
  "Do Grüns Gummies Have Caffeine?",
  "Are Grüns Gummies Non-GMO?",
  "Do Grüns Gummies Contain Allergens?",
  "Are Grüns Gummies Organic?",
  "How Are Grüns Gummies Made?",
  "Who Makes Grüns Gummies?",
  "Is Grüns a Legit Company?",
  "How Long Has Grüns Been Around?",
  "Does Grüns Have Good Customer Service?",
  "What Is Grüns Return Policy?",
  "How Does Grüns Shipping Work?",
  "Can You Get Grüns at Walmart or Target?",
  "Is Grüns Available Internationally?",
  "Does Grüns Have a Loyalty Program?",
  "What Are Customers Saying About Grüns on TrustPilot?",

  // Comparison with food
  "Grüns vs Eating a Salad Every Day: Which Is Better?",
  "Grüns vs Green Juice: Which Gives More Nutrients?",
  "Grüns vs Smoothie: Best Way to Get Your Greens",
  "Grüns vs Eating Vegetables: Can Supplements Replace Them?",
  "Grüns vs Fruit: Does It Count Toward Daily Servings?",
  "Grüns vs Fiber Supplements: How Are They Different?",
  "Grüns vs Protein Powder: Can You Stack Them?",
  "Grüns vs Collagen: Which Should You Take?",
  "Grüns vs Fish Oil: Different Benefits Explained",
  "Grüns vs Vitamin D: Do You Still Need It?",

  // Trending health topics
  "Greens Gummies: The Trend Everyone Is Talking About",
  "Why Greens Gummies Are Replacing Powders",
  "The Rise of Functional Gummies: What's the Appeal?",
  "Supplements in Gummy Form: Pros and Cons",
  "Why Gen Z Is Obsessed with Greens Supplements",
  "TikTok Greens Supplements: What Actually Works",
  "Are Influencer-Promoted Supplements Worth It?",
  "The Gut Health Trend: What's Driving It?",
  "Biohacking Your Nutrition: Where to Start",
  "The Best Wellness Products Worth Buying",

  // Specific health conditions
  "Grüns for Fatigue: Can Superfoods Fight Tiredness?",
  "Grüns for Thyroid Health",
  "Grüns for PCOS: Nutrition Support",
  "Grüns for Menopause: Managing Symptoms Naturally",
  "Grüns for High Blood Pressure",
  "Grüns for Cholesterol: Do Greens Help?",
  "Grüns for Anxiety: Calming Superfoods",
  "Grüns for Depression: Nutrition and Mood",
  "Grüns for Acne: Clearing Skin from the Inside",
  "Grüns for Eczema: Anti-Inflammatory Diet Support",

  // More how-to and educational
  "How to Build a Complete Daily Supplement Stack",
  "Morning vs Evening Supplements: When to Take What",
  "How to Track Your Supplement Routine",
  "Why Consistency Matters More Than Dosage",
  "How to Tell If Your Supplements Are Working",
  "Supplements for Beginners: Where to Start",
  "The Most Important Supplements for Your 20s",
  "The Most Important Supplements for Your 30s",
  "The Most Important Supplements for Your 40s",
  "The Most Important Supplements for Your 50s and Beyond",

  // Environmental and ethical
  "Is Grüns Environmentally Friendly?",
  "Grüns Packaging: Is It Sustainable?",
  "Ethical Supplement Brands Worth Supporting",
  "Organic Greens Supplements: Are They Worth Extra Cost?",
  "Sustainable Nutrition: How to Make Healthier Choices",

  // Bonus long-tail
  "Grüns Gummies vs Capsules: Which Absorbs Better?",
  "Grüns Bear Gummies: Why the Bear Shape?",
  "Grüns 28 Pack: How Long Does It Last?",
  "Grüns Daily Pack: Everything That Comes in One Serving",
  "Grüns Fresh and Sweet Taste: Flavor Review",
  "Grüns Sugar Free Formula: How They Sweeten It",
  "Grüns Comprehensive Nutrition: What That Means",
  "Grüns vs Single Ingredient Supplements",
  "Grüns Proprietary Blend: Is It Transparent?",
  "Grüns Certificate of Analysis: What to Look For",
  "Why Grüns Uses a Gummy Form Factor",
  "Grüns Absorption Rate vs Powders and Pills",
  "Grüns Before Bed: Is It a Good Idea?",
  "Grüns Taste After Workout: Does It Help Recovery?",
  "Grüns in Winter: Immunity and Vitamin D",
  "Grüns in Summer: Hydration and Energy",
  "Grüns for Cold and Flu Season",
  "Grüns and Probiotics: Do You Need Both?",
  "Grüns and Collagen: Perfect Daily Stack?",
  "Grüns and Omega-3: Combining for Better Health",
  "Grüns and Creatine: Gym Stack Review",
  "Grüns and Vitamin D: Completing Your Stack",
  "Grüns and Iron: What Women Should Know",
  "Grüns and Calcium: Bone Health Supplement Guide",
  "Grüns for Post-COVID Recovery",
  "Grüns for Long COVID Fatigue",
  "Grüns and Mental Health: The Nutrition Connection",
  "Grüns and Gut Microbiome Research",
  "Grüns Science: What Research Backs the Ingredients?",
  "Grüns Clinical Evidence: What Studies Show",
  "Grüns Physician Review: What Doctors Say",
  "Grüns Dietitian Opinion: Is It Nutritionally Sound?",
  "Grüns as a Meal Replacement: Is That Possible?",
  "Grüns for Night Shift Workers",
  "Grüns for Office Workers: Combating Sedentary Lifestyle",
  "Grüns for Outdoor Enthusiasts: Hiking and Nature",
  "Grüns for Yoga Practitioners",
  "Grüns for CrossFit Athletes",
  "Grüns for Marathon Runners",
  "Grüns for Cyclists: Endurance Nutrition",
  "Grüns for Swimmers: Recovery Nutrition",
  "Grüns for Team Sport Athletes",
  "Grüns for Weekend Warriors: Casual Exercise Nutrition",
];

function slugify(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
}

async function generateArticle(groq: Groq, cerebras: Cerebras, topic: string, index: number): Promise<void> {
  const slug = slugify(topic);
  const outPath = path.join("content", "articles", `${slug}.json`);

  if (fs.existsSync(outPath)) {
    const existing = JSON.parse(fs.readFileSync(outPath, "utf-8"));
    if (!existing.error) { console.log(`[${index + 1}/500] SKIP: ${topic}`); return; }
    fs.unlinkSync(outPath);
  }

  const prompt = `Write a comprehensive, SEO-optimized article titled "${topic}" for a website about Grüns greens gummies.

REQUIREMENTS:
- 800-1200 words
- Helpful, friendly tone
- Naturally mention "Grüns" throughout
- Include H1, H2, H3 sections with short paragraphs
- First line MUST be: META: <120-160 char meta description>
- Second line MUST be: KEYWORDS: keyword1, keyword2, keyword3, keyword4, keyword5
- Write in clean HTML: h1, h2, h3, p, ul, li, strong tags only
- Do NOT include any buttons, links, CTAs, or calls to action
- Do NOT include phrases like "Try Grüns", "Get Grüns", "Buy Now", "Click here"
- Do NOT include any markdown — only HTML tags
- Do NOT include a References, Sources, or Citations section
- Genuinely helpful, informative content only

Article title: ${topic}`;

  try {
    let content = "";

    if (useGroq) {
      try {
        const completion = await groq.chat.completions.create({
          model: "llama-3.3-70b-versatile",
          messages: [{ role: "user", content: prompt }],
          max_tokens: 2000,
          temperature: 0.8,
        });
        content = completion.choices[0]?.message?.content ?? "";
      } catch (groqErr: unknown) {
        const msg = String(groqErr);
        if (msg.includes("429") || msg.includes("rate_limit") || msg.includes("tokens per day")) {
          console.log("Groq quota hit -- switching to Cerebras");
          useGroq = false;
        } else { throw groqErr; }
      }
    }

    if (!useGroq || !content) {
      if (useCerebras) {
        try {
          const completion = await cerebras.chat.completions.create({
            model: "llama3.1-8b",
            messages: [{ role: "user", content: prompt }],
            max_tokens: 2000,
            // @ts-ignore
            temperature: 0.8,
          });
          // @ts-ignore
          content = (completion.choices[0]?.message?.content as string) ?? "";
          console.log(`[${index + 1}/500] Cerebras: ${topic}`);
        } catch (cerebrasErr: unknown) {
          const msg = String(cerebrasErr);
          if (msg.includes("429") || msg.includes("rate") || msg.includes("limit")) {
            console.log("Cerebras rate limited -- switching to Gemini");
            useCerebras = false;
          } else { throw cerebrasErr; }
        }
      }

    }

    // Handle both "META:" and "**Meta Description:**" formats (Cerebras uses markdown)
    const metaMatch = content.match(/META:\s*(.+)/) || content.match(/\*?\*?Meta Description:?\*?\*?\s*(.+)/i);
    const kwMatch = content.match(/KEYWORDS:\s*(.+)/) || content.match(/\*?\*?Keywords?:?\*?\*?\s*(.+)/i);
    const metaDescription = metaMatch ? metaMatch[1].replace(/\*\*/g, "").trim() : `Learn about ${topic} and how Grüns greens gummies can help.`;
    const keywords = kwMatch ? kwMatch[1].replace(/\*\*/g, "").split(",").map((k) => k.trim()) : ["Grüns", "greens gummies", "superfoods", "greens supplement"];

    // Strip meta/keywords lines, convert markdown to HTML if needed, replace CTAs
    let body = content
      .replace(/META:\s*.+\n?/g, "")
      .replace(/KEYWORDS:\s*.+\n?/g, "")
      .replace(/\*?\*?Meta Description:?\*?\*?.*\n?/gi, "")
      .replace(/\*?\*?Keywords?:?\*?\*?.*\n?/gi, "");

    // Convert markdown to HTML if Cerebras returned markdown
    if (body.includes("## ") || body.includes("### ") || body.includes("**")) {
      body = marked.parse(body) as string;
    }

    body = body.replace(/\[CTA[^\]]*\]/gi, `<a href="${AFFILIATE}" class="cta-link">Try Grüns VIP →</a>`);

    const article = { slug, title: topic, metaDescription, keywords, body, generatedAt: new Date().toISOString() };
    fs.writeFileSync(outPath, Buffer.from(JSON.stringify(article, null, 2), "utf-8"));
    console.log(`[${index + 1}/500] DONE: ${topic}`);
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error(`[${index + 1}/500] ERROR: ${topic} — ${msg}`);
    fs.writeFileSync(outPath, Buffer.from(JSON.stringify({ slug, title: topic, metaDescription: "", keywords: [], body: "", generatedAt: new Date().toISOString(), error: msg }, null, 2), "utf-8"));
  }

  await new Promise((r) => setTimeout(r, 13000));
}

async function main() {
  const envPath = path.join(process.cwd(), ".env.local");
  if (fs.existsSync(envPath)) {
    fs.readFileSync(envPath, "utf-8").split("\n").forEach((line) => {
      const [k, ...v] = line.split("=");
      if (k && v.length) process.env[k.trim()] = v.join("=").trim();
    });
  }

  // Parse CLI args: --limit N
  const limitArg = process.argv.find(arg => arg.startsWith("--limit"));
  const limit = limitArg ? parseInt(limitArg.split("=")[1]) : ARTICLE_TOPICS.length;

  const groqKey = process.env.GROQ_API_KEY;
  const cerebrasKey = process.env.CEREBRAS_API_KEY;
  if (!groqKey && !cerebrasKey) { console.error("ERROR: No API keys in .env.local"); process.exit(1); }
  if (!groqKey) { useGroq = false; console.log("Groq key missing — Cerebras only"); }

  if (!groqKey && !cerebrasKey) { console.error("ERROR: No API keys in .env.local"); process.exit(1); }

  const groq = new Groq({ apiKey: groqKey ?? "none" });
  const cerebras = new Cerebras({ apiKey: cerebrasKey ?? "none" });

  fs.mkdirSync(path.join("content", "articles"), { recursive: true });
  console.log(`Generating up to ${limit} new articles...`);
  let generated = 0;
  for (let i = 0; i < ARTICLE_TOPICS.length && generated < limit; i++) {
    const existingPath = path.join("content", "articles", `${slugify(ARTICLE_TOPICS[i])}.json`);
    const existing = fs.existsSync(existingPath) && JSON.parse(fs.readFileSync(existingPath, "utf-8"));
    if (existing && !existing.error) continue; // Skip already generated
    await generateArticle(groq, cerebras, ARTICLE_TOPICS[i], i);
    generated++;
  }
  console.log(`Done! Generated ${generated} article(s)`);
}

main().catch(console.error);
