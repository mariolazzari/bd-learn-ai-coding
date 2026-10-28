import { Plugin } from "@opencode/plugin";
import { spawn } from "node:child_process";
import { readdir } from "node:fs/promises";
import path from "node:path";

// This file lives at <project root>/.opencode/plugins/example-outputs.ts
const PROJECT_ROOT = path.resolve(import.meta.dir, "../..");
const EXAMPLES_DIR = path.join(PROJECT_ROOT, "examples");
const UV = process.env.UV_BIN ?? "uv";
const EXTRA_PATH = [
  path.join(process.env.HOME ?? "", ".local", "bin"),
  "/opt/homebrew/bin",
  "/usr/local/bin",
].join(path.delimiter);
const CHILD_ENV = {
  ...process.env,
  PATH: [process.env.PATH ?? "", EXTRA_PATH].filter(Boolean).join(path.delimiter),
};

type ExampleResult = {
  name: string;
  exitCode: number;
  firstLine: string;
};

function runExample(file: string): Promise<{ stdout: string; exitCode: number }> {
  return new Promise((resolve, reject) => {
    const child = spawn(UV, ["run", "--no-active", "sloperator.py", file], {
      cwd: PROJECT_ROOT,
      env: CHILD_ENV,
    });

    let stdout = "";
    child.stdout?.setEncoding("utf8");
    child.stdout?.on("data", (chunk: string) => {
      stdout += chunk;
    });
    child.stderr?.resume();

    child.on("error", reject);
    child.on("close", (code) => {
      resolve({ stdout, exitCode: code ?? 1 });
    });
  });
}

async function collectExamples(): Promise<ExampleResult[]> {
  const entries = await readdir(EXAMPLES_DIR);
  const files = entries.filter((name) => name.endsWith(".slop")).sort();

  return Promise.all(
    files.map(async (name) => {
      const { stdout, exitCode } = await runExample(path.join(EXAMPLES_DIR, name));
      return { name, exitCode, firstLine: stdout.split("\n")[0] ?? "" };
    }),
  );
}

export default Plugin.define({
  id: "sloperator.example-outputs",
  setup: async (ctx) => {
    await ctx.tool.transform((tools) => {
      tools.add({
        name: "example_outputs",
        description:
          "Run every examples/*.slop file and return each example's name, exit code, and first output line",
        input: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async () => {
          const examples = await collectExamples();
          return { content: JSON.stringify({ examples }, null, 2) };
        },
      });
    });
  },
});
