# Metro Exodus: the console opens through a memory patch, settings live in `user.cfg`, and 4A's own editor is public

**Status:** 🆕 new · **Priority:** high — answers hand-off questions 2 and 4, and the dossier's
"how the console opens" gap.

## 1. Developer console

- **No shipped way to open it is known.** The public route is a Cheat Engine table by **SunBeam** and
  **AltSierra117** (Steam guide 1682349291): enabling its script patches the running game, then **F1**
  toggles the console and ESC or backtick closes it `[reported]`.
- It is reported to work on the **Enhanced Edition** too, where the table needs a flamethrower-related
  section removed for stability; its **noclip** part is reported to crash on Enhanced Edition 2.x
  while the console still works `[reported]`.
- Variables named in the guide include **`r_base_fov`**, `r_gamma`, `r_exposure_control`,
  `r_bloom_prefiltered`, `g_god`, `g_notarget` `[reported]`. Our static pass found `r_base_fov_option`
  `[inferred-static 2026-09-13]`; `r_base_fov` itself is now a public name worth looking for.
- Why it matters: it proves the engine's console survives in the retail exe behind a flag or code
  path. Finding that switch statically is our own work (no copying their table), and the table's
  existence says it is findable `[hypothesis]`.

## 2. `user.cfg`

Players edit hidden settings in **`user.cfg` under `C:\Users\<name>\Saved Games\Metro Exodus\`**; the
game does not save console changes back to it, so values must be typed into the file `[reported]`.
That is a no-code route for any setting we identify (FOV, windowing, effects) and a candidate for the
first-launch windowing job.

## 3. Exodus SDK (4A Games, 2023-01-24)

4A released "the full Editor as it was the day we released Metro Exodus", able to run standalone
content from a basic executable: scene editor, model viewer, AI navigation, particles, terrain,
weather, **camera tools for cutscenes**, a visual script editor, public documentation, tutorial
levels and one full shipped level `[reported]`. It needs Metro Exodus or the Enhanced Edition
installed, comes from the same store, and its EULA forbids commercial use `[reported]`.

⚠️ For this project it is **documentation and a reference for engine concepts** (camera objects,
script-side camera control), not a route into the shipping renderer. We study its public docs and
do not redistribute anything from it. Whether its documentation describes the camera or projection
in a VR-useful way is **unchecked**.

## Next steps

- `[PD]`: read the Exodus SDK's public documentation for camera and console topics.
- `[PD]`: look in the exe for what decides whether the console key is handled (the switch the
  Cheat Engine table flips), using our own analysis.
- `[FLAT]`: check whether `user.cfg` exists after first launch, and which `r_*` keys it carries.

## Sources

- https://steamcommunity.com/sharedfiles/filedetails/?id=1682349291
- https://steamcommunity.com/app/1449560/discussions/0/3148556875502462665/
- https://www.4a-games.com.mt/4a-dna/studio-update-exodus-sdk
- https://www.thesixthaxis.com/2023/01/25/4a-games-releases-full-metro-exodus-sdk-modding-tools-update-on-game-development-during-a-war/
- https://www.deepsilver.com/games/metro-exodus/exodus-sdk
