import fs from "fs";
import path from "path";

function findMarkdownFiles(directory) {
  const files = [];
  const entries = fs.readdirSync(directory);
  for (const entry of entries) {
    const fullPath = path.join(directory, entry);
    if (fs.statSync(fullPath).isDirectory()) {
      files.push(...findMarkdownFiles(fullPath));
    } else if (path.extname(fullPath) === ".md") {
      files.push(fullPath);
    }
  }
  return files;
}

function findLiteralContent(path_, section) {
  const content = fs.readFileSync(path.join("code", path_), "utf8");
  const regex = new RegExp(
    `// section start ${section}[\\s\\S]*?// section end ${section}`,
    "g"
  );
  const match = content.match(regex);
  if (!match) return "";
  const lines = match[0].split("\n");
  if (lines.length <= 2) return "";
  return lines
    .filter((x) => x != "///|")
    .slice(1, -1)
    .join("\n").trim();
}

function injectLanguage(extname) {
  switch (extname) {
    case "mbt":
      return "moonbit";
    case "js":
      return "javascript";
    case "rs":
      return "rust";
    case "py":
      return "python";
    case "ts":
      return "typescript";
    case "lua":
      return "lua";
    case "sh":
      return "bash";
    case "toml":
      return "toml";
    case "json":
      return "json";
    case "yaml":
      return "yaml";
  }
}

function main(dirname) {
  const files = findMarkdownFiles(dirname);

  for (const file of files) {
    const content = fs.readFileSync(file, "utf8");
    const replaced = content.replace(
      /!\[([^[\]]+)\]\(([^.]+)\.([^#)]+)#:include\)/g,
      (_match, blockname, filepath, ext) =>
        `\`\`\`${injectLanguage(ext)}\n${findLiteralContent(
          `${filepath}.${ext}`,
          blockname
        )}\n\`\`\``
    );
    fs.writeFileSync(file, replaced, "utf8");
  }
}

export default main;
