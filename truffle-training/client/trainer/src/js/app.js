App = {
  web3Provider: null,
  contracts: {},
  balance: 0,
  trainer_private_key: "76164252b7a76d08d18ed7a68142632bc385352af01ae041f9fb7cb5e2c56037",
  trainer: "0x5386aCc4c29E5Dd07842bBE5324590BE95FEf66C",
  demoId: 0,
  demoType: null,
  demoCount:0,
  demoFile: null,
  requestNo: 0,
  demoHash: null,
  rate: 4,
  reward_gained: 0,
  credit_amount: 0,

  ipfs : window.IpfsHttpClient('ipfs.infura.io', '5001', { protocol: 'https' }),

  init: async function() {
    // Load available demos
    $.getJSON('../demos.json', function(data) {
      App.demoCount = data.length

      var demosRow = $('#TrainerDemosRow');
      var demoTemplate = $('#demoTemplate');

      for (i = 0; i < data.length; i ++) {
        demoTemplate.find('.panel-title').text(data[i].name);
        demoTemplate.find('img').attr('src', data[i].picture);
        demoTemplate.find('.agent-agent').text(data[i].agent);
        demoTemplate.find('.agent-goal').text(data[i].goal);
        demoTemplate.find('.btn-send-rate').attr('disabled', true);
        demoTemplate.find('.btn-primary').attr('disabled', true);
        demoTemplate.find('.btn-send-demo').attr('disabled', true);
        demoTemplate.find('.reward-gained').attr('disabled', true);
        demoTemplate.find('.amount').attr('disabled', true);
        
        demosRow.append(demoTemplate.html());
      }
    });

    return await App.initWeb3();
  },

  // Trainer
  initWeb3: async function() {
    App.web3Provider = new Web3.providers.HttpProvider('http://localhost:7545');
    web3 = new Web3(App.web3Provider);
    return App.initContracts();
  },

  // Trainer
  initContracts: function() {
    $.getJSON('Training.json', function(data) {
      // Get the necessary contract artifact file and instantiate it with truffle-contract
      var TrainingArtifact = data;
      App.contracts.Training = TruffleContract(TrainingArtifact);
    
      // Set the provider for our contract
      App.contracts.Training.setProvider(App.web3Provider);
    
      App.listenForTrainingEvents(); 

    });
    $.getJSON('TokenERC20.json', function(data) {
      // Get the necessary contract artifact file and instantiate it with truffle-contract
      var TokenArtifact = data;
      App.contracts.Token = TruffleContract(TokenArtifact);
    
      // Set the provider for our contract
      App.contracts.Token.setProvider(App.web3Provider);
    
      App.listenForTokenEvents(); 
      return App.showTrainerData();
      return
    });

       
    return App.bindEvents();
  },

  // Trainer
  bindEvents: function() {
    $(document).on('click', '.btn-send-rate', App.sendRate);
    $(document).on('click', '.btn-primary', App.uploadDemoToIPFS);
    $(document).on('click', '.btn-send-demo', App.sendDemo);
  },

  /* Trainer listens for the following event:
    RequestSent_filter = training_contract.events.RequestSent.createFilter(fromBlock='latest')
    TrainingCompleted_filter = training_contract.events.TrainingCompleted.createFilter(fromBlock='latest')
    
  */

  // Trainer
  // Listen for events emitted from the Training contract
  listenForTrainingEvents: function() {
    App.contracts.Training.deployed().then(function(instance) {

      instance.RequestSent({}, {
        fromBlock: 'latest'
      }).watch(function(error, event) {
        console.log("RequestSent event triggered", event)
        console.log("Demotype: ", event.args.demotype)
        App.demotype = event.args.demotype
        if (event.args.demotype === 'Pyramids') { 
          App.demoId = 1
        }
        else if (event.args.demotype === 'Crawler') {
          App.demoId = 2
        }
        else {
          App.demoId = 0
        }
        console.log("Demoid: ", App.demoId)
        console.log("Requestno: ", event.args.requestno.c[0])
        App.requestNo = event.args.requestno.c[0]
        $("#trainerStatus").html("Agent Status: RequestSent event received");
        $('.panel-demo').eq(App.demoId).find('.btn-send-rate').attr('disabled', false);
        
        // Reload when a new vote is recorded
        // App.render();
      });

      instance.TrainingCompleted({}, {
        fromBlock: 'latest'
      }).watch(function(error, event) {
        console.log("TrainingCompleted event triggered !!!!", event)
        console.log("Requestno: ", event.args.requestno)
        $("#trainerStatus").html("Agent Status: TrainingCompleted event received");
        $('.panel-demo').eq(App.demoId).find('.reward-gained').attr('disabled', false);
        $('.panel-demo').eq(App.demoId).find('.amount').attr('disabled', false);
        App.reward_gained = event.args.reward_gained.c[0]
        reward_txt = "Reward gained: " + event.args.reward_gained.c[0]
        $("#reward-gained").html(reward_txt);
        App.credit_amount = App.reward_gained * App.rate * 10**4 ;
        amount_txt = "Amount (to be CREDITED): " + App.credit_amount;
        $("#amount").html(amount_txt);
      });

      instance.PaymentCompleted({}, {
        fromBlock: 'latest'
      }).watch(function(error, event) {
        console.log("PaymentCompleted event triggered", event)
        console.log("Requestno: ", event.args.requestno.c[0])
        console.log("Amount credited: ", event.args.amount.c[0])
        $("#trainerStatus").html("Agent Status: Payment Completed successfully!!");
        // Show new Balance
        App.contracts.Token.deployed().then(function(instance) {
          tokenInstance = instance;
          return tokenInstance.balanceOf(App.trainee);
        }).then(function(balance) {
          console.log("BALANCE: ", balance.c[0])
          App.balance = balance
          $("#traineeBalance").html("Your Balance (in Ntua): " + App.balance);
        }).catch(function(err) {
          console.log(err.message);
        });
      });
    });

  },

  listenForTokenEvents: function() {
    App.contracts.Token.deployed().then(function(instance) {
      instance.Transfer({}, {
        fromBlock: 'latest'
      }).watch(function(error, event) {
        console.log("Transfer event triggered", event)
        console.log("Amount credited: ", event.args.value.c[0])
        $("#trainerStatus").html("Agent Status: Transfer event received");
        // Reload when a new vote is recorded
        // App.render();
      });   
    });

  },

  // Trainer
  showTrainerData: function() {
    console.log("XXXXXXXXXXXX")
    $("#trainerAddress").html("Your Account: " + App.trainer);
    $("#trainerStatus").html("Agent Status: Inactive");
    App.contracts.Token.deployed().then(function(instance) {
      tokenInstance = instance;
      return tokenInstance.balanceOf(App.trainer);
    }).then(function(balance) {
      App.balance = balance
      console.log("BALANCE: ", balance.toString())
      $("#trainerBalance").html("Your Balance (in Ntua): " + App.balance.toString());
    }).catch(function(err) {
      console.log(err.message);
    });
    
  },

  //Trainer
  markRateSent: function() {
    console.log("in markRateSent with demo ID: ", App.demoId)
    // Activate the 'Send Demo' button 
    $('.panel-demo').eq(App.demoId).find('.btn-primary').attr('disabled', false);
    $('.panel-demo').eq(App.demoId).find('.btn-send-rate').attr('disabled', true);

  },

  // Trainer
  sendRate: function(event) {
    event.preventDefault();
    console.log("in sentRate")
    
    App.contracts.Training.deployed().then(function(instance) {
        trainingInstance = instance;    
        return trainingInstance.sendRate(App.requestNo, App.rate, {from: App.trainer});
      }).then(function(result) {

        return App.markRateSent();
      }).catch(function(err) {
        console.log(err.message);
      });  
  },

    // Trainer
    sendDemo: function(event) {
      event.preventDefault();
      console.log("in sendDemo")
      
      App.contracts.Training.deployed().then(function(instance) {
        trainingInstance = instance;    
        return trainingInstance.sendDemo(App.requestNo, App.demoHash, {from: App.trainer});
      }).then(function(result) {
        $("#trainerStatus").html("Agent Status: sendDemo request sent");
        $('.panel-demo').eq(App.demoId).find('.upload-file').attr('disabled', true);
        $('.panel-demo').eq(App.demoId).find('.btn-send-demo').attr('disabled', true);
        // return App.markRateSent();
      }).catch(function(err) {
        console.log(err.message);
      }); 
    },

    // Trainer
    uploadDemoToIPFS: function(event) {
      event.preventDefault();
      console.log("in uploadDemoToIPFS")
      console.log("demoId: ", App.demoId)

      $("#upload-file").on("change", function() {
        console.log("YYYYYYYYYYYYYYYYYYYYY")
        var reader = new FileReader();
        reader.onload = function (e) {

            const magic_array_buffer_converted_to_buffer = buffer.Buffer(reader.result);
            App.ipfs.add(magic_array_buffer_converted_to_buffer, (err, ipfsHash) => {
                console.log(err,ipfsHash);
                console.log("IPFS Hash: ", ipfsHash[0].path);
                App.demoHash = ipfsHash[0].path;
                $('.panel-demo').eq(App.demoId).find('.ipfs-hash').text(ipfsHash[0].path);
                $('.panel-demo').eq(App.demoId).find('.btn-send-demo').attr('disabled', false);
                  
            })
        }
        reader.readAsArrayBuffer(this.files[0]);
      })


    }

};

$(function() {
  $(window).load(function() {
    App.init();
  });
});
