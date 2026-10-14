# BT Assignment 5: Survey report on types of blockchains and their real-time use cases

**Problem statement:** write a survey report on the types of blockchains and their real-time use cases.

## 1. Introduction

A blockchain is a shared database (ledger) kept as a chain of blocks, where each block holds a batch of transactions and the hash of the previous block, so past records cannot be altered without detection. All blockchains are distributed ledgers, but not every distributed ledger is a blockchain, since a ledger need not be organised into blocks. Blockchains differ mainly in **who may read the ledger, who may write to it, and who validates transactions**.

## 2. Types of blockchains

| Type | Who can join | Who validates | Examples | Main property |
|---|---|---|---|---|
| **Public (permissionless)** | Anyone, anonymously | Open to everyone, via consensus such as proof of work or proof of stake | Bitcoin, Ethereum | Fully decentralised, transparent, slower and costlier per transaction |
| **Private (permissioned)** | Only invited participants of one organisation | The owning organisation | Hyperledger Fabric deployments inside a company | Fast, private and controlled, but more centralised |
| **Consortium (federated)** | A fixed group of organisations | Pre-selected nodes of the group | R3 Corda, Hyperledger Fabric networks shared by several firms | Shared governance among partners, faster than public chains |
| **Hybrid / semi-private** | Part open and part restricted | Mix of both | Concept model where private data is kept inside and proofs are published publicly | Privacy for sensitive data with public verifiability (still mostly a concept, as the manual notes) |

**Permissioned vs permissionless:** on a permissionless chain anyone can run a node and send transactions; on a permissioned chain identities are known and an access policy decides who may read or write.

## 3. Real-time use cases

**Public blockchains**
- **Decentralised finance (DeFi):** lending, trading and savings through smart contracts on Ethereum without a bank.
- **Cryptocurrencies and payments:** Bitcoin and Ether transfers anywhere without an intermediary.
- **Digital identity and NFTs:** user-controlled identity credentials and proof of ownership of digital items.
- **Central bank digital currencies (CBDC):** pilots use blockchain-like ledgers for digital forms of central bank money.

**Private and consortium blockchains**
- **Supply chain and retail:** tracking goods from source to shelf, detecting counterfeits, and food traceability (for example IBM Food Trust, built on Hyperledger Fabric).
- **Healthcare:** sharing patient records with consent, verifying doctors' credentials, and tracking genuine drugs.
- **Insurance:** automatic claim settlement by smart contracts and fewer paper trails.
- **Banking and financial services:** faster interbank settlement, trade finance and privacy for sensitive data.
- **Government:** land records, transparent election systems and digital identity.

## 4. Comparison of the three models

| | Public | Private | Consortium |
|---|---|---|---|
| Decentralisation | High | Low | Medium |
| Speed / throughput | Low | High | High |
| Transaction cost | Fees (gas) | Low | Low |
| Privacy | Pseudonymous but visible | High | Restricted to members |
| Trust model | Trust in code and consensus | Trust in one owner | Trust shared by members |

## 5. Conclusion

Public blockchains give openness and censorship resistance and suit open financial services; private blockchains suit one organisation that needs speed and confidentiality; consortium blockchains suit groups of businesses that must share a ledger without trusting a single owner. Choosing a type depends on the need for decentralisation, privacy, performance and regulatory control.

## References

- Imran Bashir, *Mastering Blockchain*, 2nd ed., Packt, 2018.
- Arvind Narayanan et al., *Bitcoin and Cryptocurrency Technologies*.
- Ethereum documentation: ethereum.org/developers/docs
- Hyperledger Fabric and R3 Corda project documentation.
