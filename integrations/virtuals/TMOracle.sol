// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

interface IVeTMAI {
    function balanceOf(address account) external view returns (uint256);
}

/**
 * @title Token Metrics Oracle
 * @dev Oracle providing cryptocurrency ratings from Token Metrics API
 */
contract TMOracle {
    address public owner;
    address public keeper;
    address public veTMAIToken;
    
    struct Rating {
        string symbol;
        uint256 timestamp;
        uint256 rating;    // Rating scaled by 100 (e.g., 85.7 -> 8570)
        uint256 technical; // Technical score scaled by 100
        uint256 fundamental; // Fundamental score scaled by 100
    }
    
    mapping(string => Rating) public ratings;
    string[] public supportedSymbols;
    
    event RatingUpdated(string symbol, uint256 rating, uint256 timestamp);
    event KeeperUpdated(address oldKeeper, address newKeeper);
    event VeTMAITokenUpdated(address oldToken, address newToken);
    
    modifier onlyOwner() {
        require(msg.sender == owner, "TMOracle: caller is not the owner");
        _;
    }
    
    modifier onlyKeeper() {
        require(msg.sender == keeper, "TMOracle: caller is not the keeper");
        _;
    }
    
    modifier requireStake() {
        require(IVeTMAI(veTMAIToken).balanceOf(msg.sender) > 0, "TMOracle: caller has no veTMAI stake");
        _;
    }
    
    /**
     * @dev Constructor
     * @param _veTMAIToken Address of the veTMAI staking contract
     */
    constructor(address _veTMAIToken) {
        owner = msg.sender;
        keeper = msg.sender;
        veTMAIToken = _veTMAIToken;
    }
    
    /**
     * @dev Set a new keeper address
     * @param _keeper New keeper address
     */
    function setKeeper(address _keeper) external onlyOwner {
        address oldKeeper = keeper;
        keeper = _keeper;
        emit KeeperUpdated(oldKeeper, _keeper);
    }
    
    /**
     * @dev Set the veTMAI token address
     * @param _veTMAIToken New veTMAI token address
     */
    function setVeTMAIToken(address _veTMAIToken) external onlyOwner {
        address oldToken = veTMAIToken;
        veTMAIToken = _veTMAIToken;
        emit VeTMAITokenUpdated(oldToken, _veTMAIToken);
    }
    
    /**
     * @dev Update rating for a cryptocurrency
     * @param _symbol Token symbol (e.g., "BTC")
     * @param _rating Rating value scaled by 100
     * @param _technical Technical score scaled by 100
     * @param _fundamental Fundamental score scaled by 100
     */
    function updateRating(
        string calldata _symbol,
        uint256 _rating,
        uint256 _technical,
        uint256 _fundamental
    ) external onlyKeeper {
        // Check if symbol exists in supportedSymbols
        bool symbolExists = false;
        for (uint256 i = 0; i < supportedSymbols.length; i++) {
            if (keccak256(bytes(supportedSymbols[i])) == keccak256(bytes(_symbol))) {
                symbolExists = true;
                break;
            }
        }
        
        // Add symbol to supportedSymbols if it doesn't exist
        if (!symbolExists) {
            supportedSymbols.push(_symbol);
        }
        
        // Update rating
        ratings[_symbol] = Rating({
            symbol: _symbol,
            timestamp: block.timestamp,
            rating: _rating,
            technical: _technical,
            fundamental: _fundamental
        });
        
        emit RatingUpdated(_symbol, _rating, block.timestamp);
    }
    
    /**
     * @dev Get rating for a cryptocurrency
     * @param _symbol Token symbol (e.g., "BTC")
     * @return Rating struct
     */
    function getRating(string calldata _symbol) external view requireStake returns (Rating memory) {
        Rating memory rating = ratings[_symbol];
        require(rating.timestamp > 0, "TMOracle: rating not found");
        return rating;
    }
    
    /**
     * @dev Get technical score for a cryptocurrency
     * @param _symbol Token symbol (e.g., "BTC")
     * @return Technical score
     */
    function getTechnicalScore(string calldata _symbol) external view requireStake returns (uint256) {
        Rating memory rating = ratings[_symbol];
        require(rating.timestamp > 0, "TMOracle: rating not found");
        return rating.technical;
    }
    
    /**
     * @dev Get fundamental score for a cryptocurrency
     * @param _symbol Token symbol (e.g., "BTC")
     * @return Fundamental score
     */
    function getFundamentalScore(string calldata _symbol) external view requireStake returns (uint256) {
        Rating memory rating = ratings[_symbol];
        require(rating.timestamp > 0, "TMOracle: rating not found");
        return rating.fundamental;
    }
    
    /**
     * @dev Get all supported symbols
     * @return Array of supported symbols
     */
    function getAllSymbols() external view returns (string[] memory) {
        return supportedSymbols;
    }
}
