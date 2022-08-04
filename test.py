import requests

BASE = "http://127.0.0.1:5000/"

response = requests.post(BASE + "setu/api/bill/create/split/exact", {
    "bill_no": "1231123124",
    "bill_name": "Posh Pouf Restaurant",
    "category": "Food",
    "created_by": "kartik02manas@gmail.com",
    "paid_by": "mohak014@gmail.com",
    "amount": 1000.0,
    "splits": [
        {
            "email": "kartik02manas@gmail.com",
            "amount": 300.0
        },
        {
            "email": "mohak014@gmail.com",
            "amount": 700.0
        }
    ]
})


print(response.json())
