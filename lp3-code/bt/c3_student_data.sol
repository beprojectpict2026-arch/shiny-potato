// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/*
 * BT Assignment 3 - Student data contract using structures, arrays and a fallback function.
 *
 * Problem statement: create student records in Solidity using a struct (one student), an array
 * (list of all students) and a fallback function (runs when a call matches no function or plain
 * ETH is sent), deploy the contract on Ethereum (test network) and observe the transaction fee
 * and gas values.
 * Tools used: Solidity ^0.8.20, Remix IDE, MetaMask on the Sepolia test network.
 *
 * Driver (in Remix): deploy, addStudent(1, "Asha", 85), addStudent(2, "Ravi", 78), call getStudent(0),
 * totalStudents(), then send 1 wei to the contract address with empty calldata to trigger the fallback.
 * After each transaction open the Remix console / Etherscan and note "gas used" and "transaction fee"
 * (see c4_ether_transactions.md for how to record them).
 */
contract StudentData {
    // structure: one student record
    struct Student {
        uint256 rollNo;
        string name;
        uint8 marks;
    }

    // array: all students, in the order they were added
    Student[] private students;

    uint256 public fallbackCalls;  // how many times the fallback function has run

    event StudentAdded(uint256 indexed rollNo, string name);
    event FallbackCalled(address indexed sender, uint256 value, bytes data);

    function addStudent(uint256 rollNo, string memory name, uint8 marks) public {
        require(marks <= 100, "Marks must be 0-100");
        students.push(Student(rollNo, name, marks));
        emit StudentAdded(rollNo, name);
    }

    function getStudent(uint256 index) public view returns (uint256 rollNo, string memory name, uint8 marks) {
        require(index < students.length, "No student at this index");
        Student memory s = students[index];
        return (s.rollNo, s.name, s.marks);
    }

    function totalStudents() public view returns (uint256) {
        return students.length;
    }

    // fallback: runs when the contract is called with data that matches no function, or when
    // ETH is sent with no data (there is no receive() function in this contract).
    fallback() external payable {
        fallbackCalls += 1;
        emit FallbackCalled(msg.sender, msg.value, msg.data);
    }
}
