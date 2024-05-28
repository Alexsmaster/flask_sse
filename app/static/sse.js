console.log("build.v007");

//const nowTimestamp, minutes, seconds, millis, nowTimestamp_mmssMS




const ssestream = new EventSource("/api/sse");
ssestream.onopen = (event) => console.log("Connection opened");
ssestream.onerror = (event) => console.log("Error:", event);
ssestream.onmessage = (event) => {
  console.log("message ", event.data);
    const nowTimestamp = new Date();
    const minutes = nowTimestamp.getMinutes().toString().padStart(2, '0');
    const seconds = nowTimestamp.getSeconds().toString().padStart(2, '0');
    const millis = nowTimestamp.getMilliseconds().toString().padStart(3, '0');
    const nowTimestamp_mmssMS = `${minutes}:${seconds}:${millis}`
    document.getElementById("001").innerHTML = 'JS|sse: ' + event.data + " Came at: - " + nowTimestamp_mmssMS;
};
//
//let now = new Date();
//let minutes = now.getMinutes().toString().padStart(2, '0');
//let seconds = now.getSeconds().toString().padStart(2, '0');
//let millis = now.getMilliseconds().toString().padStart(3, '0');
//
//console.log(`${minutes}:${seconds}:${millis}`);




//ssestream.addEventListener("occur", (event) => {
//  console.log("occur ", event.data);
//  document.getElementById("002").innerHTML = '(/api/sse)  - occur ' + event.data + " Came at: - " + new Date().toISOString().split('T')[1].split('.')[0];
//});

async function postJSON(url, data) {
  try {
    const nowTimestamp = new Date();
    const minutes = nowTimestamp.getMinutes().toString().padStart(2, '0');
    const seconds = nowTimestamp.getSeconds().toString().padStart(2, '0');
    const millis = nowTimestamp.getMilliseconds().toString().padStart(3, '0');
    const nowTimestamp_mmssMS = `${minutes}:${seconds}:${millis}`
    const response = await fetch(url, {
      method: "POST", // or 'PUT'
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: data + 'send at: ' + nowTimestamp_mmssMS
      }),
    });
    const result = await response.json();
    console.log("Debug - JS: postJSON >>>> answer from server: ", result);
  } catch (error) {
    console.error("Debug - JS: postJSON >>>> error: ", error);
  }
}






function open_win() {
  window.open("/", "_blank", "toolbar=no,scrollbars=no,resizable=yes,top=0,left=0,width=300,height=300");
  window.open("/", "_blank", "toolbar=no,scrollbars=no,resizable=yes,top=0,left=300,width=300,height=300");

//  window.open("http://192.168.88.221:5000/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=600,width=300,height=300");
//  window.open("http://192.168.88.221:5000/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=900,width=300,height=300");
//  window.open("http://192.168.88.221:5000/", "_blank", "toolbar=no,scrollbars=no,resizable=no,top=0,left=1200,width=300,height=300");
}