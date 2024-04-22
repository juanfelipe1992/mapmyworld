from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED
from datetime import datetime, timedelta
from schema.schema import Locations, Categories
from config.db import engine
from model.models import locations, categories, location_category_reviewed

router = APIRouter()
# Root
@router.get("/")
def root():
    return {"message":"Welcome to map my world"}
# Getting all locations
@router.get("/api/v1/locations")
def get_locations():
    with engine.connect() as conn:
        result = conn.execute(locations.select()).fetchall()
        return result
# Create a location    
@router.post("/api/v1/locations", status_code=HTTP_201_CREATED)
def create_location(data_location: Locations):
    with engine.connect() as conn:
        new_location = data_location.dict()
        conn.execute(locations.insert().values(new_location))
        print(new_location)
        return Response(status_code=HTTP_201_CREATED)
# Update a location 
@router.put("/api/v1/locations")
def update_location():
    pass

# Getting all categories
@router.get("/api/v1/categories")
def get_categories():
    with engine.connect() as conn:
        result = conn.execute(categories.select()).fetchall()
        return result

# Create a category
@router.post("/api/v1/categories", status_code=HTTP_201_CREATED)
def create_category(data_category: Categories):
    with engine.connect() as conn:
        new_category = data_category.dict()
        conn.execute(categories.insert().values(new_category))
        print(new_category)
        return Response(status_code=HTTP_201_CREATED)
    
# Update a category 
@router.put("/api/v1/categories")
def update_category():
    pass

# Get Recommendations    
@router.get("/api/v1/recommendations")
async def get_recomendations():
    # Generating all possible combinations if nos in location_category_reviewed
    all_combinations = [(loc['id'],cat['id']) for loc in locations for cat in categories]
    for loc_id, cat_id in all_combinations:
        if not any(r for r in location_category_reviewed if r.location_id == loc_id and r.category_id == cat_id):
            location_category_reviewed.append({'location_id':loc_id, 'category_id':cat_id, 'last_reviewed_date':None})

    # Filter unreviewed combinations in the last 30 days or never reviewed
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    potential_reommendations = [r for r in location_category_reviewed if r['last_reviewed_date'] is None or r['last_reviewed_date'] < cutoff_date]

    # Prioritize those never reviewed
    never_reviewed = [r for r in potential_reommendations if r['last_reviewed_date'] is None]
    recently_reviewed = [r for r in potential_reommendations if r['last_reviewed_date'] is not None]

    # Sort reviewed recients by date to give prioritize the least recent ones
    recently_reviewed.sort(key=lambda x: x['last_reviewed_date'])

    # Merge and select the first 10 recommendations
    combined_recommendations = never_reviewed + recently_reviewed
    top_recommendations = combined_recommendations[:10]

    return [location_category_reviewed(**r) for r in top_recommendations]