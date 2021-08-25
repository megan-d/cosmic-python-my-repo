from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from allocation import config
from allocation.adapters import orm
from allocation.adapters import repository
from allocation.domain import model


# orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home_endpoint():
    return 'hi'

@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    batches = repository.SqlAlchemyRepository(session).list()
    line = model.OrderLine(
        request.json["orderid"], request.json["sku"], request.json["qty"],
    )
    batchref = model.allocate(line, batches)

    return {"batchref": batchref}, 201
