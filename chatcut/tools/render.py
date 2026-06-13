"""Capability: ``render`` — final encode.

Auto-detects a working encoder (NVENC/QSV/VideoToolbox/libx264), scales to the
configured height, and applies loudness normalisation as the LAST audio step.
Never stream-copies. This is the step that makes the output safe to publish.
"""

from __future__ import annotations

from ..core.tool import Tool, ToolManifest, ToolResult
from ..core.context import RunContext
from .. import media


class RenderTool(Tool):
    manifest = ToolManifest(
        name="render_ffmpeg",
        capability="render",
        summary="Final encode with auto-detected encoder + loudnorm (cross-platform).",
        backends=("ffmpeg",),
        requires_bin=("ffmpeg",),
    )

    def run(self, ctx: RunContext, *, input: str, name: str = "final.mp4", preview: bool = False) -> ToolResult:
        media.require("ffmpeg")
        enc_cfg = ctx.config.encode
        encoder = "libx264" if preview else media.detect_encoder(enc_cfg.encoder)
        height = 720 if preview else enc_cfg.final_height
        out_dir = ctx.paths.previews if preview else ctx.paths.renders
        out = out_dir / name

        vf = f"scale=-2:{height}:flags=lanczos"
        af = f"loudnorm=I={enc_cfg.loudness_lufs}:TP=-1.5:LRA=11"
        cmd = [
            "ffmpeg", "-y", "-i", input,
            "-vf", vf,
            "-c:v", encoder, *media.encoder_quality_args(encoder),
            "-af", af,
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(out),
        ]
        media.run(cmd, log=ctx.log, desc=f"render → {encoder} {height}p{' (preview)' if preview else ''}")

        level = media.mean_volume_db(out)
        if level is not None and level < -60:
            # Correctness guard: a finished file should not be effectively silent.
            ctx.log(f"⚠ output mean volume {level} dBFS looks silent — check audio mapping")
        return ToolResult(artifacts={"video": str(out)}, meta={"encoder": encoder, "mean_volume_db": level})


TOOL = RenderTool()
