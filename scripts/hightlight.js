import fs from "fs";
import path from "path";
import { createHighlighter } from "shiki";

const moonbitLang = JSON.parse(
  fs.readFileSync("tmlang/grammars/moonbit.tmLanguage.json", "utf8")
);

function findHtmlFiles(directory) {
  const files = [];
  function traverse(dir) {
    const entries = fs.readdirSync(dir);
    for (const entry of entries) {
      const fullPath = path.join(dir, entry);
      const stats = fs.statSync(fullPath);
      if (stats.isDirectory()) {
        traverse(fullPath);
      } else if (
        stats.isFile() &&
        path.extname(fullPath).toLowerCase() === ".html"
      ) {
        files.push(fullPath);
      }
    }
  }
  traverse(directory);
  return files;
}

function unescapeHtml(html) {
  const htmlEntities = {
    "&lt;": "<",
    "&gt;": ">",
    "&amp;": "&",
    "&quot;": '"',
    "&#39;": "'",
    "&apos;": "'",
    "&nbsp;": " ",
    "&copy;": "©",
    "&reg;": "®",
    "&trade;": "™",
    "&hellip;": "…",
    "&mdash;": "—",
    "&ndash;": "–",
    "&bull;": "•",
    "&lsquo;": "'",
    "&rsquo;": "'",
    "&ldquo;": '"',
    "&rdquo;": '"',
  };

  let unescaped = html.replace(/&[a-zA-Z0-9]+;/g, (entity) => {
    return htmlEntities[entity] || entity;
  });

  unescaped = unescaped.replace(/&#(\d+);/g, (_, dec) => {
    return String.fromCharCode(parseInt(dec, 10));
  });

  unescaped = unescaped.replace(/&#x([0-9a-fA-F]+);/g, (_, hex) => {
    return String.fromCharCode(parseInt(hex, 16));
  });

  return unescaped;
}

const highlighter = await createHighlighter({
  themes: ["light-plus", "dark-plus"],
  langs: [moonbitLang],
});

function highlightMoonbitCode(code) {
  const unescapedCode = unescapeHtml(code);
  return highlighter.codeToHtml(unescapedCode, {
    lang: "moonbit",
    themes: {
      light: "light-plus",
      dark: "dark-plus",
    },
  });
}

function processHtmlFile(filePath) {
  let content = fs.readFileSync(filePath, "utf8");
  const codeBlockRegex =
    /<pre><code class="language-moonbit">([\s\S]*?)<\/code><\/pre>/g;
  if (content.match(codeBlockRegex)) {
    content += "<link rel='stylesheet' href='/shiki.css'>";
    content = content.replace(codeBlockRegex, (match, codeContent) => {
      try {
        const highlighted = highlightMoonbitCode(codeContent);
        return `<div>${highlighted}</div>`;
      } catch (error) {
        console.error(`Highlight error: ${error.message}`);
        return match;
      }
    });
  }
  fs.writeFileSync(filePath, content, "utf8");
  console.log(`Highlighted: ${filePath}`);
}

async function main() {
  const targetDir = "./trees/publish";
  try {
    const htmlFiles = findHtmlFiles(targetDir);
    for (const file of htmlFiles) {
      processHtmlFile(file);
    }
  } catch (error) {
    console.error(`Highlight error: ${error.message}`);
  }
  fs.copyFileSync("./styles/shiki.css", "./trees/publish/shiki.css");
}

main();
