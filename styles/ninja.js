import 'ninja-keys';

export async function setupBlogSearch(jsonPath = '/kodama.json') {
  const ninja = document.querySelector('ninja-keys');
  if (!ninja) {
    console.warn('ninja-keys element not found');
    return;
  }

  // Set dark mode class if preferred
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    ninja.classList.add('dark');
  }

  try {
    const res = await fetch(jsonPath);
    if (!res.ok) throw new Error(`Failed to fetch ${jsonPath}`);
    const data = await res.json();

    const items = Object.entries(data).map(([key, value]) => {
      const title = value.title?.[0]?.Plain ?? key;
      const taxon = value.taxon?.[0]?.Plain ?? '';
      const slug = value.slug?.[0]?.Plain ?? key;
      return {
        id: key,
        title,
        section: taxon || 'Uncategorized',
        handler: () => {
          window.location.href = `/${slug}`;
        }
      };
    });

    ninja.data = items;
  } catch (err) {
    console.error('Load Error', err);
  }
}

window.addEventListener('DOMContentLoaded', () => setupBlogSearch());
