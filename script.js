function applyAttack(attackType) {
    // Reset outputs
    document.getElementById("live-output").innerText = "Processing...";
    document.getElementById("final-output").innerText = "";

    // Create a new WebSocket connection
    let socket = new WebSocket("ws://127.0.0.1:8000/ws");

    socket.onopen = function () {
        console.log("WebSocket connected");
        // Send the attack type to the backend
        socket.send(JSON.stringify({ attack: attackType }));
    };

    socket.onmessage = function (event) {
        let data = JSON.parse(event.data);

        if (data.error) {
            document.getElementById("live-output").innerText = "Error: " + data.error;
            return;
        }

        // For interim updates (every 5 sec), update the live prediction output
        if (!data.final) {
            document.getElementById("live-output").innerText = "5-sec Batch Prediction: " + data.prediction;
        } else {
            // Final update after 1 minute
            document.getElementById("final-output").innerText = "Final Prediction (1 min): " + data.prediction;
        }
    };

    socket.onerror = function (error) {
        console.error("WebSocket Error:", error);
    };

    socket.onclose = function () {
        console.log("WebSocket closed");
    };
}
