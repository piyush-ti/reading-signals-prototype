"""Bundle actual analyzed outputs for a serverless, credential-free demo."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def clip(name, **metadata):
    analysis = json.loads((ROOT / "results" / f"{name}.json").read_text())
    source = ROOT / "assets" / f"{name}.mp4"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == analysis["input_sha256"]
    assert len({p["id"] for p in analysis["people"]}) == len(analysis["people"])
    for p in analysis["people"]:
        assert p["segments"][0]["start"] == 0
        assert abs(p["segments"][-1]["end"] - analysis["duration"]) < .06
        assert all(0 <= e["time"] <= analysis["duration"] for e in p["page_turns"])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-i", str(source),
                    "-frames:v", "1", str(ROOT / "assets" / f"{name}.jpg")], check=True)
    return dict(src=f"assets/{name}.mp4", poster=f"assets/{name}.jpg",
                resultUrl=f"results/{name}.json", analysis=analysis, **metadata)


clips = [clip("overhead", title="Overhead reading observation",
    subtitle="Licensed footage · 8.8 seconds · 5 readers",
    shortLabel="Licensed footage · overhead view", generated=False, orderByX=True,
    descriptions={"reader_a": "Burgundy sweater · lower table", "reader_b": "Cream top · upper right", "reader_c": "White shirt · upper left", "reader_d": "Striped shirt · left", "reader_e": "Mustard sweater · right"},
    note="Five readers in the supplied overhead clip. Source resolution: 768 × 432; this is not a 4K classroom accuracy test.",
    credit="Getty Images asset 2194897651. Supplied for this demonstration under the owner’s confirmed license. Watermark retained.")]
if (ROOT / "results/generated-long.json").exists():
    clips.append(clip("generated-long", title="Ceiling-camera classroom",
        subtitle="Generated footage · 15 seconds · 3 readers",
        shortLabel="Generated · ceiling-corner view", generated=True,
        descriptions={"reader_a": "Blue shirt", "reader_b": "Orange shirt", "reader_c": "Red top · back desk"},
        note="Synthetic classroom with a fixed ceiling-corner viewpoint. Generated footage demonstrates the interaction; it does not validate accuracy on real children or cameras.",
        credit="Synthetic video generated with Google Veo 3.1 Fast. Requested camera mounting height: 2.7 m; physical height cannot be measured from generated pixels.",
        sourceUrl="https://ai.google.dev/gemini-api/docs/veo"))
if (ROOT / "results/generated-group.json").exists():
    clips.append(clip("generated-group", title="Five-reader overhead table",
        subtitle="Generated overhead footage · 15 seconds · 5 readers",
        menuLabel="Generated overhead", generated=True, orderByX=True,
        descriptions={"reader_a": "Blue top", "reader_b": "Orange top", "reader_c": "Green top", "reader_d": "Burgundy top", "reader_e": "Cream top"},
        note="Synthetic five-student scene. Generated footage is not an accuracy benchmark.",
        credit="Synthetic video generated with Google Veo 3.1 Fast; continuous generated extension.",
        sourceUrl="https://ai.google.dev/gemini-api/docs/veo"))
clips.sort(key=lambda c: not c["generated"])
(ROOT / "demo-data.js").write_text("window.READING_DEMO = " + json.dumps({"clips": clips}, ensure_ascii=False, separators=(",", ":")) + ";\n")
print("Packaged", len(clips), "clips with verified video hashes")
