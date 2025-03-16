document.getElementById("inputdiv").addEventListener("input", () => {
  if (document.getElementById("inputdiv").value.length > 0) {
    document.getElementById("SENDBUTTON").classList.replace("hidden", "flex");
    document.getElementById("AUDIOINPUT").classList.replace("flex", "hidden");
  } else {
    document.getElementById("SENDBUTTON").classList.replace("flex", "hidden");
    document.getElementById("AUDIOINPUT").classList.replace("hidden", "flex");
  }
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
