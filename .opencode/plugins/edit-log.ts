import { Plugin } from "@opencode/plugin";
import { appendFile, mkdir } from "node:fs/promises";
import path from "node:path";

// This file lives at <project root>/.opencode/plugins/edit-log.ts
const PROJECT_ROOT = path.resolve(import.meta.dir, "../..");
const LOG_PATH = path.join(PROJECT_ROOT, "logs", "plugin-tools.log");
const LOGGED_TOOLS = new Set(["edit", "write", "patch"]);

export default Plugin.define({
  id: "sloperator.edit-log",
  setup: async (ctx) => {
    await ctx.tool.hook("execute.after", async ({ tool, status }) => {
      if (status !== "completed" || !LOGGED_TOOLS.has(tool)) return;
      await mkdir(path.dirname(LOG_PATH), { recursive: true });
      await appendFile(
        LOG_PATH,
        JSON.stringify({ tool, status: "completed" }) + "\n",
        "utf8",
      );
    });
  },
});
