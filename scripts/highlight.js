import fs from "fs";
import path from "path";
import { createHighlighter, codeToHtml } from "shiki";

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

async function processHtmlFile(filePath) {
  let content = fs.readFileSync(filePath, "utf8");
  const codeBlockRegex =
    /<pre><code class="language-([\w-]+)">([\s\S]*?)<\/code><\/pre>/g;
  if (content.match(codeBlockRegex)) {
    content += "<link rel='stylesheet' href='/shiki.css'>";

    const matches = Array.from(content.matchAll(codeBlockRegex));
    for (const match of matches) {
      const [fullMatch, language, codeContent] = match;
      try {
        let highlighted;
        if (language === "moonbit" || language === "mbt") {
          highlighted = highlightMoonbitCode(codeContent);
        } else {
          highlighted = await codeToHtml(codeContent, {
            lang: language,
            themes: {
              light: "light-plus",
              dark: "dark-plus",
            },
          });
        }
        content = content.replace(fullMatch, `<div>${highlighted}</div>`);
      } catch (error) {
        console.error(`Highlight error: ${error.message}`);
      }
    }
  }
  content = injectClicky(content);
  fs.writeFileSync(filePath, content, "utf8");
  console.log(`Highlighted: ${filePath}`);
}

function injectClicky(content) {
  return content.replace(
    /<\/body>/,
    `<script async data-id="101490373" src="//static.getclicky.com/js"></script></body>`
  );
}

async function main(dirname) {
  const targetDir = `${dirname}/publish`;
  console.log("Target directory:", targetDir);
  try {
    const htmlFiles = findHtmlFiles(targetDir);
    await Promise.all(htmlFiles.map((file) => processHtmlFile(file)));
  } catch (error) {
    console.error(`Highlight error: ${error.message}`);
    console.error("Error stack:", error.stack);
  }
  fs.copyFileSync("styles/shiki.css", `${dirname}/publish/shiki.css`);
  if (fs.existsSync("styles/main.css")) {
    fs.copyFileSync("styles/main.css", `${dirname}/publish/main.css`);
  }
  if (fs.existsSync("styles/catalog.js")) {
    fs.copyFileSync("styles/catalog.js", `${dirname}/publish/catalog.js`);
    const htmlFiles = findHtmlFiles(targetDir);
    for (const file of htmlFiles) {
      let html = fs.readFileSync(file, "utf8");
      if (!html.includes('<script src="/catalog.js"></script>')) {
        html = html.replace(
          /<\/body>/i,
          '<script src="/catalog.js"></script>\n</body>'
        );
        fs.writeFileSync(file, html, "utf8");
      }
    }
  }
}

export default main;
