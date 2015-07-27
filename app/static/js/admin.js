BASE_URL = "../"
CURR_ID = 0

var getAdviceCode = CodeMirror.fromTextArea($("#getAdviceText").get(0),{
    lineNumbers: true,
    mode:"python"});

var setRewardCode = CodeMirror.fromTextArea($("#setRewardText").get(0),{
    lineNumbers: true,
    mode:"python"});

// Post a new experiment to the server:
$( "#CreateButton").click(function() {
    name = $("#nameOfExperiment").val(); 
    code1 = getAdviceCode.getValue(); 
    code2 = setRewardCode.getValue();

    $.post( BASE_URL+"admin/exp/add.json", { 
        name: name, 
        getaction: code1,
        setreward: code2
        })
        .done(function( data ) {
            // pretty ugly, but hey ;)
            location.reload();
      });                              
});

$( "#EditButton").click(function() {

    name = $("#nameOfExperiment").val(); 
    code1 = getAdviceCode.getValue(); 
    code2 = setRewardCode.getValue();

    if(CURR_ID != 0){
    $.post( BASE_URL+"admin/exp/"+CURR_ID+"/edit.json", { 
        name: name, 
        getaction: code1,
        setreward: code2
    })
    .done(function( data ) {
        // pretty ugly, but hey ;)
        location.reload();
     }); 
    }   
});

// Edit experiment
function editExperiment(id){

    CURR_ID = id  
    $.getJSON(BASE_URL+"admin/exp/"+id+"/get.json", function( data ){
        $("#nameOfExperiment").val(data.name)
        getAdviceCode.setValue(data.getAction);  
        setRewardCode.setValue(data.setReward);
    }); 

    $("#CreateButton").html("Store as new")
    $('#EditButton').show();
}

function deleteExperiment(id){
    $.getJSON(BASE_URL+"admin/exp/"+id+"/delete.json", function( data ){
        location.reload();
    });
}

// Get the list of experiments:
$(document).ready(function() {
    $('#EditButton').hide();

    // Get the JSON blob with all experiments:
    $.getJSON( BASE_URL+"admin/exp/list.json", function( data ) {
        console.log(data)
        $.each(data, function(key, val){
            $('#ExperimentsList > tbody:last-child').append('<tr><th scope="row">'+key+'</th><th>'+val.name+'</th><th>(<a href="#" onclick="editExperiment('+key+')">edit</a>)</th><th>(<a href="#" onclick="deleteExperiment('+key+')">delete</a>)</th></tr>');
        });          
    })
    .fail(function() {
        console.log( "error" );
      });

    $.getJSON( BASE_URL+"admin/exp/defaults.json", function( data ){
        console.log(data)
        $.each(data["defaults"], function(key, val){
            $( '#DefaultList' ).append( '<button type="button" onclick="loadDefault('+key+')" class="btn btn-lg btn-primary">'+val.name+'</button> \n' )
        })
    })

});



// Load default experiments
function loadDefault(id){
    $.getJSON( BASE_URL+"admin/exp/default/"+id+"/get.json", function( data ) {
        $("#nameOfExperiment").val(data.name)
        getAdviceCode.setValue(data.getAction);  
        setRewardCode.setValue(data.setReward);
    })
}
