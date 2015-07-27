BASE_URL = "../"

var getAdviceCode = CodeMirror.fromTextArea($("#getAdviceText").get(0),{
    lineNumbers: true,
    mode:"python"});

var setRewardCode = CodeMirror.fromTextArea($("#setRewardText").get(0),{
    lineNumbers: true,
    mode:"python"});

// Post a new experiment to the server:
$( "#CreateButton" ).click(function() {
    name = $("#nameOfExperiment").val(); 
    code1 = getAdviceCode.getValue(); 
    code2 = setRewardCode.getValue();
    adviceId = true;
    hourly = false;

    $.post( BASE_URL+"admin/exp/add.json", { 
        name: name, 
        getaction: code1,
        setreward: code2,
        adviceid: adviceId,
        hourly: hourly
        })
        .done(function( data ) {
            // pretty ugly, but hey ;)
            location.reload();
      });                              
});

// Edit experiment
function editExperiment(id){
    // First get the code
    $.getJSON( BASE_URL+"admin/exp/"+id+"/get.json", function( data ){
        console.log(data)
        // Populate
        $("#nameOfExperiment").val(data.name)
        getAdviceCode.setValue(data.getAction);  
        setRewardCode.setValue(data.setReward);
    }); 

    // Change the button
    $("#CreateButton").html("Store as new")
    $('#EditButton').show();

    // Set the handler:
    $( "#EditButton").click(function() {

        name = $("#nameOfExperiment").val(); 
        code1 = getAdviceCode.getValue(); 
        code2 = setRewardCode.getValue();
        adviceId = true;
        hourly = false;

        // Edit the experiment:
        $.post( BASE_URL+"admin/exp/"+id+"/edit.json", { 
            name: name, 
            getaction: code1,
            setreward: code2,
            adviceid: adviceId,
            hourly: hourly
        })
        .done(function( data ) {
            // pretty ugly, but hey ;)
            location.reload();
         });    
    });
}

// Get the list of experiments:
$(document).ready(function() {
    $('#EditButton').hide();
    console.log( "ready!" );

    // Get the JSON blob with all experiments:
    $.getJSON( BASE_URL+"admin/exp/list.json", function( data ) {
        console.log(data)
        var items = [];
        $.each(data, function(key, val){
            items.push('<li>' + key + ': ' + val.name + ' (<a href="#" onclick="editExperiment('+key+')">edit</a>)</li>');
        });  
        $('#experimentsList').append( items.join('') );                  
    })
    .fail(function() {
        console.log( "error" );
      });

});

// Load default experiments
function loadDefaults(){
    alert("Loading defaults")
}
