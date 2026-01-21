# PGR Gacha API Documentation

## GET /patches
- Returns all available patches.

Response:
```json
[
  {
    "id" : "spark_to_wildfire",
    "name" : "Spark to Wildfire"
  },
  {
    "id" : "through_the_tide_home",
    "name" : "Through the Tide Home"
  }
]
```

## GET /banners
- Returns all available banners.

Response:
```json
[
  {
    "id": "member_target_banner",
    "name": "Base Member Target"
  },
  {
    "id": "fate_themed_banner",
    "name": "Fate Themed Banner"
  }
]
```


## GET /patch
- Returns information of selected patch.

Response:
```json
{
    "patch_name": "Through the Tide Home",
    "patch_type" : "S",
    "img": "data/img/patch_banners/through_the_tide_home.png",
    "start_date" : "2025/07/03, 05:00 CST",
    "banners": [
      {
        "name": "Themed Banner",
        "unit" : "Bianca: Crepuscule"
      },
      {
        "name": "Fate Themed Banner",
        "unit" : "Bianca: Crepuscule"
      },
      {
        "name": "Target Weapon",
        "weapon": "Aurora",
        "unit": "Crepuscule"
      },
      {
        "name": "CUB Target",
        "unit" : "Noctiluca"
      },
      {
        "name": "Base Member Target",
        "unit" : "Vera: Geiravor",
        "rank" : "S"
      }
    ]
}
```

## GET /banner
- Returns information of selected banner.

Response:
```json
{
    "title": "Themed Banner",
    "pity" : 60,
    "has_five_star_pity" : 1,
    "has_calibration" : 0,
    "rates": [
      {
        "name": "S-Rank Omniframe",
        "rarity": 6,
        "rate": 0.005
      },
      {
        "name": "A, B-Rank Omniframe",
        "rarity": 5,
        "rate": 0.1395
      },
      {
        "name": "Construct Shard",
        "rarity": 4,
        "rate": 0.2211
      },
      {
        "name": "4-star Equipment",
        "rarity": 4,
        "rate": 0.2839
      },
      {
        "name": "Overclock Material",
        "rarity": 4,
        "rate": 0.1442
      },
      {
        "name": "EXP Material",
        "rarity": 4,
        "rate": 0.0481
      },
      {
        "name": "Cog Box",
        "rarity": 4,
        "rate": 0.1442
      }
    ]
}
```


## POST /pull
- Perform a gacha pull.

Request:
{
  "patch_id" : "through_the_tide_home"
  "banner_id": "fate_themed_banner",
  "times": 1
}
Response:
```json
{
  "banner_id": "fate_themed_banner",
  "results": [
      { "name": "Bianca: Crepuscule", "rarity": 6 , "banner" :  ["debut"], "img" : "data/img/unit/s_rank_omniframe/crepuscule.png"}
  ]
}
```