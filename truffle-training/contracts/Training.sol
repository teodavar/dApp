pragma solidity ^0.4.24;
import "./TokenERC20.sol";


contract Training {
    TokenERC20 private Ntua;

    // The trainer's address
    address public trainer;
    // The trainee's address
    address public traineeAddr;

    // The Request struct
    struct Request {
        string demotype;
        uint duration;
        uint number;
        uint rate;
        bool init;
        string demofile;
        uint reward_gained;
    }

    // The mapping to store the requests for demo
    mapping (uint => Request) public requests;

    // The sequence number of the requests for demo
    uint requestseq;


    // Event triggered when a new request for demo received

    event RequestSent(address trainee, string demotype, uint duration, uint requestno);

    // Event triggered when the trainer has evaluate the rate of the reward
    // for the requested demo
    event RateSent(address trainee, uint requestno, uint rate);

    // Event triggered when the trainer has prepared requested demo
    // demofile: contains the hash code provided by IPFS
    event DemoSent(address trainee, uint requestno, string demofile);

    // Event triggered when the trainee has completed the training
    event TrainingCompleted(address trainee, uint requestno, uint reward_gained);

    // Event triggered when the payment took place
    event PaymentCompleted(address trainee, address trainer, uint requestno, uint amount);

    // Constructor
    constructor(TokenERC20 _Ntua, address _traineeAddr) public payable {
        trainer = msg.sender;       // Trainer is the contract owner
        traineeAddr = _traineeAddr;
        Ntua = _Ntua;
    }

   // The function to query requests by its sequence number
    function queryRequest(uint number) constant public returns (uint duration, uint rate, string demofile, uint reward_gained ) {
        // Validate the request number
        require(requests[number].init);
        // Return the order data
        return(requests[number].duration,requests[number].rate, requests[number].demofile, requests[number].reward_gained);
    }


    // The function to request for Demo
    function requestDemo(string demotype, uint duration) public payable {
        // Accept requests only from trainee
        require(msg.sender == traineeAddr);
        // Increment the sequence number of requests
        requestseq++;
        // Update the requests list
        requests[requestseq] = Request(demotype, duration, requestseq, 0, true, "", 0);
        /// Trigger the event
        emit RequestSent(msg.sender, demotype, duration, requestseq);

    }

    // The function to send the rate to pay for the demo
    function sendRate(uint requestno, uint rate) public payable {
        // Only the trainer can use this function
        require(msg.sender == trainer);
        /// Validate the request number
        require(requests[requestno].init);
        requests[requestno].rate = rate;
        /// Trigger the event
        emit RateSent(traineeAddr, requestno, rate);
    }

    // The function to send the rate to pay for the demo
    function sendDemo(uint requestno, string demofile) public payable {
        // Only the trainer can use this function
        require(msg.sender == trainer);
        /// Validate the request number
        require(requests[requestno].init);
        requests[requestno].demofile = demofile;
        /// Trigger the event
        emit DemoSent(traineeAddr, requestno, demofile);
    }

    // The function to inform that the training has completed
    function trainingCompleted(uint requestno, uint reward_gained) public payable {
        // Accept requests only from trainee
        require(msg.sender == traineeAddr);
                /// Validate the request number
        require(requests[requestno].init);
        // Update the requests list
        requests[requestseq].reward_gained = reward_gained;

        // Trigger the event
        emit TrainingCompleted(traineeAddr, requestseq, reward_gained);
    }


    // The function to inform that the training has completed
    function safePay(uint requestno, uint reward_gained) public payable {
        // Accept requests only from trainee
        require(msg.sender == traineeAddr);
                /// Validate the request number
        require(requests[requestno].init);
        // Update the requests list
        
        uint amount = reward_gained * requests[requestno].rate * 10 ** 4;

        // Training contract should ask from ERC20 Token to perform the transaction
        //Ntua.transferFrom(msg.sender, trainer, amount);
        //require(Ntua.transferFrom(msg.sender, address(this), amount));
        require(Ntua.transferFrom(msg.sender, trainer, amount));

        // Trigger the event
        emit PaymentCompleted(traineeAddr, trainer, requestseq, amount);
    }


    // _value: holds the amount approved by trainee
    // _extraData: holds the reward_gained by trainee
    function receiveApproval(address _sender,
                         uint256 _value,
                         TokenERC20 _tokenContract,
                         bytes _extraData) public {
        require(Ntua == _tokenContract);
        // the _extraData is passed as bytes
        // decode the value according
        uint256 payloadSize;
        uint256 reward_gained;
        uint256 amount;
        assembly {
            payloadSize := mload(_extraData)
            reward_gained := mload(add(_extraData, 0x20))
        }
        reward_gained = reward_gained >> 8*(32 - payloadSize);
        //requests[requestseq].reward_gained = reward_gained;
        require(requests[requestseq].reward_gained == reward_gained);

        amount = requests[requestseq].rate * reward_gained * 10 ** 4;
        require(_value == amount);

        require(_tokenContract.transferFrom(_sender, address(this), _value));
        // Trigger the event
        emit PaymentCompleted(traineeAddr, trainer, requestseq, _value);

    }
}