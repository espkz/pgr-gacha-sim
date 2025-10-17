# Punishing: Gray Raven Gacha Simulator
I mostly made this because I saw the Uma Musume one and got jealous lol

## Current Features
- Organizable by patches
  - GLB Through the Tide Home integrated - Bianca: Crepuscule, Discord: Secator, and Veronica: Aegis
  - Ideal Cage - Veronica: Aegis
  - KR/JP Ideal Cage integrated - Discord: Secator and Veronica: Aegis
  - Where Nightmares Dwell - Liv: Limpidity
    - Weapon/CUB names and assets are from translated equipment
- Themed Banner and Fate Themed Banner
- Base Member Target with possible S-rank check
- Target Weapon (with calibration)
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
- Pulling too fast will make it bug out (duh don't do that)
- Gets a little slow because I think that's Streamlit latency (will look for a different place to host)
- The A-rank check resets in Member Target if you swap patches (probably doesn't really matter but still)
- Future banners in IP don't give previous unit's shards (CUB and unit)
  - ~~But also I'm not sure how to do it so it might have to wait until sync~~
- Target banner
  - Calibration exists but it's not visually there (because once it shows up it won't go away like what)
  - No uniqueness for five star and below weapons (~~but uh, do people really want to see what kind of five star they got?~~)

## TODO
- Base weapon banner
  - Similar to base unit banner where it goes up to Geiravor (2 patches behind)
  - Uh... it also has Sirius (???)
  - Otherwise percentages are the same as target weapon

- Arrival banner
  - 70% target and other two target selectors (just to make it easier)
  - It probably starts from Scire because Daren is (somehow) not dead yet (maybe just add all S-ranks for the sake of me not figuring that out)
  - Make sure targeted is not selectable from the other 15%s
