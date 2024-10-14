import unittest
import server.etherscan as etherscan
import math

class TestEtherScanAPIs(unittest.TestCase):
    '''
    References this hash: https://etherscan.io/tx/0x8395927f2e5f97b2a31fd63063d12a51fa73438523305b5b30e7bec6afb26f48
    We can compare directly things like blockNumber, from etc.
    '''
    validHash = "0x8395927f2e5f97b2a31fd63063d12a51fa73438523305b5b30e7bec6afb26f48"

    def test_get_internal_transaction_list_by_hash_empty_hash(self):
        result = etherscan.get_internal_transaction_list_by_hash("")
        self.assertEqual(result, [])
    
    def test_get_internal_transaction_list_by_hash_proper_hash(self):
        result = etherscan.get_internal_transaction_list_by_hash(self.validHash)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["blockNumber"], "14630148")
        self.assertEqual(result[0]["from"], "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45".lower())
        self.assertEqual(result[0]["isError"], "0")

    def test_get_token_transfer_fee_by_hash_empty_hash(self):
        transaction_list = etherscan.get_internal_transaction_list_by_hash(self.validHash)
        result = etherscan.get_token_transfer_fee_by_hash(transaction_list, "")
        self.assertEqual(result, [])

    '''
    Based on the EtherScan website, the transaction amount is around $22.12 on the day of transaction
    '''
    def test_get_token_transfer_fee_by_hash_proper_hash(self):
        transaction_list = etherscan.get_internal_transaction_list_by_hash(self.validHash)
        result = etherscan.get_token_transfer_fee_by_hash(transaction_list, self.validHash)
        self.assertNotEqual(len(result), 0)
        

if __name__ == '__main__':
    unittest.main()