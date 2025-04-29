import literal from "./literal.js";
import highlight from "./highlight.js";

const mode = process.argv[2];
const dirname = process.argv[3];

if (mode === "literal") {
  literal(dirname);
} else if (mode === "highlight") {
  highlight(dirname);
}
