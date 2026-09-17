# 4A's VR history, and what vorpX reaches on the Enhanced Edition

**Status:** 🆕 new · **Priority:** medium — answers hand-off questions 1, 3 and 5 as far as public
sources go.

## Arktika.1 and the leftover VR code

- **Arktika.1** (4A Games, Oculus Studios, October 2017, Oculus Rift with Touch) ran on the fourth
  iteration of the 4A Engine, which added Rift and Touch support `[reported]`. That fits the dossier's
  guess that the `vr_*` / `oculus_touch_presets` names in Metro Exodus are inherited from it
  `[hypothesis]`.
- **No public write-up was found** of how Arktika.1 rendered stereo, and **no one in public appears
  to have noticed or used the leftover VR names** in the Metro Exodus exe. Both come from automated
  search only, so neither is a negative `[hypothesis]`. If the code is live, this project would be
  first to document it.

## Existing Metro Exodus VR attempts

- **vorpX:** in Direct3D 12 it offers **depth-based 3D (Z3D) only, not geometry 3D (G3D)**; forum
  users get G3D by running the **standard edition in Direct3D 11**, and the Enhanced Edition has no
  G3D (a user reports full VR there through an unofficial profile) `[reported]`.
  ⚠️ For us: the Enhanced Edition is Direct3D 12 only (dossier §2), so the Direct3D 11 escape hatch
  is not available on this install.
- **Luke Ross R.E.A.L. VR:** one forum post lists Metro Exodus Enhanced among supported games, but his
  June 2026 list and Road to VR's March 2026 coverage do not mention it `[reported]`, so it is
  **unconfirmed**. Closed and paid: study public statements only.
- No open-source head-tracking or stereo mod for Metro Exodus turned up `[hypothesis]`.

## Metro Awakening

Not checked this pass. The hand-off's one-line question (does it offer anything for this engine)
stays open.

## Next step

The leftover VR code is the unique lead here and no public source covers it, so it stays our own
static work (board `[PD]` row). Public research has nothing further to add until that pass says
whether the code is live.

## Sources

- https://en.wikipedia.org/wiki/Arktika.1
- https://www.moddb.com/engines/4a-engine
- https://www.vorpx.com/forums/topic/metro-exodus-enhanced-edition-and-dx12/
- https://www.vorpx.com/forums/topic/metro-exodus-enhanced/
- https://mixed-news.com/en/real-vr-mod-dlss-ray-reconstruction/
- https://roadtovr.com/luke-ross-vr-mods-free-cyberpunk-2077/
