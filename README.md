- [재료 검색](#재료-검색)
- [칵테일 검색](#칵테일-검색)
- [칵테일 등록](#칵테일-등록)
- [칵테일 상세정보](#칵테일-상세정보)

# 재료 검색

## Request

__URL__

```
GET /api/ingredients
```

__Parameter__

|Name    |Type        |Description                 |Required|
|--------|------------|----------------------------|--------|
|query   |String      |이름으로 검색|X|
|category|String      |[카테고리](#category) 카테고리로 필터링|X|

## Response

__ingredients__

|Name       |Type   |Description|
|-----------|-------|-----------|
|id         |Integer|재료 고유 아이디|
|name       |String |재료 이름|
|description|String |재료 설명|
|abv        |String |재료 도수. 소수점 한 자리 까지 표시|
|category   |String |[카테고리](#category) 재료 카테고리|


# 칵테일 검색

## Request

__URL__

```
GET /api/cocktails
```
__Parameter__

|Name    |Type        |Description                 |Required|
|--------|------------|----------------------------|--------|
|query   |String      |이름으로 검색              |X       |
|base    |String      |베이스로 필터링. 아래 ___base___ 참고|X       |
|min     |Integer     |최소 도수로 필터링       |X       |
|max     |Integer     |최대 도수로 필터링       |X       |


---

## Response
__meta__

|Name        |Type        |Description|
|------------|------------|-----------|
|total_count |Integer     |검색된 칵테일의 수|

__cocktails__

|Name        |Type            |Description|
|------------|----------------|-----------|
|id          |Integer         |칵테일 고유 아이디|
|name        |String          |칵테일 이름|
|garnish     |String          |칵테일 가니쉬 설명|
|methods     |String[]        |[칵테일 기법](#method) 참고|
|description |String          |칵테일 설명|
|ingredients |Recipe[]        |칵테일 재료 리스트. [___RecipeIngredient___](#recipeingredient) 참고|
|tags        |String[]        |칵테일 태그 리스트.|
|abv         |String          |칵테일 도수. 소수점 한 자리 까지 표시|


# 칵테일 등록

## Request

__URL__
```
POST /api/cocktails
```
__Parameter__

|Name            |Type        |Description|Required|
|----------------|------------|-----------|--------|
|name            |String      |칵테일 이름|O|
|base            |String |[칵테일 베이스](#base)|O|
|garnish         |String      |칵테일 가니쉬 설명|X|
|methods         |String[]:   |[칵테일 기법](#methods) 참고.|O|
|description     |String      |칵테일 설명|X|
|ingredients     |RecipeIngredient[]    |칵테일 재료. [___RecipeIngredient___](#recipeingredient) 참고.|O|
|tags            |String[]    |칵테일 태그.|X|

__Content example__
```
{
    "name": "god father",
    "base": "whiskey",
    "garnish": "orange twist",
    "methods": ["build", "stir"],
    "description": "this is awesome cocktail.",
    "ingredients": [
        {
            "ingredient": 1,
            "volume": 50,
            "unit": "ml"
        },
        {
            "ingredient": 2,
            "volume": 25,
            "unit": "ml"
        },
        {
            "ingredient": 3,
            "volume": 1,
            "unit": "slices",
            "optional": "True"
        }
    ],
    "tags": ["classic"]
}
```
    
## Response

---


### ___category___
|Name       |Description|
|-----------|-----------|
|spirits    |증류주|
|wines      |와인|
|liqueurs   |리큐르|
|juices     |주스|
|beverages  |음료|
|fruits     |과일|
|syrups     |시럽|
|bitters    |비터스|
|pantries   |기타 식재료|

### ___base___

|Name        |Description|
|------------|-----------|
|whiskey     |위스키|
|rum         |럼|
|gin         |진|
|vodka       |보드카|
|tequila     |데킬라|
|brandy      |브랜디|
|liqueur     |리큐르|
|wine        |와인|
|mixed       |혼합|

### ___methods___

|Name        |Description|
|------------|-----------|
|build       |빌드|
|stir        |스터|
|shake       |쉐이킹|
|float       |플로팅|
|blend       |블렌딩|

### ___RecipeIngredient___

|Name        |Type            |Description|Required|
|------------|----------------|-----------|--------|
|ingredient  |Integer         |재료 고유 아이디|O|
|name        |String          |재료 이름|X|
|volume      |Integer         |재료 용량|O|
|unit        |String          |재료 용량 단위|O|
|optional    |Boolean         |선택적 재료 여부|X|
