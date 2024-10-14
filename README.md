# uniswap_transaction
## Project Introduction
This project aims to build a simple application to track the transaction fee assocaited with a UniSwap Transaction.

## Tech Stack
This project is built with the following:
- Python 3.12.3
- Flask
- SwaggerUI

We also utilized the following downstream API services provided:
- Etherscan: https://docs.etherscan.io/
- Binance: 

## Project Directory
```
.
├── README.md
├── app.py
├── docs
│   └── swagger.json 
├── requirements.txt
├── server
│   ├── binance.py
│   └── etherscan.py
└── tests
    └── test_etherscan.py

```
- `README.md`: Markdown file briefly explaining the project
- `app.py`: Where the main code is executed
- `docs/swagger.json`: Our Interface file describing our HTTP Rest APIs
- `requirements.txt`: Used for docker compose
- `server/`: Contains bulk of the processing code used when calling downstream ETH or Binance APIs
- `tests/`: Folder contains our test files

## Project Setup





## Testing
Ensure that the project setup is completed beforehand.

Run the following line in your CLI to run tests:

```
python3 -m unittest discover tests/
```
