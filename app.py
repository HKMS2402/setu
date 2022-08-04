from flask_restful import Api, Resource, reqparse
from flask import Flask, request, make_response
import os
import sys

cuurent_dir = os.getcwd()
sys.path.append(cuurent_dir)

from models import user, splitTypes, bill, balanceSheet

app = Flask(__name__)
api = Api(app)

# Defining list of arguments for creating new user
user_post_args = reqparse.RequestParser()
user_post_args.add_argument("name", type=str, help="required", required=True)
user_post_args.add_argument("email", type=str, help="required", required=True)
user_post_args.add_argument(
    "contact", type=str, help="required", required=True)


# Defining list of arguments for creating new bill with exact split
# exact_split_post_args = reqparse.RequestParser()
# exact_split_post_args.add_argument("bill_no",type= str, help = "required", required = True)
# exact_split_post_args.add_argument("bill_name",type= str, help = "required", required = True)
# exact_split_post_args.add_argument("category",type= str, help = "required", required = True)
# exact_split_post_args.add_argument("created_by",type= str, help = "required", required = True)
# exact_split_post_args.add_argument("paid_by",type= str, help = "required", required = True)
# exact_split_post_args.add_argument("amount",type= float, help = "required", required = True)
# exact_split_post_args.add_argument("splits",type= list, help = "required", required = True)


# Defining list of arguments for creating new bill with equal split
# equal_split_post_args = reqparse.RequestParser()
# equal_split_post_args.add_argument("bill_no",type= str, help = "required", required = True)
# equal_split_post_args.add_argument("bill_name",type= str, help = "required", required = True)
# equal_split_post_args.add_argument("category",type= str, help = "required", required = True)
# equal_split_post_args.add_argument("created_by",type= str, help = "required", required = True)
# equal_split_post_args.add_argument("paid_by",type= str, help = "required", required = True)
# equal_split_post_args.add_argument("amount",type= float, help = "required", required = True)
# equal_split_post_args.add_argument("splits",type= dict, help = "required", required = True)


# Defining list of arguments for creating new bill with percentage split
# percent_split_post_args = reqparse.RequestParser()
# percent_split_post_args.add_argument("bill_no",type= str, help = "required", required = True)
# percent_split_post_args.add_argument("bill_name",type= str, help = "required", required = True)
# percent_split_post_args.add_argument("category",type= str, help = "required", required = True)
# percent_split_post_args.add_argument("created_by",type= str, help = "required", required = True)
# percent_split_post_args.add_argument("paid_by",type= str, help = "required", required = True)
# percent_split_post_args.add_argument("amount",type= float, help = "required", required = True)
# percent_split_post_args.add_argument("splits",type= list, help = "required", required = True)


class FetchUser(Resource):

    def get(self, email=None):
        if email is None:
            result = user.User.getAllUsers()
            if len(result) > 0:
                return {
                    "success": "true",
                    "message": "data fetched successfully",
                    "data": result
                }
            else:
                return {
                    "success": "true",
                    "message": "no data fetched",
                    "data": []
                }
        else:
            result = user.User.getUserByEmail(email)
            if len(result) > 0:
                return {
                    "success": "true",
                    "message": "records fetched",
                    "data": result
                }
            else:
                return {
                    "success": "true",
                    "message": "no records fetched",
                    "data": []
                }


class CreateUser(Resource):
    def post(self):
        args = user_post_args.parse_args()
        email = args.email
        checkExistingUser = user.User.getUserByEmail(email)
        name = args.name
        contact = args.contact
        if len(checkExistingUser) > 0:
            return {
                "success": "false",
                "message": "This email id is already registered."
            }, 409
        else:
            new_user = user.User(name, email, contact)
            result = new_user.createUser()
            print(result)
            if result["success"] == "true":
                return {
                    "success": "true",
                    "data": result["data"]
                }, 201
            else:
                return result, 500


class CreateBillWithExactSplit(Resource):
    def post(self):

        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            args = request.get_json()
            args["split_type"] = "EXACT"

            new_bill = bill.Bill(args["bill_no"], args["bill_name"], args["category"],
                                 args["created_by"], args["paid_by"], args["amount"], "EXACT", args["splits"])

            final_bill = new_bill.createBill()
            if(final_bill["success"]) == "true":
                return final_bill
            else:

                return final_bill,403
        else:
            return 'Content-Type not supported! Should be application/json', 403

        


class CreateBillWithEqualSplit(Resource):
    def post(self):

        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            args = request.get_json()

            new_bill = bill.Bill(args["bill_no"], args["bill_name"], args["category"],
                                 args["created_by"], args["paid_by"], args["amount"], "EQUAL", args["splits"])

            final_bill = new_bill.createBill()
            if(final_bill["success"]) == "true":
                return final_bill
            else:

                return final_bill,403
        else:
            return 'Content-Type not supported! Should be application/json', 403


class CreateBillWithPercentageSplit(Resource):
    def post(self):

        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            args = request.get_json()

            new_bill = bill.Bill(args["bill_no"], args["bill_name"], args["category"],
                                 args["created_by"], args["paid_by"], args["amount"], "PERCENTAGE", args["splits"])

            final_bill = new_bill.createBill()
            if(final_bill["success"]) == "true":
                return final_bill
            else:

                return final_bill,403
        else:
            return 'Content-Type not supported! Should be application/json', 403


class GetBalanceSheet(Resource):
    def get(self, email):
        result = balanceSheet.BalanceSheet.findBalanceSheetByUserEmail(email)
        if len(result) > 0:
                return {
                    "success": "true",
                    "message": "records fetched",
                    "data": result[0]
                }
        else:
            return {
                "success": "true",
                "message": "no records fetched",
                "data": []
            }

class SettleBalance(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            args = request.get_json()

            settlement = balanceSheet.BalanceSheet.settlePayment(args["paid_to"], args["paid_by"], args["amount"])

            return settlement
        else:
            return 'Content-Type not supported! Should be application/json', 403



api.add_resource(FetchUser, "/setu/api/user/<email>", "/setu/api/users")
api.add_resource(CreateUser, "/setu/api/user/create")
api.add_resource(CreateBillWithExactSplit, "/setu/api/bill/create/split/exact")
api.add_resource(CreateBillWithEqualSplit, "/setu/api/bill/create/split/equal")
api.add_resource(CreateBillWithPercentageSplit,
                 "/setu/api/bill/create/split/percent")
api.add_resource(GetBalanceSheet, "/setu/api/balance/<email>")
api.add_resource(SettleBalance, "/setu/api/balance/settle")

if __name__ == "__main__":
    app.run(debug=True)
