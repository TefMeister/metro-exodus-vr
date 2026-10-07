# Research index

**Last `/gr` pass: 2026-10-07 (estate sweep) — CHECK-IN.** Inbox empty. For the keyed-mutex wall: REFramework binds OpenXR to the game's own D3D11 device and needs no shared texture (option d), plus a one-line check for an 11on12 device; topic filed, pointer sent, and the idea handed to Bulletstorm.

_Previous: **Last `/gr` pass: 2026-10-04 (estate sweep, second pass) — CHECK-IN.** Inbox empty; board `OPEN` rows read: one search for `-build_key` found no public mention. Nothing new._

_Previous: **Last `/gr` pass: 2026-09-29 (estate sweep) — CHECK-IN.** Inbox empty; one search for the `-vr_profile` / `vr_*` names found no public mention (vorpX threads only). Nothing new._

_Previous: **Last `/gr` pass: 2026-09-23 (estate sweep) — CHECK-IN.** Checked phunkaeg's *VR Modding Playbook*: no entry for the 4A Engine. Nothing new.

_Previous: **Last `/gr` pass: 2026-09-17 (estate sweep) — FULL.** First pass on this project: folder bootstrapped, the modding lane's project-start hand-off drained, two topics written (console, `user.cfg` and the Exodus SDK; Arktika.1 history and vorpX on the Enhanced Edition), and a pointer sent to `engine-research/inbox/`. Metro Awakening was not checked._

Every research topic gathered for this project, newest first. Each row links to a self-contained
write-up in `topics/`. Status tags:

- 🆕 **new** — found, not yet acted on by the modding side.
- 👀 **looked at** — the modding side has read it; no verdict yet.
- ✅ **used / confirmed** — acted on, and it held.
- ❌ **dead end** — tried, and it did not work (kept so it is not re-proposed).

| Date | Topic | Status | Why it matters |
| --- | --- | --- | --- |
| 2026-10-07 | [Skip the shared texture: give the headset runtime the game's own D3D11 device](topics/2026-10-07-skip-the-shared-texture-bind-the-headset-to-the-game-device.md) | 🆕 | A fourth option for the keyed-mutex wall, used by REFramework, plus a one-line 11on12 check |
| 2026-09-17 | [The console opens through a memory patch, settings live in `user.cfg`, and 4A's own editor is public](topics/2026-09-17-console-user-cfg-and-exodus-sdk.md) | 🆕 | Answers "how the console opens" (F1, after a public memory patch), names `r_base_fov`, and points at the official SDK docs |
| 2026-09-17 | [4A's VR history, and what vorpX reaches on the Enhanced Edition](topics/2026-09-17-arktika-vr-history-and-vorpx-on-the-enhanced-edition.md) | 🆕 | Nobody in public has used the leftover VR code; Direct3D 12 limits vorpX to depth-based 3D |
