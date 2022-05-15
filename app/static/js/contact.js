// var sendMessage = function(){
//     document.getElementById('sendBtn');

// } 
// Reset form fields after submission
var resetForm = function(){
    document.getElementById('contactForm').reset();
}

document.getElementById('sendBtn').addEventListener('click', clickedBtn);
function clickedBtn(){
    // Confirm("You clicked the button!");
    confirm('Do you want to send this message?')
}