from sqlalchemy import  Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from config.db  import engine, meta_data

locations = Table("locations",meta_data,
                  Column("id",String(255), primary_key=True),
                  Column("longitude",String(255), nullable=False),
                  Column("latitude",String(255), nullable=False)
                )   

categories = Table("categories",meta_data,
                  Column("id",Integer, primary_key=True),
                  Column("name",String(255), nullable=False)
                )        

location_category_reviewed = Table("location_category_reviewed",meta_data,
                  Column("id",Integer, primary_key=True),
                  Column("location_id",Integer),
                  Column("category_id",Integer),
                  Column("last_review_date",DateTime),
                  Column("is_reviewed",Boolean)
                )        

meta_data.create_all(engine)