document.getElementById("question-form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent the form from refreshing the page

    // Get the question input value
    const question = document.getElementById("question").value;

    // Optional: Add a default context or allow users to provide one
    const context = "A hash map is a data structure that stores key-value pairs. It uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found.";

    // Clear the previous answer
    document.getElementById("answer").textContent = "Loading...";

    try {
        // Send a POST request to the /ask endpoint
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question, context }),
        });

        // Parse the JSON response
        const data = await response.json();

        // Display the answer
        if (data.answer) {
            document.getElementById("answer").textContent = data.answer;
        } else {
            document.getElementById("answer").textContent = "No answer found.";
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("answer").textContent = "An error occurred while fetching the answer.";
    }
});