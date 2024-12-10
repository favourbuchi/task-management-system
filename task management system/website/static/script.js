document.getElementById('close-btn').addEventListener('click', function(){
    var alert_message = document.querySelector(".alert");
    if(alert_message){
        alert_message.remove();
    }
})


function deleteActivity(activitiesId) {
    fetch('/delete-activity', {
        method: 'POST',
        body: JSON.stringify({ taskId: activitiesId })
    }).then((_res) => {
        window.location.href = "/"
    });
}