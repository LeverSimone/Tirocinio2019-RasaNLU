$(function () {

  Handlebars.registerHelper('times', function(n, block) {
    var accum = '';
    for(var i = 0; i < n; ++i)
        accum += block.fn(i);
    return accum;
  });
  
  Handlebars.registerHelper('formatNum', function (num) {
    return num == 0 ? 0 : Math.round(num * 100) / 100
  });

  Handlebars.registerHelper('formatPerc', function (num, dec) {
    dec = dec === undefined ? 2 : dec
    return (Math.round(num * 100 * (10 ** dec)) / (10 ** dec))
  });
  
  Handlebars.registerHelper('isEq', function (a, b) {
    return a == b;
  });
  
  Handlebars.registerHelper('formatDate', function (date) {
    date = new Date(date);
    return date.toLocaleDateString();
  });
  
  Handlebars.registerHelper('formatTime', function (date) {
    date = new Date(date);
    return date.toLocaleTimeString().
      replace(/([\d]+:[\d]{2})(:[\d]{2})(.*)/, "$1$3");
  });  

  Handlebars.registerHelper('toLowerCase', function (str) {
    return str.toLowerCase()
  });

  Handlebars.registerHelper('likert', function (label, score) {
    var tmpl = Handlebars.compile($("#likert-template").html())
    return tmpl({
      label: label,
      score: score,
      class: score.toLowerCase()
    })
  });
  
  Handlebars.registerHelper('displayAnnotations', function (data, type) {
      // look at the data type, and based on that the template
      if (type == "image") {
        var tmpl = Handlebars.compile($("#message-vision-template").html())
        msg = tmpl({annotations : data})
      } else {
        var tmpl = Handlebars.compile($("#message-nlp-template").html())
        msg = tmpl({aspects : data})
      }
      return msg;
  });  
  
  var CONF_ID = null;
  
  var processMessage = function(msg, cb){
    
    $.get("/parse?q="+ msg + "&conf=" + CONF_ID, function (data) {
      cb.done(data);
    });    
    
         
  };
  
  var configurePage = function(config, cb){
    
    console.log(config);
    
    $.ajax({
        url: "/configure",
        type: 'POST',
        contentType: 'application/json',
        data : JSON.stringify(config),
        success: function(data){
          cb.done(data);                    
        },
        error: function(){
          console.log("Error configuring page");
          cb.error();
        }
    });      
  };
  
  
  $('.testing').on("keydown", "textarea", function (event) {
    var keypressed = event.keyCode || event.which;
    if (keypressed == 13) {
      event.preventDefault();
      
      var msg = $("#test-message").val();
      var $el = $(this);

      $el.attr("disabled", ""); 
      $("#test-message").val('');
      processMessage(msg, {
        done : function(data){
          var tmpl = Handlebars.compile($("#nlu-template").html());
          var el = tmpl({
                          message : data.text,
                          entities : data.entities,
                          intent : data.intent.name,
                          matching : data.matching,
                          matching_failed : data.matching_failed,
                    
                        });        

          $(".testing .test-results").prepend(el);
          $el.removeAttr("disabled");
          $el.focus();

        },
        error : function(){
        }      
      });    
    }
  });
  
  
  $('.testing').on("click", "button", function (event) {
    
    var config = {
      intents : JSON.parse($("#test-config").val())
    };
    
    configurePage(config, {
      done : function(data){
        CONF_ID = data.id;
        
        $(".card-message").show();
        $(".card-config").hide();
      }, 
      error : function(){
        console.error("Error configure page");
      }
    });           
  }); 
  
  
  
  var renderSandbox = function(){
    var tmpl = Handlebars.compile($("#training-template").html());
    var el = tmpl({});
    $(".testing").html(el);  
    $(".card-message").hide();    
  };
  
  
  
  renderSandbox();
  

});