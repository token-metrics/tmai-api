// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

/**
 * @title Mock veTMAI Token
 * @dev Mock implementation of veTMAI token for testing
 */
contract MockVeTMAI {
    mapping(address => uint256) private _balances;
    
    function balanceOf(address account) external view returns (uint256) {
        return _balances[account];
    }
    
    function setBalance(address account, uint256 amount) external {
        _balances[account] = amount;
    }
}
