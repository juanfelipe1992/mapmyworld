from sqlalchemy import create_engine, MetaData
# Enable to connect my DB juanvalencia@localhost/mapmyworld
engine = create_engine("mysql+pymysql://juanvalencia:juan10.@localhost:3306/mapmyworld")
# Metadata
meta_data = MetaData()
