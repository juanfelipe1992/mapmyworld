from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from random import sample
from router.router import router

app = FastAPI()

app.include_router(router)

'''
# Creating the project without a mysql database --> "Only create data as a list [locations,categories,location_category_reviewed]"
db:List[Locations] = [
    Locations(
        id="88cb8b53-b4b8-4f56-9ab0-ca22837fe739",
        longitude=10.0010,
        latitude=11.0011
    ),
    Locations(
        id="88cb8b53-b4b8-4f56-9ab0-ca22837fe740",
        longitude=12.0012,
        latitude=13.0013
    )
]
db2:List[Categories] = [
    Categories(
        id="99cb8b53-b4b8-4f56-9ab0-ca22837fe980",
        name="Beach Zone"
    ),
    Categories(
        id="99cb8b53-b4b8-4f56-9ab0-ca22837fe981",
        name="Natural Park"
    )
]

db3:List[location_category_reviewed] = [
    location_category_reviewed(
        id= UUID("88cb8b53-b4b8-4f56-9ab0-ca22837fe738"),
        location_id= "88cb8b53-b4b8-4f56-9ab0-ca22837fe739",
        category_id= "99cb8b53-b4b8-4f56-9ab0-ca22837fe980",
        last_review_date = None,
        is_reviewed = False
    ),
    location_category_reviewed(
        id= UUID("996f5df5-4e59-4dfa-94c5-5a0391b8d642"),
        location_id= "88cb8b53-b4b8-4f56-9ab0-ca22837fe740",
        category_id= "99cb8b53-b4b8-4f56-9ab0-ca22837fe981",
        last_review_date = None,
        is_reviewed = False
    )
]
# Mock databases
locations = [{'id': i, 'longitude': i * 10.0, 'latitude': i * 5.0} for i in range(1, 21)]
categories = [{'id': i, 'name': f"Category {i}"} for i in range(1, 11)]
location_category_reviews = []

@app.get("/api/v1/locations")
async def fetch_locations():
    # getting all locations
    return db

@app.post("/api/v1/locations")
async def add_location(location: Locations):
    # location persistence in the db
    db.append(location)
    return {"id": location.id}

@app.get("/api/v1/categories")
async def fetch_categories():
    # gettin all categories
    return db2

@app.post("/api/v1/categories")
async def add_category(category:Categories):
    # category persistence in the db
    db2.append(category)
    return {"id": category.id}

@app.get("/api/v1/recommendations")
async def fetch_recommendations():
    # gettin all recomendations
    return db3

@app.get("/api/v1/recomendations")
async def get_recomendations():
    # Generating all possible combinations if nos in location_category_reviewed
    all_combinations = [(loc['id'],cat['id']) for loc in locations for cat in categories]
    for loc_id, cat_id in all_combinations:
        if not any(r for r in location_category_reviewed if r.location_id == loc_id and r.category_id == cat_id):
            location_category_reviewed.append({'location_id':loc_id, 'category_id':cat_id, 'last_reviewed_date':None})

    # Filter unreviewed combinations in the last 30 days or never reviewed
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    potential_reommendations = [r for r in location_category_reviewed if r['last_reviewed_date'] is None or r['last_reviewed_date'] < cutoff_date]

    # Prioritize never reviewed
    never_reviewed = [r for r in potential_reommendations if r['last_reviewed_date'] is None]
    recently_reviewed = [r for r in potential_reommendations if r['last_reviewed_date'] is not None]

    # Sort reviewed recients by date to give prioritize the least recent ones
    recently_reviewed.sort(key=lambda x: x['last_reviewed_date'])

    # Merge and select the first 10 recommendations
    combined_recommendations = never_reviewed + recently_reviewed
    top_recommendations = combined_recommendations[:10]

    return [location_category_reviewed(**r) for r in top_recommendations]
'''