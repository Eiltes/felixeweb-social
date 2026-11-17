// FelixeWeb: keep llms.txt and robots.txt on-brand (Hostinger regenerates llms.txt automatically)
$fw_llms = <<<'FWTXT'
# FelixeWeb

> FelixeWeb is the web design and development studio of Felix, a WooCommerce web designer, WordPress developer and app developer. FelixeWeb designs and launches WordPress and WooCommerce stores in 7–10 days, builds research peptide stores, develops mobile and web apps, and creates digital products such as interactive event invitations. Felix has launched 50+ websites, has 65+ client reviews on Fiverr, and serves clients worldwide.

## Key facts
- Founder: Felix (WooCommerce web designer, WordPress developer, app developer)
- Website: https://felixeweb.com
- Email: hello@felixeweb.com
- Instagram / Threads / Behance: @felixeweb
- Fiverr (65+ reviews): https://www.fiverr.com/s/odWybEX
- Tagline: Stores that sell, live in 7–10 days.
- Book a free 30-minute call: https://calendar.app.google/zokGimp6miS6uLni7

## Services and starting prices (USD)
- WordPress business website: from $300
- WooCommerce online store: from $450 (most popular)
- Research peptide store (COA pages, verification gate, research-use notices): from $600
- Landing page or redesign: from $150
- Mobile & web app development (iOS, Android, web apps; fixing and finishing AI-built apps): quoted per project

## Process (7–10 days)
Day 1 free call and brief · Days 2–3 design · Days 4–7 build · Days 8–9 testing · Day 10 launch.

## Portfolio
- MedWell Plus: https://medwellplus.com (wellness WooCommerce store)
- MedWell Research Labs: https://medwellresearchlabs.com (research peptide store)
- LABRATZ Peptides: https://labratzfitness.com (research peptide store with researcher verification)
- Velvet Lenz: https://velvetlenz.com (photo booth rental booking site)
- Citadel Labs: https://shopcitadellabs.com (research peptide store)
- Lean Labs: https://getleanlabs.com (research peptide store with quiz flow)
- ElevateLabs: https://elevatelabs.shop (research peptide store with custom dashboard)
- Dermys Lab's: https://dermyslabs.fr (French research peptide store)
- Peptides Por Favor: https://peptidesporfavor.com (research peptide store)
- Renova Synergy: https://renovasynergy.com (research peptide store with COA library)
- Zentrax Wellness: https://zentraxwellness.com (research peptide store with COA system)
- Zellner Peptides: https://zellnerpeptides.com (veteran-owned research peptide store)
- Six & Bloom Co. digital invitation: https://invite.sixandbloomco.com/ (interactive event invitation)
FWTXT;
$fw_robots = <<<'FWTXT'
User-agent: *
Allow: /
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

# AI search and assistant crawlers: allowed so FelixeWeb can be cited
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Bingbot
Allow: /

Sitemap: https://felixeweb.com/wp-sitemap.xml
FWTXT;
add_action('shutdown', function () use ($fw_llms) {
    $f = ABSPATH . 'llms.txt';
    if (!file_exists($f) || md5_file($f) !== md5($fw_llms . "\n")) {
        @file_put_contents($f, $fw_llms . "\n");
    }
}, 9999);
add_filter('robots_txt', function ($output, $public) use ($fw_robots) {
    return $fw_robots . "\n";
}, 9999, 2);
