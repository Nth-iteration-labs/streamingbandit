BASE_URL = "../";
API_URL = "http://localhost:8080";
CURR_ID = 0;

var getAdviceCode ;
var setRewardCode;
// Post a new experiment to the server:
$( "#CreateButton").click(function() {
    name = $("#nameOfExperiment").val(); 
    code1 = getAdviceCode.getValue(); 
    code2 = setRewardCode.getValue();
    hourly = $("#hourlyTheta").val();

    $.post( BASE_URL+"admin/exp/add.json", { 
        name: name, 
        getaction: code1,
        setreward: code2,
    	  hourly: hourly
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
    hourly = $("#hourlyTheta").val();

    if(CURR_ID !== 0){
    $.post( BASE_URL+"admin/exp/"+CURR_ID+"/edit.json", { 
        name: name, 
        getaction: code1,
        setreward: code2,
	  hourly: hourly
    })
    .done(function( data ) {
        // pretty ugly, but hey ;)
        location.reload();
     }); 
    }   
});

// Edit experiment
function editExperiment(id){

    CURR_ID = id ; 
    // Load the current experiment
    $.getJSON(BASE_URL+"admin/exp/"+id+"/get.json", function( data ){
        $("#nameOfExperiment").val(data.name);
        getAdviceCode.setValue(data.getAction);  
        setRewardCode.setValue(data.setReward);
        $("#TestGetAdvice").html('(<a href="'+API_URL+'/'+id+'/getAction.json?key='+data.key+'" target="_blank">try out</a>)');
        $("#TestSetReward").html('(<a href="'+API_URL+'/'+id+'/setReward.json?key='+data.key+'&reward='+encodeURIComponent(JSON.stringify({click:1}))+'&action='+encodeURIComponent(JSON.stringify({choice:1}))+'" target="_blank">try out</a>)');
    }); 
    $("#CreateButton").html("Store as new");
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
        console.log(data);
        $.each(data, function(key, val){
            $('#ExperimentsList > tbody:last-child').append('<tr><th scope="row">'+key+'</th><th>'+val.name+'</th><th>'+val.key+'</th><th>(<a href="#" onclick="editExperiment('+key+')">edit</a>)</th><th>(<a href="#" onclick="deleteExperiment('+key+')">delete</a>)</th></tr>');
        });          
    })
    .fail(function() {
        console.log( "error" );
      });

    $.getJSON( BASE_URL+"admin/exp/defaults.json", function( data ){
        console.log(data);
        $.each(data.defaults, function(key, val){
            $( '#DefaultList' )
            .append( '<button type="button" onclick="loadDefault('+key+')" class="btn btn-lg btn-primary">'+val.name+'</button> \n' );
        });
    });


    getAdviceCode = CodeMirror.fromTextArea($("#getAdviceText").get(0),{
    lineNumbers: true,
    mode:"python"});

    setRewardCode = CodeMirror.fromTextArea($("#setRewardText").get(0),{
    lineNumbers: true,
    mode:"python"});
    console.log(setRewardCode);


});



// Load default experiments
function loadDefault(id){
    $.getJSON( BASE_URL+"admin/exp/default/"+id+"/get.json", function( data ) {
        $("#nameOfExperiment").val(data.name);
        getAdviceCode.setValue(data.getAction);  
        setRewardCode.setValue(data.setReward);
    });
}
