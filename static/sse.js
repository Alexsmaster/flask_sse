
console.log("build.v003");

const sse = new EventSource("/api/v1/sse");
sse.onopen = (event) => console.log("Connection opened")
sse.onerror = (event) => console.log("Error:", event)
sse.addEventListener("notice", (event) => {  console.log(event.data); });
sse.addEventListener("update", (event) => {  console.log(event.data); });
sse.onmessage = (event) => {
    console.log("message " + event.data);

    document.getElementById("002").innerHTML = '(/api/v1/sse).... - ' + event.data + " Came at: - " + new Date().toISOString();
}

const ssestream = new EventSource("/api/v1/stream");
ssestream.onopen = (event) => console.log("Connection opened")
ssestream.onerror = (event) => console.log("Error:", event)
ssestream.addEventListener("notice", (event) => {  console.log(event.data); });
ssestream.addEventListener("update", (event) => {  console.log(event.data); });

ssestream.onmessage = (event) => {
    console.log("message " + event.data);

    document.getElementById("003").innerHTML = '(/api/v1/stream)  - ' + event.data + " Came at: - " + new Date().toISOString();
}




//
//async function postJSON(url, data) {
//  try {
//    const response = await fetch(url, {
//      method: "POST", // or 'PUT'
//      headers: {
//        "Content-Type": "application/json"
//      },
//      body: JSON.stringify({
//        text: data
//      }),
//    });
//    const result = await response.json();
//    console.log("comment: postJSON >>>> fetch()", result);
//  } catch (error) {
//    console.error("Error: postJSON >>>> fetch():", error);
//  }
//}



function open_win() {
  window.open("/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=0,width=300,height=300");
  window.open("/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=300,width=300,height=300");
//  window.open("http://192.168.88.221:5000/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=600,width=300,height=300");
//  window.open("http://192.168.88.221:5000/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=900,width=300,height=300");
//  window.open("http://192.168.88.221:5000/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=1200,width=300,height=300");
}