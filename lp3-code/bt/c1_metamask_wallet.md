# BT Assignment 1: Install MetaMask, create a wallet and study spending Ether per transaction

**Problem statement:** install MetaMask, create your own wallet for crypto transactions, and perform a transaction on a test network.
**Tools:** Google Chrome (or Firefox/Edge) with the MetaMask browser extension, a Sepolia test-network faucet, Sepolia Etherscan.

> The manual lists Rinkeby, Kovan, Ropsten and Goerli. Those test networks have been shut down, so use **Sepolia**, the current Ethereum test network. Test ETH has no real value.

## What you need (nothing to compile here)

| Tool | What it is | Install? |
|---|---|---|
| **MetaMask** | A browser-extension wallet. It stores your private key, shows your account address and signs transactions, so it is also how Remix talks to the blockchain. | Yes, browser extension from the official site only (metamask.io) |
| **Remix IDE** (remix.ethereum.org) | A web IDE with the Solidity compiler built in. Used for assignments 2, 3 and the mini-project. | No, runs in the browser |
| **Solidity compiler** | Converts a `.sol` contract into code that the Ethereum Virtual Machine runs. | No, already inside Remix |
| VS Code + Solidity extension | Optional editor with syntax help. | Optional |

## Steps

1. **Install MetaMask.** Open metamask.io in Chrome, choose *Download*, and add it from the Chrome Web Store (*Add to Chrome*, then *Add extension*). Check the publisher is MetaMask and the download count is in the millions, because fake wallet extensions exist.
2. **Create a wallet.** Click *Create a new wallet*, accept the terms, and set a password (used only on this device).
3. **Secure the account.** MetaMask shows a **12-word Secret Recovery Phrase**. Write it on paper in order, confirm it when asked, and **never share it or screenshot it**. Anyone with the phrase controls the wallet.
4. **Find your address.** Under *Account 1* click the address to copy it (it starts with `0x`).
5. **Switch to the test network.** Settings, Advanced, enable *Show test networks*, then pick **Sepolia** in the network drop-down.
6. **Get free test ETH.** Copy your address and use a Sepolia faucet (search "Sepolia faucet"; for example the ones from Alchemy or Google Cloud). The ETH arrives after a short wait.
7. **Create a second account.** Click the account menu, then *Add account*, and name them Alice and Bob.
8. **Send a transaction.** From Alice choose *Send*, paste Bob's address, enter `0.01` ETH, review the gas fee MetaMask shows, and *Confirm*.
9. **Verify.** Open the *Activity* tab, click the transaction, then *View on block explorer* (Sepolia Etherscan). Note the transaction hash, status, block, gas used and fee.

## Journal items to fill in

| Item | Your value |
|---|---|
| Date | |
| Wallet address (Account 1) | `0x...` (public address only, never the phrase) |
| Network | Sepolia |
| Faucet used and amount received | |
| Transaction hash of the transfer | |
| Value sent / Gas used / Transaction fee | |
| Screenshots | wallet created, balance, send screen, Etherscan page |

**Theory to write:** digital wallet, public/private key pair, seed phrase, MetaMask, test network vs main network, gas.
**Conclusion:** students install MetaMask, create a secure wallet with a recovery phrase, get test ETH and complete a transaction on an Ethereum test network.
