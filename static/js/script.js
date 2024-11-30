var loading= document.getElementById("loading");
var loading2= document.getElementById("loading2");
var loading3= document.getElementById("loading3");

document
  .getElementById("predict-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    // Get form data
    const ticker = document.getElementById("predict-ticker").value;
    const start = document.getElementById("predict-start").value;
    const end = document.getElementById("predict-end").value;

    try {
        loading.style.display = "block";
      // Send request to the predict route
      const response = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker, start, end }),
      });

      const data = await response.json();

      if (data.error) {
        alert(data.error);
        return;
      }
      loading.style.display = "none";
      // Extract data for the chart
      const originalPrices = data.original_prices;
      const predictedPrices = data.predicted_prices;
      const labels = Array.from(
        { length: originalPrices.length },
        (_, i) => `Day ${i + 1}`
      );
      
      // Draw the chart
      drawChart(labels, originalPrices, predictedPrices);
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while fetching predictions.");
    }
  });

// Recommend Form Handler
document
  .getElementById("recommend-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    // Get form data
    const ticker = document.getElementById("recommend-ticker").value;
    const start = document.getElementById("recommend-start").value;
    const end = document.getElementById("recommend-end").value;

    try {
      loading2.style.display = "block";

      // Send request to the recommend route
      const response = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker, start, end }),
      });

      const data = await response.json();

      if (data.error) {
        alert(data.error);
        return;
      }
      loading2.style.display = "none";

      // Display recommendation result
      document.getElementById("result").innerHTML = `
              <p><strong>Recommendation:</strong> ${
                data.recommendation
              }</p>
              <p><strong>Last Actual Price:</strong> ${data.last_actual_price.toFixed(
                2
              )}</p>
              <p><strong>Last Predicted Price:</strong> ${data.last_predicted_price.toFixed(
                2
              )}</p>
          `;
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while fetching the recommendation.");
    }
  });

// Function to draw the chart
function drawChart(labels, originalPrices, predictedPrices) {
  const ctx = document.getElementById("stockChart").getContext("2d");

  // Destroy any existing chart before creating a new one
  if (window.stockChartInstance) {
    window.stockChartInstance.destroy();
  }

  // Create a new chart
  window.stockChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Original Prices",
          data: originalPrices,
          borderColor: "blue",
          fill: false,
          tension: 0.1,
        },
        {
          label: "Predicted Prices",
          data: predictedPrices,
          borderColor: "red",
          fill: false,
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Stock Price Prediction",
        },
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Days",
          },
        },
        y: {
          title: {
            display: true,
            text: "Price",
          },
        },
      },
    },
  });
}


document.getElementById("fetch-stocks").addEventListener("click", async function() {
  try {
    loading3.style.display = "block";

      // Fetch data from the server
      const response = await fetch("/fetch_stocks");
      const data = await response.json();

      if (data.error) {
          alert(data.error);
          return;
      }

      const stockContainer = document.getElementById("stock-container");
      stockContainer.innerHTML = ""; // Clear previous data
      loading3.style.display = "none";
    
      // Loop through stocks and create tables for each
      data.stocks.forEach(stock => {
          const table = document.createElement("table");
          table.border = "1";
          table.style.marginBottom = "20px";
          table.style.width = "100%";
          table.innerHTML = `
              <thead>
                  <tr>
                      <th colspan="3">${stock.ticker}</th>
                  </tr>
                  <tr>
                      <th>Date</th>
                      <th>Actual Price</th>
                      <th>Predicted Price</th>
                  </tr>
              </thead>
              <tbody>
                  ${stock.details.map(detail => `
                      <tr>
                          <td>${detail.Date}</td>
                          <td>${detail["Actual Price"].toFixed(2)}</td>
                          <td>${detail["Predicted Price"].toFixed(2)}</td>
                      </tr>
                  `).join("")}
              </tbody>
          `;
          stockContainer.appendChild(table);
      });
  } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while fetching stock data.");
  }
});
