# Reading Lab

Standalone Marauder’s Map physical-book reading prototype. Play a clip to see
person and book bounding boxes, estimated reading durations and candidate page
turns. On desktop, the player sits on the left and compact reader cards sit on the right.
On narrow screens, cards stack below the player. The default
15-second generated overhead clip includes all six visible students, followed by
the 15-second generated CCTV clip with all three visible people, then the supplied
Getty clip with five. Overhead display labels run left to right at the first
frame and remain stable during playback. Model IDs in the saved JSON stay intact.

## Run

Open `index.html`, or serve this directory with `python3 -m http.server 8766`.
The published site is static: no credentials, backend, or inference calls run
in the viewer's browser.

## Evidence

This replays **saved Gemini model outputs with documented visual-review
corrections**, rather than running live inference during playback. The original
video-model responses remain in `results/*.video.raw.json`. Any reviewed
classification changes are recorded under `review_corrections` in the clip result. Video activity is sampled at 4 FPS. Boxes are
independently localized at approximately 1 FPS and linearly interpolated. The
exact analyzed source video is tied to each result by SHA-256.

- `results/*.json`: observations, intervals, page-turn candidates, boxes, model,
  prompts, sampling rates and source hashes.
- `tools/analyze_detail.py`: analysis and localization runner.
- `tools/package_demo.py`: verifies source hashes and generates `demo-data.js`.

Reading time sums only `likely_reading` intervals up to the current playhead.
Pausing stops accumulation; seeking recomputes from intervals and does not
double-count replay. `unclear` and `other_activity` time is excluded. Page-turn
counts are model-estimated gestures, not pages read. Confidence labels are
model judgments, not calibrated probabilities.

## Limits

This is a feasibility prototype, not an accuracy benchmark. Short stock clips
and generated scenes do not establish performance in a real classroom. Looking
at a book cannot establish comprehension or attention. Associations can be
ambiguous, especially when two people share a book or a book is obscured.
Localization can drift, and page-turn events may be missed or confused with
other hand movements. No results should be used for grading or evaluation.

## Media

The supplied Getty Images asset 2194897651 is included for the commissioned demo
under the requester's confirmed license. Its existing watermark remains in the
preview source. No redistribution rights are granted to visitors; it is not
covered by an open-source code license.

The generated classroom clip is clearly identified in its video selector.
It is a continuous 15-second Veo 3.1 Fast generation with extension, not a loop
or slowed clip. Requested camera height is a prompt parameter, not a measurable
camera calibration. Generation provenance is in `results/generation.json` and
`results/generation-group.json`. The second scene has six students around a shared
table. All generated clips are labeled in their selectors.

## Reproduce

Install Python packages `google-genai` and `python-dotenv`, and install FFmpeg.
Set `GEMINI_API_KEY` locally or pass a local environment file with `--env-file`.
Never commit that file. Supply explicit clothing/position identifiers through
`--targets` and set `--readers` to the number of readers. Analysis sends the
chosen media to the Gemini API; only authorized demo media should be used.

`--reuse-video` is intended only for retrying localization with the exact same
source and targets after a successful video-analysis request.

## Design

The MVP uses the existing Marauder’s Map frontend palette: primary blue
`#2563eb`, app background `#e9eef0`, white cards, text `#18202a`, and Inter.
The font is self-hosted with its SIL Open Font License.
