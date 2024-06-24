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

let stripe; // Declare stripe variable in a global scope

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
    // Initialize Stripe.js and assign to global stripe variable
    stripe = Stripe(data.publicKey);
  })
  .catch((error) => {
    console.error("Error:", error);
  });

// Event handler
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM content loaded");
  try {
    const purchaseReportBtn = document.querySelector("#purchaseReportBtn");
    purchaseReportBtn.addEventListener("click", () => {
      console.log("button clicked");
      fetch("/payments/create-checkout-session/", {
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
          // Ensure stripe is defined before using it
          if (!stripe) {
            throw new Error("Stripe has not been initialized yet.");
          }
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
  } catch (error) {
    console.error("Error finding button:", error);
  }
});
