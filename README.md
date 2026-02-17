# Punishing: Gray Raven Gacha Simulator
I mostly made this because I saw the Uma Musume one and got jealous lol

## Current Features
- Organizable by patches
  - Withering Crown - Rosetta: Arete

### Banners
- Themed Banner and Fate Themed Banner
- Arrival Banner and Fate Arrival Banner
  - Selectable units from units after Karenina: Scire (~~I forgot what units are left for the dead and not part of it~~)
- Base Member Target with possible S-rank check
- Target Weapon banner (with calibration)
- Base Weapon banner
- Uniframe banner
- CUB banner

## Sources
- Huaxu
  - [Shards, currency, weapons](https://assets.huaxu.app/browse/glb/assets/product/texture/image/icontools/?layout=grid#)
  - [Character](https://assets.huaxu.app/browse/glb/assets/product/texture/image/role/?layout=grid#)
  - [CUBs](https://assets.huaxu.app/browse/glb/assets/product/texture/image/rolepartner/?layout=grid)
- [Gray Ravens](https://grayravens.com/wiki/GRAY_RAVENS)

## Current Issues
- Doesn't account for the Phylotree banner and Limpidity (yet, I still have no idea how to work it)
- Windows doesn't show the star for 5-star/4-star/3-star weapon in test which... why....
- Pulling too fast will make it bug out (duh don't do that)
- Gets a little slow because I think that's Streamlit latency (will look for a different place to host)
- The A-rank check resets in Member Target if you swap patches (probably doesn't really matter but still)
- Target weapon and arrival banner
  - Calibration exists but it's not visually there (because once the message shows up it won't go away like what)
  - No uniqueness for five star and below weapons (~~but uh, do people really want to see what kind of five star they got?~~)
- Liv's banner will be **separate** — weapon and CUB too
  - Phylotree banner operates the same as Themed, 100% rate up but unsure when it returns
  - Weapon and CUB targetable if the unit debuts/reruns
- Unsure how the CUB shards and base banner works — for now the debut CUB banner has debut CUB shards and characters have shards in the base banner if they are put into it

## TODO

- [ ] Move it to a more scalable platform
- [ ] Patch cleanup for post-integrated patches (also a general code cleanup to be honest)

## Log
2026.01.19 Update for upcoming Withering Crown (Arete)
2026.02.04 Withering Crown patch
2026.02.10 Fixes for shard accountability, Phylotree variable setup