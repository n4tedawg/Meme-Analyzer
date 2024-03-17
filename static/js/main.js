const form = document.querySelector("#meme-explainer-form");
const explanationParagraph = document.querySelector("#explanation");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const requestOptions = {
    method: "POST",
    body: formData
  };

  try {
    const response = await fetch("/explain_meme", requestOptions);
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    explanationParagraph.textContent = data.explanation;
  } catch (error) {
    console.error("Error occurred while fetching explanation:", error);
    explanationParagraph.textContent = "An error occurred. Please try again.";
  }
});