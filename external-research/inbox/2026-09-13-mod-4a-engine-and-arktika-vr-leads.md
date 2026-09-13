# Hand-off to `/gr`: 4A Engine research and its VR history

**From:** modding session, home PC, 2026-09-13 (project start, no launch).

Tefa's framing when starting this project: drawn to proprietary engines and to reverse-engineering
them. Nothing here has been searched yet; these are the questions worth the first `/gr` pass.

1. **Arktika.1 (4A Games, 2017, Oculus)** was a VR game on the 4A Engine `[reported]`. The Metro
   Exodus exe still carries VR code names (`-vr_profile`, `vr_hand_speed`, `oculus_touch_presets`,
   "Negate VR HMD Offset") `[inferred-static 2026-09-13]`. Has anyone in public noticed or used these?
   Is anything documented about how Arktika.1 rendered stereo on this engine?
2. **Metro Exodus console and config variables.** The exe has about 350 `r_*`/`g_*`-style names. Is
   there a known way to open a developer console or set them (a `user.cfg`, a launch flag)?
3. **Existing Metro Exodus VR attempts:** VorpX profiles, depth-3D injectors, any head-tracking or
   stereo mod, and how far they got on the Enhanced Edition (Direct3D 12, ray tracing always on).
4. **Public 4A Engine reverse-engineering:** `.vfs`/`.vfx` archive tools, the Metro Exodus modding SDK
   that 4A released `[reported]`, and any write-ups of its renderer.
5. **Metro Awakening** (2024) is a VR Metro game, but by Vertigo Games on a different engine `[reported]`.
   Worth one line confirming it offers nothing for this engine, so it is not re-proposed.
