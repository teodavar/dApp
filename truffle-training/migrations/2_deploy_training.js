
var TokenERC20 = artifacts.require("TokenERC20");
var Training = artifacts.require("./Training.sol");

module.exports = function(deployer, network, accounts) {

    // Deploy the TokenERC20 contract
    deployer.deploy(TokenERC20, "10000", "NtuaToken", "NtuaTok")
        // Wait until the TokenERC20 contract is deployed
        .then(() => TokenERC20.deployed())
        // Deploy the Training contract, while passing the address of the
        // TokenERC20 contract
        .then(() => deployer.deploy(Training, TokenERC20.address, accounts[9]));
}


