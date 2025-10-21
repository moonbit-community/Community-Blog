import fs from "node:fs";
import cp from "node:child_process";

function build() {
  fs.cpSync("trees", "__trees", { recursive: true });
  cp.execSync("node scripts/index.js literal __trees");
  cp.execSync("kodama build");
  cp.execSync("node scripts/index.js highlight __trees");
  fs.rmSync("publish", { recursive: true, force: true });
  fs.cpSync("__trees/publish", "publish", { recursive: true });
  fs.rmSync("__trees", { recursive: true, force: true });
}

export default build;
