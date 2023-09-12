My code is written in Python3 using Flask.

In order to run the API:
1. Install Python3 from https://www.python.org/downloads/
2. Install Flask by running the following command in the terminal: python3 -m pip install Flask
3. Start the application. From the command line, go to the directory where the fetch_receipt_processor.py file is downloaded and run: python3 fetch_receipt_processor.py
4. Open a new tab in terminal and run the following in command line (the JSON argument can be replaced with the json of any receipt):
curl -X POST http://localhost:5000/receipts/process -H "Content-Type: application/json" -d '{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}'
5. To get the points of that receipt ID, run: curl http://localhost:5000/receipts/{id}/points 
where you replace {id} with the id of the receipt you want to get the points for.
6. To run the unit tests, from the command line, go to the directory where the fetch_receipt_processor_test.py file is downloaded and run: python3 fetch_receipt_processor_test.py