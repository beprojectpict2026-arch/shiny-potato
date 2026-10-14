// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
 * BT Assignment 2 - Bank account smart contract (deposit, withdraw, show balance).
 *
 * Problem statement: write a smart contract for a customer's bank account with three
 * operations: deposit money, withdraw money and show the balance. Every customer (account
 * address) has a separate balance kept inside the contract; amounts are in wei (1 ETH = 10^18 wei).
 * Tools used: Solidity ^0.8.20, Remix IDE (compile + deploy), MetaMask on the Sepolia test network.
 *
 * Driver (in Remix, "Deploy & Run Transactions"): deploy, then call deposit with a Value of
 * 1000000000000000 wei (0.001 ETH), call showBalance, call withdraw(500000000000000) and call
 * showBalance again. See README steps in c1_metamask_wallet.md for setting up Remix + MetaMask.
 */
contract BankAccount {
    // balance of every customer, indexed by the customer's address
    mapping(address => uint256) private balances;

    event Deposited(address indexed customer, uint256 amount);
    event Withdrawn(address indexed customer, uint256 amount);

    // Deposit money: the ETH sent with the call (msg.value) is added to the sender's balance.
    function deposit() public payable {
        require(msg.value > 0, "Deposit must be more than 0");
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }

    // Withdraw money: the amount is paid back to the sender if the balance is enough.
    function withdraw(uint256 amount) public {
        require(amount > 0, "Amount must be more than 0");
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;  // update the balance first, then send (prevents re-entrancy)
        (bool sent, ) = payable(msg.sender).call{value: amount}("");
        require(sent, "Transfer failed");
        emit Withdrawn(msg.sender, amount);
    }

    // Show balance: read-only call, costs no gas when called directly from Remix.
    function showBalance() public view returns (uint256) {
        return balances[msg.sender];
    }
}
