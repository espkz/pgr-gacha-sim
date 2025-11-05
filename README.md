# Punishing: Gray Raven Gacha Simulator
I mostly made this because I saw the Uma Musume one and got jealous lol

## Current Features
- Organizable by patches
  - GLB Through the Tide Home integrated - Bianca: Crepuscule, Discord: Secator, and Veronica: Aegis
  - Ideal Cage - Veronica: Aegis
  - KR/JP Ideal Cage integrated - Discord: Secator and Veronica: Aegis
  - Where Nightmares Dwell - Liv: Limpidity
    - DOESN'T ACCOUNT FOR NEW PHYLO TREE BANNER AND PERIOD (I'm currently unsure how it will work so I will leave it as is for now)
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
  - [Frame images](https://assets.huaxu.app/browse/cn/image/role/?layout=grid)
  - Icons
    - [Shards, currency](https://assets.huaxu.app/browse/glb/assets/product/texture/image/icontools/?layout=grid#)
    - [Character](https://assets.huaxu.app/browse/glb/assets/product/texture/image/role/?layout=grid#)
    - [CUBs](https://assets.huaxu.app/browse/glb/assets/product/texture/image/rolepartner/?layout=grid)
- [Gray Ravens](https://grayravens.com/wiki/GRAY_RAVENS)

## Current Issues
- Windows doesn't show the star for 5-star/4-star/3-star weapon in test which... why....
- Pulling too fast will make it bug out (duh don't do that)
- Gets a little slow because I think that's Streamlit latency (will look for a different place to host)
- The A-rank check resets in Member Target if you swap patches (probably doesn't really matter but still)
- Future banners in IP don't give previous unit's shards (CUB and unit)
  - ~~But also I'm not sure how to do it so it might have to wait until sync~~
- Target weapon and arrival banner
  - Calibration exists but it's not visually there (because once it shows up it won't go away like what)
  - No uniqueness for five star and below weapons (~~but uh, do people really want to see what kind of five star they got?~~)
- Liv's banner will be **separate** — weapon and CUB too
  - Phylo Tree banner operates the same as Themed, 100% rate up but unsure when it returns
  - Weapon and CUB targetable if the unit debuts/reruns

## TODO

- [ ] Move it to a more scalable platform
- [ ] Patch cleanup for post-integrated patches (also a general code cleanup to be honest)
