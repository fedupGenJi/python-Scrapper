document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/laptops")
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("laptop-container");
      data.forEach(laptop => {
        const card = document.createElement("div");
        card.className = "laptop-card";
        card.innerHTML = `
          <img src="${laptop.face_image_url || 'https://via.placeholder.com/300'}" alt="Laptop Image">
          <h2>${laptop.display_name || laptop.model_name || 'No Name'}</h2>
          <p><strong>Brand:</strong> ${laptop.brand_name}</p>
          <p><strong>Model:</strong> ${laptop.model_name}</p>
          <p><strong>Year:</strong> ${laptop.model_year}</p>
          <p><strong>Type:</strong> ${laptop.product_type}</p>
          <p><strong>Auth:</strong> ${laptop.product_authentication}</p>
          <p><strong>Suitable for:</strong> ${laptop.suitable_for}</p>
          <p><strong>Color:</strong> ${laptop.color}</p>
          <p><strong>Processor Gen:</strong> ${laptop.processor_generation}</p>
          <p><strong>Processor:</strong> ${laptop.processor}</p>
          <p><strong>Series:</strong> ${laptop.processor_series}</p>
          <p><strong>RAM:</strong> ${laptop.ram} GB (${laptop.ram_type})</p>
          <p><strong>Storage:</strong> ${laptop.storage} GB (${laptop.storage_type})</p>
          <p><strong>Graphics:</strong> ${laptop.graphic} (${laptop.graphic_ram} GB)</p>
          <p><strong>Display:</strong> ${laptop.display} (${laptop.display_type})</p>
          <p><strong>Touchscreen:</strong> ${laptop.touchscreen ? "Yes" : "No"}</p>
          <p><strong>Power:</strong> ${laptop.power_supply}</p>
          <p><strong>Battery:</strong> ${laptop.battery}</p>
          <p><strong>Warranty:</strong> ${laptop.warranty}</p>
          <p><strong>Cost Price:</strong> ₹${laptop.cost_price}</p>
          <p><strong>Show Price:</strong> ₹${laptop.show_price}</p>
          <p><strong>Quantity:</strong> ${laptop.quantity}</p>
        `;
        container.appendChild(card);
      });
    })
    .catch(err => {
      console.error("Failed to load laptops:", err);
    });
});
