from flask_restful import reqparse,Resource
from flask_jwt import jwt_required
from mycode.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item must have store id"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Requested item does not exist"},404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "Item already exists with {}".format(name)}, 400

        request_data = Item.parser.parse_args()
        print("requested_data:",request_data)
        item = ItemModel(name, **request_data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while insertion"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        else:
            return {"message": "Item to delete does not  exists"}, 400
        return {"message": "Item {} deleted successfully".format(name)}, 200

    def put(self, name):
        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **request_data)
        else:
            item.price = request_data['price']
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):

    def get(self):
        return {"items": list(map(lambda x: x.json(),ItemModel.query.all()))}, 200


