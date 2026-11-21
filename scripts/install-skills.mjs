#!/usr/bin/env node
// install-skills.mjs — Cross-platform symlink installer for JENGAI marketing-* skills and agents.
//
// Mirrors core-brain/scripts/brain-skills.mjs conventions:
// - Works identically on macOS, Linux, and Windows (Node 18+; symlinks or directory junctions)
// - Links skills instead of copying so git pulls update everything immediately
// - Supports deploying directly into a gtm-brain clone so brain-skills.mjs owns installation
//
// Usage:
//   node scripts/install-skills.mjs install [--agents claude,codex] [--dry-run]
//   node scripts/install-skills.mjs uninstall [--dry-run]
//   node scripts/install-skills.mjs check
//   node scripts/install-skills.mjs list
//   node scripts/install-skills.mjs sync-gtm-brain <path-to-gtm-brain> [--dry-run]

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const SKILLS_SRC = path.join(REPO_ROOT, "skills");
const AGENTS_SRC = path.join(REPO_ROOT, "agents");

const HOME = os.homedir();
const WIN = os.platform() === "win32";
const HUB = path.join(HOME, ".agents", "skills");
const AGENT_SKILL_DIRS = {
  claude: path.join(HOME, ".claude", "skills"),
  codex: path.join(HOME, ".codex", "skills"),
};
const CLAUDE_AGENTS_DIR = path.join(HOME, ".claude", "agents");

const [, , command = "help", ...rest] = process.argv;
let dryRun = false;
let selectedAgents = null;
const positional = [];

for (let i = 0; i < rest.length; i++) {
  const a = rest[i];
  if (a === "--dry-run") dryRun = true;
  else if (a === "--agents") selectedAgents = (rest[++i] ?? "").split(",").filter(Boolean);
  else positional.push(a);
}

function log(msg) { console.log(msg); }
function act(msg, fn) {
  if (dryRun) log(`  (dry) ${msg}`);
  else { fn(); log(`  ${msg}`); }
}
function lstatSafe(p) { try { return fs.lstatSync(p); } catch { return null; } }

function discoverSkills() {
  if (!fs.existsSync(SKILLS_SRC)) return [];
  return fs.readdirSync(SKILLS_SRC, { withFileTypes: true })
    .filter((d) => d.isDirectory() && fs.existsSync(path.join(SKILLS_SRC, d.name, "SKILL.md")))
    .map((d) => ({ name: d.name, dir: path.join(SKILLS_SRC, d.name) }))
    .sort((a, b) => a.name.localeCompare(b.name));
}

function discoverAgents() {
  if (!fs.existsSync(AGENTS_SRC)) return [];
  return fs.readdirSync(AGENTS_SRC, { withFileTypes: true })
    .filter((f) => f.isFile() && f.name.endsWith(".md"))
    .map((f) => ({ name: f.name, file: path.join(AGENTS_SRC, f.name) }))
    .sort((a, b) => a.name.localeCompare(b.name));
}

function ensureDirLink(target, dest) {
  const st = lstatSafe(dest);
  if (st) {
    if (st.isSymbolicLink()) {
      const cur = path.resolve(path.dirname(dest), fs.readlinkSync(dest));
      if (cur === target) return "ok";
      act(`repoint ${dest} -> ${target}`, () => {
        fs.unlinkSync(dest);
        fs.symlinkSync(target, dest, WIN ? "junction" : "dir");
      });
      return "repointed";
    }
    log(`  CONFLICT: ${dest} is a real directory/file; left untouched.`);
    return "conflict";
  }
  act(`link ${dest} -> ${target}`, () => {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.symlinkSync(target, dest, WIN ? "junction" : "dir");
  });
  return "created";
}

function ensureFileLink(target, dest) {
  const st = lstatSafe(dest);
  if (st) {
    if (st.isSymbolicLink()) {
      const cur = path.resolve(path.dirname(dest), fs.readlinkSync(dest));
      if (cur === target) return "ok";
      act(`repoint ${dest} -> ${target}`, () => {
        fs.unlinkSync(dest);
        fs.symlinkSync(target, dest, "file");
      });
      return "repointed";
    }
    log(`  CONFLICT: ${dest} is a real file; left untouched.`);
    return "conflict";
  }
  act(`link ${dest} -> ${target}`, () => {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    try {
      fs.symlinkSync(target, dest, "file");
    } catch {
      fs.copyFileSync(target, dest);
    }
  });
  return "created";
}

function detectTargets() {
  const names = selectedAgents ?? Object.keys(AGENT_SKILL_DIRS);
  const targets = {};
  for (const name of names) {
    if (!AGENT_SKILL_DIRS[name]) {
      console.error(`Unknown agent '${name}'. Valid: ${Object.keys(AGENT_SKILL_DIRS).join(", ")}`);
      process.exit(2);
    }
    if (selectedAgents || fs.existsSync(path.dirname(AGENT_SKILL_DIRS[name]))) {
      targets[name] = AGENT_SKILL_DIRS[name];
    }
  }
  return targets;
}

function cmdInstall() {
  const skills = discoverSkills();
  const agents = discoverAgents();
  const targets = detectTargets();

  log(`JENGAI AI Marketing Team — installing ${skills.length} skills and ${agents.length} subagents`);
  log(`Targets: ${Object.keys(targets).join(", ") || "hub only"}`);

  for (const sk of skills) {
    const hubDest = path.join(HUB, sk.name);
    ensureDirLink(sk.dir, hubDest);
    for (const dir of Object.values(targets)) {
      ensureDirLink(hubDest, path.join(dir, sk.name));
    }
  }
  if (targets.claude) {
    for (const ag of agents) {
      ensureFileLink(ag.file, path.join(CLAUDE_AGENTS_DIR, ag.name));
    }
  }
  log("Done. Start a new session to pick up updated skills and subagents.");
}

function cmdUninstall() {
  const skills = discoverSkills();
  const agents = discoverAgents();
  log("Removing JENGAI marketing-* links created by this repository...");
  for (const sk of skills) {
    for (const base of [HUB, ...Object.values(AGENT_SKILL_DIRS)]) {
      const dest = path.join(base, sk.name);
      const st = lstatSafe(dest);
      if (st?.isSymbolicLink()) {
        act(`unlink ${dest}`, () => fs.unlinkSync(dest));
      }
    }
  }
  for (const ag of agents) {
    const dest = path.join(CLAUDE_AGENTS_DIR, ag.name);
    const st = lstatSafe(dest);
    if (st?.isSymbolicLink()) {
      act(`unlink ${dest}`, () => fs.unlinkSync(dest));
    }
  }
}

function cmdCheck() {
  const skills = discoverSkills();
  const agents = discoverAgents();
  const missing = [];
  for (const sk of skills) {
    if (!lstatSafe(path.join(HUB, sk.name))) missing.push(`hub:${sk.name}`);
  }
  for (const ag of agents) {
    if (!lstatSafe(path.join(CLAUDE_AGENTS_DIR, ag.name))) missing.push(`agent:${ag.name}`);
  }
  if (missing.length) {
    log(`Missing links (${missing.length}): ${missing.join(", ")}`);
    process.exit(1);
  }
  log(`OK — ${skills.length} skills and ${agents.length} subagents linked.`);
}

function cmdList() {
  log("Skills:");
  for (const sk of discoverSkills()) log(`  - ${sk.name}`);
  log("Subagents:");
  for (const ag of discoverAgents()) log(`  - ${ag.name.replace(/\.md$/, "")}`);
}

function cmdSyncGtmBrain() {
  const targetBrain = positional[0];
  if (!targetBrain) {
    console.error("Usage: node scripts/install-skills.mjs sync-gtm-brain <path-to-gtm-brain> [--dry-run]");
    process.exit(2);
  }
  const brainRoot = path.resolve(targetBrain);
  const mktRoot = path.join(brainRoot, "marketing");
  if (!fs.existsSync(path.join(brainRoot, "gtm-knowledge")) || !fs.existsSync(mktRoot)) {
    console.error(`Error: ${brainRoot} does not look like a gtm-brain checkout.`);
    process.exit(2);
  }
  const destSkills = path.join(mktRoot, "skills");
  const destAgents = path.join(mktRoot, "agents");
  for (const sk of discoverSkills()) {
    const dest = path.join(destSkills, sk.name);
    act(`copy skill ${sk.name} -> ${dest}`, () => fs.cpSync(sk.dir, dest, { recursive: true }));
  }
  for (const ag of discoverAgents()) {
    const dest = path.join(destAgents, ag.name);
    act(`copy agent ${ag.name} -> ${dest}`, () => fs.copyFileSync(ag.file, dest));
  }
  log("Synced into gtm-brain/marketing/. Run `node core-brain/scripts/brain-skills.mjs install` inside gtm-brain to activate for Renata and Berwyn.");
}

switch (command) {
  case "install": cmdInstall(); break;
  case "uninstall": cmdUninstall(); break;
  case "check": cmdCheck(); break;
  case "list": cmdList(); break;
  case "sync-gtm-brain": cmdSyncGtmBrain(); break;
  default:
    log("Usage: node scripts/install-skills.mjs <install|uninstall|check|list|sync-gtm-brain> [--dry-run]");
}
