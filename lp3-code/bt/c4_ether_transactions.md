# BT Assignment 4: Study spending Ether per transaction

**Problem statement:** study how much Ether each transaction costs. Create at least two accounts, perform a series of transactions, and analyse the details.
**Tools:** MetaMask (two or more accounts) on the Sepolia test network, Sepolia Etherscan, Remix IDE (to compare with contract calls from assignments 2 and 3).

## Theory in short

- A **transaction** is a signed instruction from an account (from, to, value, data, nonce, gas limit and fee settings).
- **Gas** measures the computation a transaction needs. A plain ETH transfer always uses **21,000 gas**; calling or deploying a contract uses more.
- **Fee paid = gas used × effective gas price.** Gas price is in **gwei** (1 gwei = 10^-9 ETH). Since the London upgrade the price is `base fee` (burned) + `priority fee` (tip to the validator); `max fee per gas` is the most you are willing to pay.
- Worked example: 21,000 gas × 20 gwei = 420,000 gwei = **0.00042 ETH**. Unused gas is refunded, and the amount sent (value) is separate from the fee.
- Ethereum now uses **proof of stake** (validators), not proof-of-work mining as the older manual text describes.

## Steps

1. Create Alice and Bob in MetaMask on Sepolia and fund Alice from a faucet (see `c1_metamask_wallet.md`).
2. Perform this series of transactions and open each one on Etherscan:
   1. Alice sends 0.01 ETH to Bob.
   2. Alice sends 0.02 ETH to Bob, and then again with the *Advanced* gas option on "Low" priority.
   3. Bob sends 0.005 ETH back to Alice.
   4. Deploy `c2_bank_account.sol` from Remix (a contract deployment transaction).
   5. Call `deposit` on the deployed bank contract with value 0.001 ETH (a contract execution).
   6. Call `addStudent` on `c3_student_data.sol` (a contract execution that writes storage).
3. For every transaction copy these fields from Etherscan: *Transaction Hash, Status, Block, From, To, Value, Gas Limit, Gas Used, Gas Price, Base Fee, Priority Fee, Transaction Fee, Nonce*.
4. Fill in the analysis table and compute fee = gas used × gas price for each row to check it matches Etherscan's *Transaction Fee*.

## Analysis table (fill with your observed values)

| # | Type | Value (ETH) | Gas limit | Gas used | Gas price (gwei) | Fee (ETH) | Nonce |
|---|---|---|---|---|---|---|---|
| 1 | Transfer | 0.01 | 21000 | 21000 | | | |
| 2 | Transfer | 0.02 | 21000 | 21000 | | | |
| 3 | Transfer | 0.005 | 21000 | 21000 | | | |
| 4 | Contract deployment | 0 | | | | | |
| 5 | Contract call (`deposit`) | 0.001 | | | | | |
| 6 | Contract call (`addStudent`) | 0 | | | | | |

## What to observe and conclude

- Every simple transfer uses exactly 21,000 gas regardless of the value sent; the **fee changes only with the gas price** (network congestion).
- Contract deployment and calls cost much more gas, since they run code and write storage; longer data and more storage writes cost more.
- The sender's balance drops by **value + fee**; the receiver gains only the value.
- The nonce increases by one for each transaction from the same account, so transactions are ordered and cannot be replayed.
- Test networks use free test ETH, but on the main network every one of these fees is real money.

**Conclusion:** students understand how Ether is spent per transaction through gas, gas price and the transaction fee, and can read these values from the explorer.
