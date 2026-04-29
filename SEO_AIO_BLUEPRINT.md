# Master Blueprint: Hyper-SEO & AIO Architecture

**Project Scope:** Machine-Readable Authority & Search Engine Dominance  
**Target:** High-End Digital Archives and Technical Institutions  
**Architect:** Mema (via Glass Gallery Project)  
**Reference:** Google Search Essentials & SEO Starter Guide (developers.google.com, April 2026)

---

## 0. Foundational Compliance: Google Search Essentials

Before any advanced optimization, the site must satisfy Google's baseline eligibility requirements. A site violating these will not rank regardless of schema quality.

### 0.1 Crawlability

Google must be able to access and render the page exactly as a user would. This means:

- CSS and JavaScript must not be blocked in `robots.txt`. Blocking them prevents Google from understanding page rendering and layout.
- The primary content must not be gated behind user interactions (clicks, swipes, form submissions). Lazy-loaded content must be crawlable without interaction.
- Use Google Search Console's URL Inspection tool to verify Google's rendered view of any page.

### 0.2 XML Sitemap

Submit a sitemap to Google Search Console. This is the most reliable signal to ensure all canonical URLs are discovered, especially on larger archives.

- Format: `sitemap.xml` at the root, submitted via Search Console.
- Include only canonical URLs. Exclude paginated or filtered variants unless they carry unique content.
- Update the `lastmod` timestamp accurately; do not use today's date for every URL — Google ignores inaccurate timestamps.

### 0.3 Robots.txt

Standardize the `robots.txt` to allow crawling of all assets required for rendering:

```
User-agent: *
Allow: /wp-content/uploads/
Allow: /*.css$
Allow: /*.js$
Disallow: /wp-admin/
Sitemap: https://yourdomain.com/sitemap.xml
```

The `$` anchor ensures the rule matches only URLs ending in `.css` or `.js`, not paths that happen to contain those strings.

Avoid blanket disallow rules. Disallowing CSS or JS files is a critical crawlability error.

---

## 1. The Strategy: E-E-A-T Sovereign Authority

The goal is to move beyond tags and establish a Knowledge Graph. This links the digital project to a verified human expert and a formal institution.

Google's E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) framework is a quality signal used by Search Quality Raters and informs core ranking systems. It is reinforced through structured data, not replaced by it.

### 1.1 Personal Identity Mapping

Every project must be anchored to a unique Global ID (e.g., `.../porto/#person`). This ID must be referenced across all schema blocks (Organization, WebSite, Article) to prove undisputed authorship.

### 1.2 The SameAs Social Graph

AI models and Google's Knowledge Graph use the `sameAs` array to verify authority. Include:

- Professional Portfolio
- GitHub Profile (Technical Authority)
- LinkedIn (Professional Identity)
- X/Medium (Social/Knowledge Authority)

### 1.3 Content Authority

Structured data amplifies content authority — it does not substitute for it. Google's systems reward original, useful content that matches user intent. Every page must demonstrate genuine expertise through its written content before schema signals carry weight.

---

## 2. Technical Implementation: The Metadata Layer

### 2.1 Dynamic Intelligence Engine

Metadata must be context-aware.

- **Articles:** Pull 25-word excerpts, automated keywords from tags/categories.
- **Root:** Use the high-level mission/tagline as the description.
- **Canonical Anchoring:** Force the root URL on the home page and specific permalinks on subpages to prevent duplicate content indexing.

### 2.2 Title Tag Optimization

Title tags are the primary snippet signal in Google Search results. Each page must have a unique, descriptive title.

- Length: 50–60 characters (Google truncates beyond ~600px display width).
- Format: `[Primary Keyword] — [Brand Name]` for articles; `[Brand Name]: [Tagline]` for root.
- Do not repeat the brand name across every page title identically.

### 2.3 Machine-Readable Controls (Robots)

Standardize on: `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1`.

### 2.4 Duplicate Content

Duplicate content is not a penalty, but it dilutes crawl budget and split link equity. Resolution strategy:

1. Self-referencing canonical tags on all pages.
2. Redirect `www` to non-`www` (or vice versa) consistently — never serve both.
3. Redirect HTTP to HTTPS at the server level, not via plugin.

---

## 3. The AIO Layer: Full AI Optimization Stack

AIO has three distinct targets with different signal sets. Treat them as separate layers that compound each other.

| Target | Primary Signal | Schema |
|---|---|---|
| Google AI Overviews | Passage indexing, E-E-A-T, FAQ | FAQPage, Article, Speakable |
| LLM citation (Perplexity, ChatGPT) | Entity consistency, external citations | Organization, Person, sameAs |
| Voice AI (Google Assistant, Siri) | SpeakableSpecification CSS selectors | Speakable |

---

### 3.1 Google AI Overviews (AIO Citation)

Google's AI Overviews pull from pages already ranked in the top results. The primary citation signals are:

**Passage Indexing Compliance**

Google indexes individual passages, not just full pages. Each section must function as a standalone answer. Structure every `<h2>` block to answer one specific question completely within its own scope. Do not split answers across sections.

**Direct Answer Placement**

Place the core answer within the first 2–3 sentences after a heading. AI Overviews extract the closest concise answer to a query. Burying the answer after preamble reduces citation probability.

**FAQ Schema**

Add `FAQPage` schema to any page containing question-based headings. This is the highest-signal schema for AI Overview inclusion.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is the Glass Gallery archive?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "The Glass Gallery is a digital archive of..."
    }
  }]
}
```

**HowTo Schema**

Use `HowTo` schema for any procedural/instructional content. AI systems parse step-by-step structure natively.

**Freshness Signal**

AI Overviews prefer recently updated sources. `dateModified` in Article schema must be accurate and updated on substantive edits. Do not fake this date — Google cross-references crawl timestamps.

---

### 3.2 LLM Citation Optimization (Perplexity, ChatGPT, Claude)

LLMs cite sources they encountered during training or via web retrieval. Both paths require the same foundation: entity consistency across the web.

**Entity Consistency**

The Person entity (Azzar Budiyanto) must be described with the same name, role, and identifiers across every platform in the `sameAs` array. Inconsistency across LinkedIn, GitHub, and the portfolio reduces Knowledge Graph confidence. LLMs use this cross-reference to verify the entity is real and authoritative.

**External Citation Acquisition**

LLMs weight pages that are cited by other authoritative sources. Prioritize getting linked from:

- GitHub READMEs referencing your work
- Technical documentation or tutorials citing your projects
- Academic or institutional sources

A single citation from a high-authority domain outweighs hundreds of low-authority links.

**`mentions` and `citation` Schema Properties**

In Article schema, use the `mentions` property to explicitly reference entities discussed in the content. This helps LLMs map your content to known Knowledge Graph nodes.

```json
{
  "@type": "Article",
  "mentions": [
    { "@type": "SoftwareApplication", "name": "WordPress" },
    { "@type": "Person", "@id": "https://yourdomain.com/porto/#person" }
  ]
}
```

**llms.txt (Emerging Standard)**

An emerging convention (adopted by Anthropic, Perplexity, and others) is a plain-text `llms.txt` file at the root that gives LLMs a structured index of the site's content and permissions. Format:

```
# Glass Gallery Archive

> Digital archive and technical portfolio of Azzar Budiyanto.

## Key Pages
- [Portfolio](https://yourdomain.com/porto/): Main portfolio index
- [Archive](https://yourdomain.com/archive/): Full project archive

## Permissions
LLMs may cite and summarize content from this domain.
```

This is not a Google signal — it targets ChatGPT plugins, Perplexity, and Claude's web retrieval.

---

### 3.3 JSON-LD Knowledge Graph: Modular Blocks

Do not use a single block; use modular JSON-LD blocks for 100% machine-readability.

**Critical constraint from Google:** Structured data must describe content that is visible to the user on the page. Do not add schema markup for information not rendered in the HTML output. Violations risk manual actions.

**3.3.1 WebSite Schema**

Defines the project's purpose and explicitly links to the Person ID as the author.

**3.3.2 Organization Schema**

Defines the institution. Links the Person ID as the Founder and includes the full `sameAs` authority array.

**3.3.3 Article Schema (with Speakable Support)**

Crucial for AI voice assistants (Alexa, Siri, Google Assistant).

- **CSS Selectors:** Provide specific selectors (e.g., `header h1`, `.prose`) in the `SpeakableSpecification` block so AI knows exactly what to read aloud.
- Include `datePublished` and `dateModified` in ISO 8601 format. Keep `dateModified` accurate — falsifying it is a quality violation.

**3.3.4 BreadcrumbList Schema**

Recommended for all pages with hierarchical depth. Aligns with mobile-first display and improves sitelinks appearance in SERPs.

---

## 4. Image & Media Optimization

Google indexes images and serves them through Google Images. Optimized media directly contributes to crawl coverage and rich result eligibility.

### 4.1 Images

- **Alt text:** Required on every content image. Describe the image content factually; do not keyword-stuff.
- **Dimensions:** Always declare explicit `width` and `height` attributes on `<img>` elements. This is the primary fix for Cumulative Layout Shift (CLS).
- **Format:** Use WebP or AVIF for raster images. Serve via `<picture>` element with fallbacks.
- **Filenames:** Use descriptive, hyphen-separated filenames (e.g., `glass-gallery-archive-2024.webp`), not `IMG_4892.jpg`.
- **Responsive:** Use `srcset` and `sizes` attributes for responsive delivery.

### 4.2 Videos

- Provide a `VideoObject` schema block with `name`, `description`, `thumbnailUrl`, `uploadDate`, and `duration`.
- Host a transcript or caption file; this is the primary source of text content Google extracts from video pages.

---

## 5. Connectivity & Core Web Vitals

Performance is a confirmed Google ranking signal. All three Core Web Vitals must pass the "Good" threshold at the 75th percentile of real Chrome user data (CrUX).

### 5.1 Core Web Vitals Thresholds

| Metric | What It Measures | Good | Needs Work | Poor |
|---|---|---|---|---|
| LCP (Largest Contentful Paint) | Loading performance | ≤ 2.5s | 2.5s–4.0s | > 4.0s |
| INP (Interaction to Next Paint) | Responsiveness | ≤ 200ms | 200ms–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | Visual stability | ≤ 0.1 | 0.1–0.25 | > 0.25 |

INP replaced FID in March 2024. It measures the full lifecycle of every interaction, not just the first one.

### 5.2 Implementation Targets (Production Budget)

| Asset | Target |
|---|---|
| Total JavaScript (compressed) | < 300 KB |
| Total CSS (compressed) | < 80 KB |
| Hero/LCP image | < 200 KB |
| Total page weight | < 1.5 MB |
| Third-party scripts | < 5 |

### 5.3 Connectivity Prefetch

- **DNS Prefetch:** For external assets (Google Fonts, analytics endpoints).
- **Preconnect:** For mission-critical external servers (CDN origin, font server).
- **LCP Image Preload:** Add `<link rel="preload" as="image">` for the hero image to front-load LCP.

### 5.4 Mobile-First Indexing

Google indexes the mobile version of all pages. This is not optional — it is the default for all sites. Violations cause indexing failures.

Mandatory requirements:

- Structured data must be identical on mobile and desktop renderings.
- Content must be identical on mobile and desktop. Content hidden in mobile accordions is still indexed.
- Do not use `noindex` or `nofollow` on the mobile version that is absent on desktop.
- Ensure the mobile `robots.txt` and canonical tags match desktop.
- `hreflang` tags, if used, must reference mobile-equivalent URLs correctly.

---

## 6. Architectural Dominance (The Interceptor)

Standard SEO plugins (Rank Math/Yoast) often create duplicate, conflicting metadata. Implement a Universal Output Sanitizer.

### 6.1 The Logic

1. **Buffer Capture:** Use `ob_start()` to capture the entire HTML output before it is sent to the browser.
2. **Surgical Removal:** Use RegEx to identify and remove all XHTML self-closing tags (` />`) commonly used by plugins.
3. **Schema Gatekeeping:** Use an allow-list logic. Intercept all `<script type="application/ld+json">` blocks and only preserve those that contain your project's specific identifiers (e.g., your Name or Institution Name).
4. **Singular Source of Truth:** This ensures your high-authority custom code is the only metadata search engines see.

**Note:** The Interceptor must preserve all structured data that corresponds to visible page content, per Google's structured data quality guidelines.

---

## 7. Anti-Patterns: What Not to Do

Google's official documentation explicitly identifies these as low or zero impact. Do not allocate engineering time to them.

- **Keyword stuffing:** Unnatural keyword repetition in content, alt text, or meta tags. Google's systems detect and discount this.
- **Exact-match domains:** A `.guru` or keyword-in-domain TLD provides negligible ranking benefit. Authority signals outweigh domain choice.
- **Directory submissions:** Third-party directory links have near-zero impact on modern ranking.
- **Meta keywords tag:** Google has ignored this tag since 2009. Do not populate it.
- **Duplicate structured data across every page:** Adding Article schema to non-article pages (e.g., contact page) creates noise without benefit.

---

## 8. Execution Checklist for Replicating Agents

**Baseline Compliance**
1. [ ] Confirm `robots.txt` does not block CSS, JS, or upload directories.
2. [ ] Submit XML sitemap to Google Search Console.
3. [ ] Verify Google can render the page via URL Inspection tool.
4. [ ] Confirm HTTP redirects to HTTPS at server level.
5. [ ] Confirm `www` and non-`www` redirect to a single canonical version.

**Identity & Schema**
6. [ ] Define Global ID: establish the `#person` anchor URL.
7. [ ] Authority Helper: build a function to return the social graph (`sameAs`).
8. [ ] Modular Header: inject individual WebSite, Org, and Article JSON-LD blocks.
9. [ ] Speakable IDs: identify primary content CSS classes for AI voice.
10. [ ] BreadcrumbList schema on all sub-pages.
11. [ ] FAQPage schema on all question-based content pages.
12. [ ] HowTo schema on all procedural/tutorial pages.
13. [ ] `mentions` property populated in Article schema with referenced entities.

**AIO (AI Optimization)**
14. [ ] Each `<h2>` section answers one question fully within its own scope (passage indexing).
15. [ ] Core answer placed in first 2–3 sentences after each heading.
16. [ ] `llms.txt` deployed at site root with content index and permissions.
17. [ ] Entity consistency verified: name and role match across all `sameAs` platforms.
18. [ ] At least one external citation from a high-authority domain (GitHub, academic, institutional).

**Metadata Layer**
19. [ ] Unique title tags on every page (50–60 characters).
20. [ ] Context-aware meta descriptions (25-word excerpts for articles, tagline for root).
21. [ ] Self-referencing canonical on every page.
22. [ ] Robots meta: `index, follow, max-image-preview:large, max-snippet:-1`.

**Media**
23. [ ] All content images have descriptive alt text.
24. [ ] All images have explicit `width` and `height` attributes.
25. [ ] Hero/LCP image is preloaded via `<link rel="preload">`.
26. [ ] Images served in WebP/AVIF with `<picture>` fallback.

**Performance**
27. [ ] LCP ≤ 2.5s at 75th percentile (measure via CrUX / Search Console).
28. [ ] INP ≤ 200ms at 75th percentile.
29. [ ] CLS ≤ 0.1 at 75th percentile.
30. [ ] DNS Prefetch and Preconnect for all external asset origins.

**Mobile**
31. [ ] Structured data identical on mobile and desktop.
32. [ ] Content parity between mobile and desktop versions.

**Interceptor**
33. [ ] Activate `ob_start` sanitizer to force-clean the HTML.
34. [ ] Verification: use `curl` to count `canonical` and `description` tags. Count must equal 1 each.

---

**Document Status: AUTHORITATIVE BLUEPRINT**  
*Generated for Azzar Budiyanto*  
*Last updated: April 2026 — aligned with Google Search Essentials & SEO Starter Guide (April 2026 refresh)*
