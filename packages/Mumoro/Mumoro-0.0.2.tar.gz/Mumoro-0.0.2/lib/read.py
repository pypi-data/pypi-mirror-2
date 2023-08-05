from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, mapper
from generate import *

engine = create_engine('sqlite:///blah.db')
meta = MetaData()
meta.bind = engine
nodes = Table('nodes', meta, autoload=True, autoload_with=engine)

for c in nodes.columns:
    print c


mapper(Node, nodes)



Session = sessionmaker(bind=engine)
session = Session()
for node in session.query(nodes):
    print node.id, node.original_id

