# chatcut

> One command turns raw talking-head footage into a finished video — driven by your coding agent (Claude Code / Codex), not a timeline.

**chatcut** is an extensible, agent-orchestrated video-editing studio focused on **talking-head** content (vlogs, tutorials, explainers). You drop in raw footage, say what you want in plain language, and the agent runs a battle-tested pipeline: transcribe → cut pauses & stumbles → subtitles → motion graphics → color → render.

It does **not** reinvent the engines. It orchestrates the best open tools — [video-use](https://github.com/browser-use/video-use), [hyperframes](https://github.com/heygen-com/hyperframes), [auto-editor](https://github.com/WyattBlue/auto-editor), [faster-whisper](https://github.com/SYSTRAN/faster-whisper), ffmpeg — and adds the part that's actually hard: **opinionated, hard-won correctness rules** so a single command doesn't produce a broken video (no frozen frames, no A/V desync, no crushed audio).

> 🚧 **Status: v0.1, building in the open.** The core pipeline works end-to-end
> (raw → finished video in one command); polishing setup and real-world testing.

## Quick start

```bash
git clone https://github.com/ArtCog/chatcut && cd chatcut
./setup.sh            # Windows: ./setup.ps1   (installs chatcut + free local toolchain)
chatcut tools         # see capabilities and what's ready
chatcut edit raw.mp4  # raw footage → projects/raw/renders/final.mp4
```

Then just talk to your agent: *"edit raw.mp4 — cut the filler, add captions,
warm look."* It runs the pipeline, shows you a cut-plan, renders a preview, and
finalises.

## Why chatcut

- **One command, not copy-paste.** A real CLI + agent orchestration, instead of pasting prompts into an IDE.
- **Talking-head depth.** Cut by meaning, kill filler, fix stumbles, sync captions to words.
- **Free by default.** Local `faster-whisper` out of the box — no paid API key required. Premium engines (ElevenLabs Scribe) are an opt-in upgrade.
- **Cross-platform encode.** NVENC when available, graceful fallback to libx264 / VideoToolbox / QSV.
- **Built to grow.** A plugin/tool registry — new tools and pipelines drop in without touching the core.

## How it works (talking-head pipeline)

```
raw footage
  → normalize (clean CFR)            don't desync on variable-framerate input
  → transcribe (word-level)          faster-whisper (local) / ElevenLabs (opt-in)
  → detect stumbles & pauses
  → cut-plan (you approve)           never auto-cuts blindly
  → cut (EDL, padded by cut type)
  → subtitles
  → motion graphics (optional)       hyperframes
  → color (LUT)
  → render                           correctness-checked output
```

## Status & roadmap

v0.1 ships a working talking-head pipeline behind one command. Growth (shorts, podcast, B-roll, diarization, denoise, background replacement) lands as plugins.

## Credits & license

Built on the shoulders of open-source tools — see [CREDITS.md](CREDITS.md). Architecture ideas (tool registry, checkpoints) inspired by [OpenMontage](https://github.com/calesthio/OpenMontage); no code copied.

MIT © 2026 [ArtCog](https://github.com/ArtCog). The bundled engines keep their own licenses.

🇷🇺 [Русская версия — README.ru.md](README.ru.md)
