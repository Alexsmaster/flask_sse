console.log("build.v007");


const ssestream = new EventSource("/api/sse");
ssestream.onopen = (event) => console.log("Connection opened");
ssestream.onerror = (event) => console.log("Error:", event);
ssestream.onmessage = (event) => {
  console.log("message ", event.data);
    document.getElementById("001").innerHTML = '(/api/sse)  - message ' + event.data + " Came at: - " + new Date().toISOString();
};

ssestream.addEventListener("occur", (event) => {
  console.log("occur ", event.data);
  document.getElementById("002").innerHTML = '(/api/sse)  - occur ' + event.data + " Came at: - " + new Date().toISOString();
});

async function postJSON(url, data) {
  try {
    const response = await fetch(url, {
      method: "POST", // or 'PUT'
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: data + 'Button pressed at ' + new Date().toISOString()
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