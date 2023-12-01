App = {
  web3Provider: null,
  contracts: {},
  balance: 0,
  trainee_private_key: "7ba69ecf88e8a56356a29f166bf87a2aece8fac2aa1ffbee459a1258dda1ec72",
  trainee: "0x080C0B5E15FA20f520e27C6C9ebDd59cc7d20f02",
  demoId: 0,
  demoDuration: 1,
  demoEnvironment: "default",
  demoType: null,
  demoCount:0,
  demoFile: null,
  demoHash: null,
  requestNo: 0,
  waitForDemo: false,
  rate: 0,
  reward_gained: 0,
  debit_amount: 0,
  training_contract: null,

  init: async function() {
    // Load available demos
    $.getJSON('../demos.json', function(data) {
      App.demoCount = data.length

      var demosRow = $('#TraineeDemosRow');
      var demoTemplate = $('#demoTemplate');

      for (i = 0; i < data.length; i ++) {
        demoTemplate.find('.panel-title').text(data[i].name);
        demoTemplate.find('img').attr('src', data[i].picture);
        demoTemplate.find('.agent-agent').text(data[i].agent);
        demoTemplate.find('.agent-goal').text(data[i].goal);
        demoTemplate.find('.btn-request-demo').attr('data-id', data[i].id);
        demoTemplate.find('.btn-download-demo').attr('disabled', true);
        demoTemplate.find('.btn-pay').attr('disabled', true);
        demoTemplate.find('.ipfs-hash').attr('disabled', true);
        demoTemplate.find('.reward-gained').attr('disabled', true);
        demoTemplate.find('.amount').attr('disabled', true);

        demosRow.append(demoTemplate.html());
      }
    });

    return await App.initWeb3();
  },

  initWeb3: async function() {

    App.web3Provider = new Web3.providers.HttpProvider('http://localhost:7545');

    web3 = new Web3(App.web3Provider);

    return App.initContracts();
  },

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
      return App.showTraineeData();
    });

       // Listens for contract events
    return App.bindEvents();
  },

  bindEvents: function() {
    $(document).on('click', '.btn-request-demo', App.requestDemo);
    $(document).on('click', '.btn-download-demo', App.downloadDemo);
    $(document).on('click', '.btn-pay', App.approveAndPay);
  },

  /* Trainee listens for the following events:
  RateSent_filter = training_contract.events.RateSent.createFilter(fromBlock='latest')
  DemoSent_filter = training_contract.events.DemoSent.createFilter(fromBlock='latest')
  */

  // Listen for events emitted from the Training contract
  listenForTrainingEvents: function() {
    App.contracts.Training.deployed().then(function(instance) {

      instance.DemoSent({}, {
        fromBlock: 'latest'
      }).watch(function(error, event) {
        if (App.waitForDemo) {
            console.log("DemoSent event triggered!", event)
            console.log("DemoHash: ", event.args.demofile)
            App.demoHash = event.args.demofile
            console.log("Requestno: ", event.args.requestno.c[0])
            $('.panel-demo').eq(App.demoId).find('.ipfs-hash').text(App.demoHash);
            $("#traineeStatus").html("Agent Status: DemoSent event received");
            $('.panel-demo').eq(App.demoId).find('.btn-download-demo').attr('disabled', false);

        }
      });

      instance.RateSent({}, {
        fromBlock: 'latest'
      }).watch(function(error, event) {
        console.log("RateSent event triggered", event)
        console.log("Requestno: ", event.args.requestno.c[0])
        App.requestNo = event.args.requestno.c[0]
        console.log("Rate: ", event.args.rate)
        App.waitForDemo = true
        App.rate = event.args.rate
        $("#traineeStatus").html("Agent Status: RateSent event received");
        // Reload when a new vote is recorded
        // App.render();
      });

      instance.TrainingCompleted({}, {
        fromBlock: 'latest'
      }).watch(function(error, event) {
        console.log("TrainingCompleted event triggered", event)
        console.log("Requestno: ", event.args.requestno.c[0])
        App.requestNo = event.args.requestno.c[0]
        $("#traineeStatus").html("Agent Status: TrainingCompleted event received");
        $('.panel-demo').eq(App.demoId).find('.btn-pay').attr('disabled', false);
        $('.panel-demo').eq(App.demoId).find('.reward-gained').attr('disabled', false);
        $('.panel-demo').eq(App.demoId).find('.amount').attr('disabled', false);
        App.reward_gained = event.args.reward_gained.c[0]
        reward_txt = "Reward gained: " + event.args.reward_gained.c[0]
        $("#reward-gained").html(reward_txt);
        App.debit_amount = App.reward_gained * App.rate * 10**4
        amount_txt = "Amount (to be DEBITED): " + App.debit_amount
        $("#amount").html(amount_txt);

        // Reload when a new vote is recorded
        // App.render();
      });

      instance.PaymentCompleted({}, {
        fromBlock: 'latest'
      }).watch(function(error, event) {
        console.log("PaymentCompleted event triggered", event)
        console.log("Requestno: ", event.args.requestno.c[0])
        console.log("Amount debited: ", event.args.amount.c[0])
        $("#traineeStatus").html("Agent Status: Payment Completed successfully!!");
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
        // Activate all 'RequestDemo' buttons
        for (i = 0; i < App.demoCount; i++) {
          $('.panel-demo').eq(i).find('btn-request-demo').attr('disabled', false);
        }
      });
    });
  },

  // Listen for events emitted from the token contract
  listenForTokenEvents: function() {
    App.contracts.Token.deployed().then(function(instance) {
      instance.Transfer({}, {
        fromBlock: 'latest'
      }).watch(function(error, event) {
        console.log("Transfer event triggered", event)
        console.log("Amount debited: ", event.args.value.c[0])

        $("#traineeStatus").html("Agent Status: Transfer has been approved!!");
        // Reload when a new vote is recorded
        // App.render();
      });
    });
  },

  showTraineeData: function() {
    console.log("XXXXXXXXXXXX")
    $("#traineeAddress").html("Your Account: " + App.trainee);
    $("#traineeStatus").html("Agent Status: Inactive");
    App.contracts.Token.deployed().then(function(instance) {
      tokenInstance = instance;
      return tokenInstance.balanceOf(App.trainee);
    }).then(function(balance) {
      console.log("TRAINEE: ", App.trainee)
      console.log("BALANCE: ", balance.c[0])
      App.balance = balance
      $("#traineeBalance").html("Your Balance (in Ntua): " + App.balance);
    }).catch(function(err) {
      console.log(err.message);
    });
    
  },

  markRequested: function() {
    console.log("in markRequested")
    // Inactivate all 'RequestDemo' buttons util the completion of the current training
    for (i = 0; i < App.demoCount; i++) {
      $('.panel-demo').eq(i).find('button').attr('disabled', true);
    }
  },


  downloadDemo: function(event) {
    event.preventDefault();
    console.log("in downloadDemo with RequestNo: ", App.requestNo)

    var data = {'demohash': App.demoHash, 'requestno': App.requestNo}
    fetch("http://localhost:5200/start_training", {
              method: "post",
              body: JSON.stringify(data)
            })
            .then(response => {
              $('.panel-demo').eq(App.demoId).find('.btn-download-demo').attr('disabled', true);
              console.log("OKKKKKKKKKKKKKKK");
              })
            .catch(error => console.error(error));
  },

  
  approveAndPay: function(event) {
    event.preventDefault();
    console.log("in approveAndPay !!!!!!!!!")
    // Solution A - two fold payment : a) approve and b) safePay
    // a) approve the Payment
    $('.panel-demo').eq(App.demoId).find('.btn-pay').attr('disabled', true);
    
    App.contracts.Token.deployed().then(function(instance) {
      tokenInstance = instance;
      console.log("Training contract address:", App.training_contract)
      return tokenInstance.approve(App.training_contract, App.debit_amount, {from: App.trainee});
    }).then(function(result) {
        // b) perform SafePay

        App.contracts.Training.deployed().then(function(instance) {
          trainingInstance = instance;      
          return trainingInstance.safePay(App.requestNo, App.reward_gained, {from: App.trainee});
        }).then(function(result) {
        }).catch(function(err) {
          console.log(err.message);
        });
    }).catch(function(err) {
      console.log(err.message);
    });
    

  },

  requestDemo: function(event) {
    event.preventDefault();
    console.log("in requestDemo !!!!!!!!!")
    App.demoId = parseInt($(event.target).data('id'));
    console.log("demoId: ", App.demoId)
    var trainingInstance;
    if (App.demoId === 1)
      App.demoType = 'Pyramids'
    else if (App.demoId === 2)
      App.demoType = 'Crawler'
    else 
      App.demoType = 'Hummingbird'
    console.log("demoType: ", App.demoType)

    // Dynamically populate a dropdown list from a json file
    // https://www.encodedna.com/jquery/dynamically-bind-populate-select-element-with-json-data-using-jquery-ajax.htm
    
    App.demoEnvironment = $('.panel-demo').eq(App.demoId).find('#environment option:selected').val()
    console.log("Selected environment is: ", App.demoEnvironment)
    App.demoDuration = $('.panel-demo').eq(App.demoId).find('#duration option:selected').val()
    console.log("Selected duration is: ", App.demoDuration)
    
    App.contracts.Training.deployed().then(function(instance) {
        trainingInstance = instance;      
        App.training_contract = trainingInstance.address
        console.log("Training address: ", App.training_contract)
        //demoDuration = 4
        return trainingInstance.requestDemo(App.demoType, App.demoDuration, {from: App.trainee, gas:300000});
      }).then(function(result) {

        return App.markRequested();
      }).catch(function(err) {
        console.log(err.message);
      });
    
    
  }

};

$(function() {
  $(window).load(function() {
    App.init();
  });
});
