var timeStampEvent;

var source = new EventSource("{{ url_for('sse.stream') }}");

source.addEventListener('greeting', function(event) {
    var data = JSON.parse(event.data);
    timeStampEvent = Date.now()
    document.getElementById("001").innerHTML = "The server says " + data.message + " at " + new Date(timeStampEvent).toISOString();

}, false);
source.addEventListener('error', function(event) {

    document.getElementById("001").innerHTML = "Failed to connect to event stream. Is Redis running?";
}, false);
var intervalId = window.setInterval(function() {
    document.getElementById("001").innerHTML = "No events came";
    if (timeStampEvent != undefined) {
        document.getElementById("001").innerHTML = "No events came since " + new Date(timeStampEvent).toISOString();
    }
    document.getElementById("002").innerHTML = "No events came";
    document.getElementById("003").innerHTML = "No events came";
}, 10000);


var isPerformanceSupported = (
    window.performance &&
    window.performance.now &&
    window.performance.timing &&
    window.performance.timing.navigationStart
);

var timeStampInMs = (
    isPerformanceSupported ?
    window.performance.now() +
    window.performance.timing.navigationStart :
    Date.now()
);



var now = new Date();
var isoString = now.toISOString();


var intervalUpdate = window.setInterval(function() {

    document.getElementById("002").innerHTML = timeStampEvent != undefined ? (Date.now() - timeStampEvent) / 1000 : (Date.now() - window.performance.timing.navigationStart) / 1000;
    document.getElementById("003").innerHTML = new Date(window.performance.timing.navigationStart).toISOString() + " | " + new Date().toISOString();
}, 100);

var button = document.getElementById("004");
button.addEventListener('click', function(event) {
    console.log('button got fired');
})



async function postJSON(data) {
    let url = "/api/call_event";
    try {
        const response = await fetch(url, {
            method: "POST", // or 'PUT'
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: data
            }),
        });
        const result = await response.json();
        console.log("comment: postJSON >>>> fetch()", result);
    } catch (error) {
        console.error("Error: postJSON >>>> fetch():", error);
    }
}



function open_win() {
    window.open("http://192.168.88.221:5000/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=0,width=300,height=300")
    window.open("http://192.168.88.221:5000/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=300,width=300,height=300") <
        !--window.open("http://192.168.88.221:5000/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=600,width=300,height=300") -- >
        <
        !--window.open("http://192.168.88.221:5000/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=900,width=300,height=300") -- >
        <
        !--window.open("http://192.168.88.221:5000/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=1200,width=300,height=300") -- >
}

var source = new EventSource("http://localhost:8001/stream")
source.onopen = (e) => console.log("Connection opened")
source.onerror = (e) => console.log("Error:", event)
source.onmessage = (e) => {
    if (event.data !== "[DONE]") {
        document.getElementById("msg-box").innerHTML += " " + event.data
    } else {
        console.log("Connection closed")
        source.close()
    }
}