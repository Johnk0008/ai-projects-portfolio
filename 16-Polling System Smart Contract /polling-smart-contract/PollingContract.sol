// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PollingSystem {
    // Poll structure
    struct Poll {
        string title;
        string[] options;
        uint256 endTime;
        bool exists;
        mapping(address => bool) hasVoted;
        mapping(uint256 => uint256) votes; // optionIndex -> voteCount
    }
    
    // State variables
    mapping(uint256 => Poll) public polls;
    uint256 public pollCount;
    address public owner;
    
    // Events
    event PollCreated(uint256 pollId, string title, uint256 endTime);
    event VoteCast(uint256 pollId, address voter, uint256 optionIndex);
    event WinnerDeclared(uint256 pollId, uint256 winningOption, string optionName);
    
    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action");
        _;
    }
    
    modifier pollExists(uint256 _pollId) {
        require(_pollId < pollCount && polls[_pollId].exists, "Poll does not exist");
        _;
    }
    
    modifier votingOpen(uint256 _pollId) {
        require(block.timestamp < polls[_pollId].endTime, "Voting has ended");
        _;
    }
    
    constructor() {
        owner = msg.sender;
        pollCount = 0;
    }
    
    // Create a new poll
    function createPoll(
        string memory _title,
        string[] memory _options,
        uint256 _durationInMinutes
    ) public onlyOwner returns (uint256) {
        require(_options.length >= 2, "At least 2 options required");
        require(_durationInMinutes > 0, "Duration must be positive");
        
        uint256 pollId = pollCount;
        Poll storage newPoll = polls[pollId];
        
        newPoll.title = _title;
        newPoll.endTime = block.timestamp + (_durationInMinutes * 1 minutes);
        newPoll.exists = true;
        
        // Copy options array
        for (uint256 i = 0; i < _options.length; i++) {
            newPoll.options.push(_options[i]);
        }
        
        pollCount++;
        emit PollCreated(pollId, _title, newPoll.endTime);
        return pollId;
    }
    
    // Vote in a poll
    function vote(uint256 _pollId, uint256 _optionIndex) 
        public 
        pollExists(_pollId)
        votingOpen(_pollId)
    {
        Poll storage poll = polls[_pollId];
        
        require(!poll.hasVoted[msg.sender], "Already voted in this poll");
        require(_optionIndex < poll.options.length, "Invalid option index");
        
        poll.hasVoted[msg.sender] = true;
        poll.votes[_optionIndex]++;
        
        emit VoteCast(_pollId, msg.sender, _optionIndex);
    }
    
    // Get current vote count for an option
    function getVotes(uint256 _pollId, uint256 _optionIndex) 
        public 
        view 
        pollExists(_pollId)
        returns (uint256)
    {
        require(_optionIndex < polls[_pollId].options.length, "Invalid option index");
        return polls[_pollId].votes[_optionIndex];
    }
    
    // Get poll details
    function getPollDetails(uint256 _pollId)
        public
        view
        pollExists(_pollId)
        returns (
            string memory title,
            string[] memory options,
            uint256 endTime,
            bool isActive
        )
    {
        Poll storage poll = polls[_pollId];
        return (
            poll.title,
            poll.options,
            poll.endTime,
            block.timestamp < poll.endTime
        );
    }
    
    // Determine and return winning option
    function getWinningOption(uint256 _pollId)
        public
        view
        pollExists(_pollId)
        returns (uint256 winningOption, string memory optionName, uint256 voteCount)
    {
        Poll storage poll = polls[_pollId];
        require(block.timestamp >= poll.endTime, "Voting still in progress");
        
        uint256 maxVotes = 0;
        uint256 winningIndex = 0;
        bool hasTie = false;
        
        for (uint256 i = 0; i < poll.options.length; i++) {
            if (poll.votes[i] > maxVotes) {
                maxVotes = poll.votes[i];
                winningIndex = i;
                hasTie = false;
            } else if (poll.votes[i] == maxVotes && maxVotes > 0) {
                hasTie = true;
            }
        }
        
        require(!hasTie || maxVotes > 0, "No votes cast or tie detected");
        
        return (
            winningIndex,
            poll.options[winningIndex],
            maxVotes
        );
    }
    
    // Check if user has voted in a poll
    function hasUserVoted(uint256 _pollId, address _user) 
        public 
        view 
        pollExists(_pollId)
        returns (bool)
    {
        return polls[_pollId].hasVoted[_user];
    }
    
    // Get total votes in a poll
    function getTotalVotes(uint256 _pollId)
        public
        view
        pollExists(_pollId)
        returns (uint256 total)
    {
        Poll storage poll = polls[_pollId];
        for (uint256 i = 0; i < poll.options.length; i++) {
            total += poll.votes[i];
        }
        return total;
    }
}