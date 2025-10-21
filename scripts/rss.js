import fs from 'fs';
import path from 'path';

function generateRSS() {
  const kodamaPath = path.join('publish', 'kodama.json');
  if (!fs.existsSync(kodamaPath)) {
    console.error('kodama.json not found');
    return;
  }

  const data = JSON.parse(fs.readFileSync(kodamaPath, 'utf8'));

  const items = [];

  for (const [key, value] of Object.entries(data)) {
    const title = value.title?.[0]?.Plain || key;
    const taxon = value.taxon?.[0]?.Plain || '';
    const slug = value.slug?.[0]?.Plain || key;
    const date = value.date?.[0]?.Plain || '';

    if (taxon.startsWith('Blog') || taxon.startsWith('Weekly')) {
      const link = `https://moonbit.community/${slug}`;
      const pubDate = parseDate(date);

      items.push({
        title,
        link,
        description: title,
        pubDate,
        guid: link
      });
    }
  }

  // Sort by date descending
  items.sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate));

  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>MoonBit Community Blog</title>
<link>https://moonbit.community/</link>
<description>MoonBit Community Blog and Weekly Reports</description>
<language>zh-cn</language>
<atom:link href="https://moonbit.community/feed.xml" rel="self" type="application/rss+xml" />
${items.map(item => `
<item>
<title><![CDATA[${item.title}]]></title>
<link>${item.link}</link>
<description><![CDATA[${item.description}]]></description>
<pubDate>${item.pubDate}</pubDate>
<guid>${item.guid}</guid>
</item>`).join('')}
</channel>
</rss>`;

  fs.writeFileSync(path.join('publish', 'feed.xml'), rss);
  console.log('RSS feed generated');
}

function parseDate(dateStr) {
  // Handle formats like "2025/3/24 ~ 2025/4/6", "2023-3-23", or single date
  let match = dateStr.match(/(\d{4})\/(\d{1,2})\/(\d{1,2})/);
  if (!match) {
    match = dateStr.match(/(\d{4})-(\d{1,2})-(\d{1,2})/);
  }
  if (match) {
    const [, year, month, day] = match;
    const date = new Date(year, month - 1, day);
    return date.toUTCString();
  }
  return new Date().toUTCString();
}

export default generateRSS;