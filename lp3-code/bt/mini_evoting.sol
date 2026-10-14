// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
 * BT Mini-project - E-voting system (decentralised application backend).
 *
 * Problem statement: build a blockchain-based e-voting system. The election admin adds candidates
 * and registers voters; voting happens in phases (Registration -> Voting -> Ended); every registered
 * voter can vote only once; votes are public and cannot be changed, and anyone can read the result.
 * Tools used: Solidity ^0.8.20, Remix IDE, MetaMask on the Sepolia test network.
 *
 * Driver (in Remix): deploy with account 1 (admin), addCandidate("Alice") and addCandidate("Bob"),
 * registerVoter(<address of account 2>) and registerVoter(<address of account 3>), startVoting(),
 * vote(0) from account 2, vote(1) from account 3, endVoting(), then call winner() and getCandidate(0).
 * See mini_evoting_guide.md for the full step list.
 */
contract EVoting {
    enum Phase { Registration, Voting, Ended }

    struct Candidate {
        string name;
        uint256 voteCount;
    }

    struct Voter {
        bool registered;
        bool voted;
    }

    address public admin;
    Phase public phase;
    Candidate[] private candidates;
    mapping(address => Voter) public voters;
    uint256 public totalVotes;

    event CandidateAdded(uint256 indexed id, string name);
    event VoterRegistered(address indexed voter);
    event PhaseChanged(Phase newPhase);
    event VoteCast(address indexed voter, uint256 indexed candidateId);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Only the admin can do this");
        _;
    }

    modifier inPhase(Phase p) {
        require(phase == p, "Not allowed in the current phase");
        _;
    }

    constructor() {
        admin = msg.sender;  // whoever deploys the contract is the election admin
        phase = Phase.Registration;
    }

    // ---- Registration phase (admin only) ----
    function addCandidate(string memory name) public onlyAdmin inPhase(Phase.Registration) {
        candidates.push(Candidate(name, 0));
        emit CandidateAdded(candidates.length - 1, name);
    }

    function registerVoter(address voter) public onlyAdmin inPhase(Phase.Registration) {
        require(!voters[voter].registered, "Voter already registered");
        voters[voter].registered = true;
        emit VoterRegistered(voter);
    }

    function startVoting() public onlyAdmin inPhase(Phase.Registration) {
        require(candidates.length >= 2, "Need at least 2 candidates");
        phase = Phase.Voting;
        emit PhaseChanged(phase);
    }

    // ---- Voting phase ----
    function vote(uint256 candidateId) public inPhase(Phase.Voting) {
        Voter storage v = voters[msg.sender];
        require(v.registered, "You are not a registered voter");
        require(!v.voted, "You have already voted");
        require(candidateId < candidates.length, "Invalid candidate");
        v.voted = true;
        candidates[candidateId].voteCount += 1;
        totalVotes += 1;
        emit VoteCast(msg.sender, candidateId);
    }

    function endVoting() public onlyAdmin inPhase(Phase.Voting) {
        phase = Phase.Ended;
        emit PhaseChanged(phase);
    }

    // ---- Results (anyone can read) ----
    function candidateCount() public view returns (uint256) {
        return candidates.length;
    }

    function getCandidate(uint256 id) public view returns (string memory name, uint256 voteCount) {
        require(id < candidates.length, "Invalid candidate");
        return (candidates[id].name, candidates[id].voteCount);
    }

    // winner = candidate with the most votes (the first one wins a tie); only after voting has ended
    function winner() public view inPhase(Phase.Ended) returns (string memory name, uint256 voteCount) {
        uint256 best = 0;
        for (uint256 i = 1; i < candidates.length; i++) {
            if (candidates[i].voteCount > candidates[best].voteCount) {
                best = i;
            }
        }
        return (candidates[best].name, candidates[best].voteCount);
    }
}
