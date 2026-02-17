# PGR Gacha API Documentation

## GET /patches
- Returns all current and future patches.

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


## GET /patches/{patch_id}
- Returns information of selected patch.
- Use time in ISO format for hopefully easier conversion

Response:
```json
{
    "id" : "through_the_tide_home",
    "name": "Through the Tide Home",
    "type" : "S",
    "img": "data/img/patch_banners/through_the_tide_home.png",
    "start_date" : "2025-07-03T05:00:00Z",
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

## GET /banners/{banner_id}
- Returns information of selected banner.

Response:
```json
{
    "id" : "themed_banner",
    "name": "Themed Banner",
    "pity" : 60,
    "has_five_star_pity" : true,
    "has_calibration" : false,
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
- Perform n number of gacha pulls.

Request:
```json
{
  "patch_id" : "through_the_tide_home",
  "banner_id" : "fate_themed_banner",
  "times": 1
}
```
Response:
```json
{
  "banner": "fate_themed_banner",
  "results": [
      { "name": "Bianca: Crepuscule", "rarity": 6 , "banner" :  ["debut"], "img" : "data/img/unit/s_rank_omniframe/crepuscule.png"}
  ]
}
```