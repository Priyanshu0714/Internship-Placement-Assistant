function audiotextChange() {
    document.getElementById("inputdiv").addEventListener("input", () => {
        if (document.getElementById("inputdiv").value.length > 0) {
            document
                .getElementById("SENDBUTTON")
                .classList.replace("hidden", "flex");
            document
                .getElementById("AUDIOINPUT")
                .classList.replace("flex", "hidden");
        } else {
            document
                .getElementById("SENDBUTTON")
                .classList.replace("flex", "hidden");
            document
                .getElementById("AUDIOINPUT")
                .classList.replace("hidden", "flex");
        }
    });
}
audiotextChange();
function addChatarea() {
    if (document.getElementById("chattingarea").children.length == 0) {
        document
            .getElementById("chattingarea")
            .classList.replace("flex", "hidden");
    } else {
        document
            .getElementById("chattingarea")
            .classList.replace("hidden", "flex");
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
        appenddiv.innerHTML += `<div class="w-[50%] h-auto float-right clear-both text-right">
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
        const response = await json.response;
        const response_div = document.createElement("div");
        response_div.classList = [
            "w-[50%]",
            "h-auto",
            "float-left",
            "clear-both",
            "text-left",
        ];
        const response_table = document.createElement("table");
        response_table.innerHTML =
            "<tr><th class='p-2 border'>Title</th><th class='p-2 border'>Company</th><th class='p-2 border'>Stipend</th><th class='p-2 border'>Link</th></tr>";
        for (i in response) {
            let row = document.createElement("tr");
            response_table.append(row);
            for (j in response[i]) {
                if (j == 3) {
                    row.innerHTML += `<td class='p-2 px-5 border'><a src=${response[i][j]}>Apply</a></td>`;
                } else {
                    row.innerHTML += `<td class='p-2 px-5 border'>${response[i][j]}</td>`;
                }
            }
        }
        response_div.append(response_table);
        appenddiv.append(response_div);
        console.log(json.response);
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
        document
            .getElementById("SENDBUTTON")
            .classList.replace("hidden", "flex");
        document
            .getElementById("AUDIOINPUT")
            .classList.replace("flex", "hidden");
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
    };
} else {
    console.warn("Speech Recognition API is not supported in this browser.");
}
