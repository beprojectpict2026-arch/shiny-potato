<h1 align="center">Blockchain E-Voting System</h1>
<h3 align="center">Blockchain Technology (410243) - Mini-Project Report</h3>
<p align="center">Laboratory Practice III (410246)</p>

<hr/>

<h2 align="center">1\. Problem Statement</h2>

Develop a blockchain-based application for an e-voting system. Voting should be transparent and tamper-proof: only registered voters can vote, each voter can vote once, votes cannot be changed after they are cast, and anyone can verify the result.

<h2 align="center">2\. Objectives</h2>

1. Write a smart contract in Solidity that runs an election in clear phases.
2. Let only the admin add candidates, register voters and move the election from one phase to the next.
3. Allow each registered voter to vote exactly once, and only while voting is open.
4. Make the votes and the result public, and record every action as an event on the blockchain.
5. Deploy the contract on an Ethereum test network, test it, and observe the gas used and the transaction fee.

<h2 align="center">3\. Methodology</h2>

**Why a blockchain.** A normal voting database is controlled by one party, which could change the counts. On a blockchain the vote is stored in a transaction that every node validates. Once confirmed it cannot be altered, and anyone can recount the votes. A **smart contract** is a program stored on the blockchain whose rules are enforced by the network and not by a person.

**Design.** The contract moves through three phases, and each function works only in its own phase:

| Phase | Allowed actions | Who |
|---|---|---|
| Registration | `addCandidate`, `registerVoter`, `startVoting` | Admin |
| Voting | `vote`, then `endVoting` | Registered voters; admin ends it |
| Ended | `winner`, `getCandidate` (reading the result) | Anyone |

**Rules enforced by the contract**

- The account that deploys the contract becomes the admin. Only the admin can add candidates, register voters or change the phase.
- Voting can start only when there are at least 2 candidates.
- A voter must be registered, can vote only once, and can only pick an existing candidate.
- The winner can be read only after voting has ended. In a tie the first candidate wins.

**Tools.** Solidity 0.8.20 or newer; the Remix IDE (browser) to write, compile and deploy; MetaMask wallet; the Sepolia test network with free test Ether. The Remix VM (a local test blockchain with ten funded accounts) is used first, so no real transactions are needed for a first test.

<h2 align="center">4\. Implementation Details</h2>

The contract `EVoting` is in `bt/mini_evoting.sol`.

| Element | Meaning in the code |
|---|---|
| `enum Phase { Registration, Voting, Ended }` | The three phases of the election |
| `struct Candidate { name, voteCount }` and `Candidate[] candidates` | The list of candidates and their votes |
| `struct Voter { registered, voted }` and `mapping(address => Voter) voters` | The state of each voter, looked up by wallet address |
| `modifier onlyAdmin` | Stops everyone but the admin from calling a function (`require(msg.sender == admin)`) |
| `modifier inPhase(p)` | Allows a function only in the phase `p` |
| `event VoteCast`, `CandidateAdded`, `VoterRegistered`, `PhaseChanged` | Records every action in the transaction log, so the election can be audited |
| `require(condition, "message")` | Stops the transaction and undoes its changes with a message if a rule is broken |

**Functions:** `addCandidate(name)`, `registerVoter(address)`, `startVoting()`, `vote(candidateId)`, `endVoting()`, `candidateCount()`, `getCandidate(id)`, `winner()`.

**Deploy and test (summary; full steps in `bt/mini_evoting_guide.md`)**

1. In MetaMask create three accounts (Admin, Voter1, Voter2) and add Sepolia test Ether.
2. In Remix paste `mini_evoting.sol` and compile with 0.8.20 or newer.
3. In *Deploy & Run* choose **Injected Provider - MetaMask** with the Admin account and press *Deploy*.
4. As Admin: `addCandidate("Alice")`, `addCandidate("Bob")`, `registerVoter(<Voter1>)`, `registerVoter(<Voter2>)`, `startVoting()`.
5. As Voter1 call `vote(0)`; as Voter2 call `vote(1)` or `vote(0)`.
6. As Admin call `endVoting()`, then `winner()`, `getCandidate(0)` and `getCandidate(1)`.

<h2 align="center">5\. Results</h2>

**Network:** ______ (Sepolia / Remix VM). **Contract address:** ______ . **Compiler:** ______ .

<p align="center"><img src="screenshots/deploy.png" width="560" alt="Contract deployed in Remix"/></p>
<p align="center"><em>Figure 1: Contract deployed in Remix</em></p>

**5.1 Test cases.** The "expected result" column follows from the contract's `require()` checks. Fill the last column from your run.

| # | Action | Expected result | Your result |
|---|---|---|---|
| 1 | Admin adds 2 candidates | `candidateCount()` returns 2 | ______ |
| 2 | A non-admin calls `addCandidate` | Reverts: "Only the admin can do this" | ______ |
| 3 | `startVoting()` with fewer than 2 candidates | Reverts: "Need at least 2 candidates" | ______ |
| 4 | Registered voter votes once | Candidate's count and `totalVotes` increase by 1 | ______ |
| 5 | The same voter votes again | Reverts: "You have already voted" | ______ |
| 6 | An unregistered account votes | Reverts: "You are not a registered voter" | ______ |
| 7 | Vote before `startVoting()` | Reverts: "Not allowed in the current phase" | ______ |
| 8 | `winner()` before `endVoting()` | Reverts: "Not allowed in the current phase" | ______ |
| 9 | `winner()` after `endVoting()` | Returns the candidate with the most votes | ______ |

<p align="center"><img src="screenshots/vote_transaction.png" width="560" alt="A vote transaction"/></p>
<p align="center"><em>Figure 2: A successful vote transaction</em></p>

<p align="center"><img src="screenshots/revert.png" width="560" alt="A reverted transaction"/></p>
<p align="center"><em>Figure 3: A second vote by the same voter is rejected</em></p>

**5.2 Gas and fee (from Remix or Etherscan).**

| Transaction | Gas used | Fee (ETH) |
|---|---|---|
| Deploy contract | ______ | ______ |
| `addCandidate` | ______ | ______ |
| `registerVoter` | ______ | ______ |
| `vote` | ______ | ______ |

**5.3 Final result.** Votes: Alice ___ , Bob ___ . `winner()` returned ______ .

**Analysis.** A rejected transaction (cases 2, 3, 5, 6, 7 and 8) changes nothing on the chain, which shows that the rules are enforced by the contract. Writing data (deploying, adding a candidate, voting) costs gas, while reading the result with `getCandidate` and `winner` is free. Anyone can recount the votes from the `VoteCast` events.

**Limits.** Votes are public and linked to the voter's wallet address, so the system is transparent but not secret. A real system would also verify each voter's identity and use a privacy technique such as zero-knowledge proofs. A web front-end (HTML with ethers.js talking to MetaMask) can be added on top of the same contract.

**Conclusion.** The smart contract runs an election in three phases, allows one vote per registered voter, and gives a public, tamper-proof result.
