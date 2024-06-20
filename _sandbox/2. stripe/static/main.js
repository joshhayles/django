// main.js

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

// Get Stripe publishable key
fetch("/config/")
  .then((result) => {
    if (result.ok) {
      return result.json();
    } else {
      throw new Error("Error fetching Stripe configuration");
    }
  })
  .then((data) => {
    console.log("Publishable key:", data.publicKey);
    // initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // Event handler
    document.addEventListener("DOMContentLoaded", () => {
      document.querySelector("#submitBtn").addEventListener("click", () => {
        console.log("button clicked");
        fetch("/create-checkout-session/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
        })
          .then((result) => {
            if (result.ok) {
              return result.json();
            } else {
              throw new Error("Error creating Checkout session");
            }
          })
          .then((data) => {
            console.log("Checkout session data:", data);
            // redirect to Stripe checkout
            return stripe.redirectToCheckout({ sessionId: data.sessionId });
          })
          .then((result) => {
            if (result.error) {
              console.error("Error redirecting to Checkout:", result.error);
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      });
    });
  })
  .catch((error) => {
    console.error("Error:", error);
  });
