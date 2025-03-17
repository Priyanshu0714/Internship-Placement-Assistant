function audiotextChange() {
  document.getElementById("inputdiv").addEventListener("input", () => {
    if (document.getElementById("inputdiv").value.length > 0) {
      document.getElementById("SENDBUTTON").classList.replace("hidden", "flex");
      document.getElementById("AUDIOINPUT").classList.replace("flex", "hidden");
    } else {
      document.getElementById("SENDBUTTON").classList.replace("flex", "hidden");
      document.getElementById("AUDIOINPUT").classList.replace("hidden", "flex");
    }
  });
}
audiotextChange();
function addChatarea() {
  if (document.getElementById("chattingarea").children.length == 0) {
    document.getElementById("chattingarea").classList.replace("flex", "hidden");
  } else {
    document.getElementById("chattingarea").classList.replace("hidden", "flex");
    document.getElementById("heading").classList.replace("flex", "hidden");
  }
}
// for the input field send when enter is clicked
document.getElementById("inputdiv").addEventListener("keypress", (event) => {
  if (event.key === "Enter") {
    document.getElementById("SENDBUTTON").click();
  }
});

// for the message appening part when the user send the message
document.getElementById("SENDBUTTON").addEventListener("click", async () => {
  const messageinput = document.getElementById("inputdiv");
  const appenddiv = document.getElementById("chattingarea");
  if (messageinput.value.length < 2) {
    appenddiv.innerHTML += `<div class="min-w-full h-auto float-left clear-both">
                Message too Short!!
            </div>`;
  } else {
    appenddiv.innerHTML += `<div class="max-w-[50%] h-auto float-right clear-both text-right py-2 px-4 bg-[#303030] rounded-l-full rounded-r-full w-auto">
                ${messageinput.value}
            </div>`;

    const res = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: messageinput.value }),
    });

    const json = await res.json();
    console.log(json);
    const data = await json.response;
    // if (json.response) {
    //   appenddiv.innerHTML += `<div class="min-w-full h-auto float-left clear-both">
    //                 ${json.response}
    //             </div>`;
    // }

    const response_table = document.createElement("table");
    for (let i in data) {
      let row = document.createElement("tr");

      for (let j in data[i]) {
        row.innerHTML += `<td>${data[i][j]}</td>`;
        response_table.appendChild(row);
      }

      appenddiv.innerHTML += `
            <div class="min-w-full h-auto float-left clear-both text-left py-5 px-4 bg-[#303030] rounded-l-full rounded-r-full">
                ${response_table.innerHTML}
            </div>`;
    }
  }
  messageinput.value = "";
  messageinput.dispatchEvent(new Event("input"));
  addChatarea();
});

// Speech Recognition Setup
const audioButton = document.getElementById("AUDIOINPUT");
const inputField = document.getElementById("inputdiv");

// Check if SpeechRecognition API is supported
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.lang = "en-US"; // Set language
  recognition.interimResults = false;

  audioButton.addEventListener("click", () => {
    recognition.start();
  });

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript; // Get the spoken text
    inputField.value = transcript;

    // Toggle buttons
    document.getElementById("SENDBUTTON").classList.replace("hidden", "flex");
    document.getElementById("AUDIOINPUT").classList.replace("flex", "hidden");
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
  };
} else {
  console.warn("Speech Recognition API is not supported in this browser.");
}
