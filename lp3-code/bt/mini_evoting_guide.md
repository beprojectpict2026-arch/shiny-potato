# BT Mini-project: E-voting system (guide for `mini_evoting.sol`)

**Problem statement:** a blockchain-based e-voting system where an admin sets up an election, registered voters vote exactly once, votes are public and cannot be changed, and anyone can read the result.

## Design

- **Phases:** `Registration` (admin adds candidates and registers voters), `Voting` (registered voters vote), `Ended` (winner can be read). The admin moves the phases with `startVoting()` and `endVoting()`.
- **Rules enforced by the contract:** only the admin can add candidates, register voters or change phases; a voter must be registered, can vote only once, and can only pick an existing candidate; nothing can change after the election ends.
- **Transparency:** every vote emits a `VoteCast` event and the counts are readable by anyone with `getCandidate(id)`.
- **Not included (limits to mention in the report):** votes are public and linked to the voter's address, so this is transparent rather than secret; a production system would add voter identity verification and a privacy technique such as zero-knowledge proofs. A web front-end (HTML + ethers.js talking to MetaMask) can be added on top of the same contract.

## Deploy and test on Remix + MetaMask (Sepolia)

1. In MetaMask create three accounts (Admin, Voter1, Voter2) and fund them with Sepolia test ETH (see `c1_metamask_wallet.md`).
2. Open remix.ethereum.org, create `EVoting.sol` and paste `mini_evoting.sol`. In the *Solidity compiler* tab compile with a 0.8.20+ compiler.
3. In *Deploy & Run Transactions* choose environment **Injected Provider - MetaMask**, make sure Admin and Sepolia are selected, and press **Deploy**. Confirm in MetaMask and note the contract address, gas used and transaction fee.
4. As Admin: `addCandidate("Alice")`, `addCandidate("Bob")`, `registerVoter(<Voter1 address>)`, `registerVoter(<Voter2 address>)`, then `startVoting()`.
5. Switch the MetaMask account to Voter1 and call `vote(0)`; switch to Voter2 and call `vote(1)` or `vote(0)`.
6. Try the failing cases and record the revert messages: Voter1 voting a second time, an unregistered account voting, a voter calling `startVoting`.
7. Switch back to Admin and call `endVoting()`, then call `winner()` and `getCandidate(0)`, `getCandidate(1)` to read the result.

> You can first try everything for free in Remix's built-in **Remix VM** environment (no MetaMask needed), which provides ten pre-funded accounts, then repeat on Sepolia for the real transaction fees.

## Test cases

| # | Action | Expected result |
|---|---|---|
| 1 | Admin adds 2 candidates | `candidateCount()` returns 2 |
| 2 | Non-admin calls `addCandidate` | Reverts "Only the admin can do this" |
| 3 | `startVoting()` with fewer than 2 candidates | Reverts "Need at least 2 candidates" |
| 4 | Registered voter votes once | `totalVotes` becomes 1, candidate count +1 |
| 5 | Same voter votes again | Reverts "You have already voted" |
| 6 | Unregistered account votes | Reverts "You are not a registered voter" |
| 7 | Vote before `startVoting()` | Reverts "Not allowed in the current phase" |
| 8 | `winner()` before `endVoting()` | Reverts "Not allowed in the current phase" |
| 9 | `winner()` after `endVoting()` | Returns the candidate with the most votes |

## Journal items

Date, title, problem definition, learning objective and outcome, theory (smart contract, Solidity, gas, blockchain voting), the contract listing, the test-case table with screenshots from Remix/Etherscan (deployment transaction, a vote transaction, a reverted transaction), gas and fee values, and the conclusion.
