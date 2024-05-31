// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

contract RootAISecToken is ERC20, ReentrancyGuard {
    uint256 public constant REWARD_AMOUNT = 10 * 10**18; // 10 tokens
    address creator;
    address[] public adminList; // Array to keep track of admin addresses
    mapping(address => bool) public admins;

    event TokensRewarded(address indexed user, uint256 amount);
    event GuideUploaded(address indexed researcher, string guideHash);
    event AuditRequested(address indexed user, string contractHash);

    modifier onlyCreator() {
        require(msg.sender == creator, "Only creator can call this function");
        _;
    }

    modifier onlyAdmin() {
        require(admins[msg.sender], "Only admins can call this function");
        _;
    }

    constructor(uint256 initialSupply) ERC20("RootAISecToken", "RAS") {
        _mint(msg.sender, initialSupply); // Mint initial supply of tokens to contract deployer
        creator = msg.sender;
        admins[msg.sender] = true;
        adminList.push(msg.sender);
        _mint(address(this), 1000000000 * 10**18); // Mint 1 billion tokens to the contract for rewards
    }

    function mint(address to, uint256 amount) external onlyAdmin {
        _mint(to, amount);
    }


    function addAdmin(address admin) external onlyCreator {
        require(!admins[admin], "Address is already an admin");
        admins[admin] = true;
        adminList.push(admin);
    }

    function listAdmins() external view returns (address[] memory) {
        return adminList;
    }


    function uploadGuide(string memory guideHash) external nonReentrant {
        // Assuming guideHash is a hash of the uploaded guide
        emit GuideUploaded(msg.sender, guideHash);
    }


    function requestAudit(string memory contractHash) external nonReentrant {
        // Assuming contractHash is a hash of the smart contract to be audited
        emit AuditRequested(msg.sender, contractHash);
    }

    function rewardTokens(address recipient, uint256 amount) external nonReentrant onlyAdmin {
        require(balanceOf(address(this)) >= amount * 10 ** 18, "Insufficient balance in the contract to reward");
        _transfer(address(this), recipient, amount * 10 ** 18);
        emit TokensRewarded(recipient, amount * 10 ** 18);
    }

    // Function to validate uploaded guides or prompts (stub for AI validation logic)
    function validateGuideOrPrompt(string memory dataHash) external pure returns (bool) {
        // Replace with actual validation logic
        return keccak256(abi.encodePacked(dataHash)) != keccak256(abi.encodePacked(""));
    }
}
