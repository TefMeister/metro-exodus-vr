# Two other people's Metro Exodus VR mods: RippeR37's public beta and farmerarmor's experiment

Found by `/gr` on 2026-11-14 (check-in pass, part of a full scan on the Developer PC). The pass of 2026-11-07 found
no Metro Exodus VR mod by anyone else; that is no longer true.

## What exists

**1. RippeR37, MetroExodusVR** — <https://github.com/RippeR37/MetroExodusVR>

- Repo created 2026-11-04; first public beta **v0.9.0 on 2026-11-06**, bug-fix **v0.9.1 on 2026-11-09**; 111 stars
  on 2026-11-14; no licence file `[measured 2026-11-14, GitHub API]`.
- By the maker of q3vr (a PC VR port of Quake 3 Arena) `[reported 2026-11-14, vr.org]`.
- What it does, as reported: the whole main campaign in a PC VR headset with full 6DoF head and hands; motion
  controls for aiming, reloading and weapons with custom animations; hands for the gas mask, filters and medkits;
  standing, seated and room-scale; left-handed play; DLSS, FSR2 and foveated rendering; experimental bHaptics.
  The two expansions (The Two Colonels, Sam's Story) are planned for later `[reported 2026-11-14, vr.org]`.
- **Edition: the Steam STANDARD edition only, updated to build 1.0.0.7.** Epic and GOG are "work in progress";
  Enhanced Edition support "has not been decided yet" according to its README, as quoted by the article
  `[reported 2026-11-14, vr.org; README not read by us]`.
- The stereo method is not stated in the article `[reported]`.

**2. farmerarmor, MetroExodusVR** — <https://github.com/farmerarmor/MetroExodusVR>

- Described on GitHub as an "Experimental native D3D11/OpenXR VR mod for Metro Exodus with paired stereo
  rendering". One pre-release, v0.82.0, 2026-09-08; no push since; 7 stars `[measured 2026-11-14, GitHub API]`.
- farmerarmor is also the maker of TombRaiderVR, which our Tomb Raider project keeps as a reference.

## Why it matters for this project

- Our project targets the **Enhanced Edition** (4A Engine, Direct3D 12) and has been paused since 2026-11-04 by
  Tefa's choice. RippeR37's mod is for the **Standard** edition (the 2019 game, appid 412020, which our notes show
  is installed on the Developer PC and reaches its main menu).
- Under Tefa's rule of 2026-09-23 (do not build a VR mod someone else is already building; watch it), this is a
  watch-list case: a playable, actively developed VR mod for the same game. Whether "different edition" changes
  that is Tefa's call, not this lane's.
- If the project is ever resumed, the allowed shape is building ON it (as with Visceral on REFramework), and its
  hands, reload and gas-mask work is exactly the part we had not started.

## The next step it unlocks

- The modding lane: add a row to `claude-memory/WATCHING.md` and the `⏸️ PAUSED` line naming the mod (pointer
  dropped in `engine-research/inbox/`).
- A later `/gr` pass: read RippeR37's README and release notes first-hand (stereo method, which renderer it hooks,
  whether Enhanced Edition support was decided), and re-check both repos.

## Sources

- vr.org, "Metro Exodus VR mod" article, 2026-11-09: <https://vr.org/articles/metro-exodus-vr-mod-ripper37-free-pc-vr-beta-how-to-play-2026>
- GitHub: <https://github.com/RippeR37/MetroExodusVR>, <https://github.com/farmerarmor/MetroExodusVR>
