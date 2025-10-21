import fs from "node:fs";
import cp from "node:child_process";
import generateRSS from "./rss.js";

function build() {
  fs.cpSync("trees", "__trees", { recursive: true });
  cp.execSync("node scripts/index.js literal __trees");
  cp.execSync("kodama build --config kodama.toml");
  cp.execSync("node scripts/index.js highlight __trees");
  fs.rmSync("publish", { recursive: true, force: true });
  fs.cpSync("__trees/publish", "publish", { recursive: true });
  cp.execSync("npm run build");
  generateRSS();
  fs.rmSync("__trees", { recursive: true, force: true });
}

export default build;
