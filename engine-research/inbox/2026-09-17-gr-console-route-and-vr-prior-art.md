# From /gr: how the console is opened in public, and what is (not) known about the VR code

**From:** `/gr` estate sweep, 2026-09-17. Full write-ups in `external-research/topics/`.

1. **Dossier §4, "how the console opens — unchecked":** there is no known shipped switch. A public
   Cheat Engine table (SunBeam and AltSierra117) patches the running game, then **F1** toggles the
   console; reported working on the Enhanced Edition, with its noclip crashing on 2.x `[reported]`.
   Suggested dossier note: "the console is present in retail and reachable by a memory patch
   `[reported]`; the switch itself is not yet located by us." Public variable names include
   `r_base_fov`, `r_gamma`, `r_exposure_control`, `g_god` `[reported]`.
   → `external-research/topics/2026-09-17-console-user-cfg-and-exodus-sdk.md`
2. **Settings file:** `C:\Users\<name>\Saved Games\Metro Exodus\user.cfg` holds hidden settings, and
   console changes are not written back to it `[reported]`. Relevant to the first-launch windowing job.
3. **Leftover VR code (the board's `[PD]` row):** Arktika.1 ran on the 4A Engine with Rift and Touch
   support `[reported]`, but no public source mentions the `vr_*` names in Metro Exodus. Nothing public
   stands in front of that row; it stays static work.
4. **Prior art:** vorpX gets only depth-based 3D in Direct3D 12; geometry 3D needs the standard
   edition in Direct3D 11, which this Enhanced Edition install does not have `[reported]`.
   → `external-research/topics/2026-09-17-arktika-vr-history-and-vorpx-on-the-enhanced-edition.md`
