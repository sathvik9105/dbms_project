document.addEventListener("DOMContentLoaded", () => {
  // Venue options for each event type
  const venues = {
    birthday: [
      {
        name: "Noma Convention",
        facilities: ["ac", "valet_parking"],
        capacity: 200,
      },
      {
        name: "Balaji Function Hall",
        facilities: ["non_ac", "internet"],
        capacity: 150,
      },
      {
        name: "Grand Paradise",
        facilities: ["ac", "internet", "led_screens"],
        capacity: 300,
      },
      {
        name: "Sunshine Hall",
        facilities: ["non_ac", "valet_parking"],
        capacity: 100,
      },
    ],
    wedding: [
      {
        name: "Royal Orchid Palace",
        facilities: ["ac", "valet_parking", "led_screens"],
        capacity: 500,
      },
      {
        name: "Vivanta Taj",
        facilities: ["ac", "internet", "led_screens"],
        capacity: 400,
      },
      {
        name: "The Oberoi Venue",
        facilities: ["ac", "valet_parking", "internet"],
        capacity: 600,
      },
      {
        name: "Leela Banquet Hall",
        facilities: ["ac", "valet_parking", "internet"],
        capacity: 450,
      },
    ],
    house_warming: [
      { name: "Cozy Corner", facilities: ["ac", "internet"], capacity: 100 },
      {
        name: "Home Sweet Home",
        facilities: ["non_ac", "valet_parking"],
        capacity: 80,
      },
      {
        name: "Garden Paradise",
        facilities: ["non_ac", "internet"],
        capacity: 120,
      },
      {
        name: "Urban Nest",
        facilities: ["ac", "valet_parking"],
        capacity: 150,
      },
    ],
    baby_shower: [
      {
        name: "Little Angels Hall",
        facilities: ["ac", "internet"],
        capacity: 100,
      },
      {
        name: "Tiny Tots Paradise",
        facilities: ["ac", "valet_parking"],
        capacity: 120,
      },
      {
        name: "Stork's Corner",
        facilities: ["non_ac", "internet"],
        capacity: 80,
      },
      {
        name: "Baby Bliss Center",
        facilities: ["ac", "led_screens"],
        capacity: 150,
      },
    ],
    reunion: [
      {
        name: "Memory Lane Hall",
        facilities: ["ac", "internet", "led_screens"],
        capacity: 200,
      },
      {
        name: "Nostalgia Palace",
        facilities: ["ac", "valet_parking"],
        capacity: 250,
      },
      {
        name: "Friends Forever Center",
        facilities: ["non_ac", "internet"],
        capacity: 180,
      },
      {
        name: "Reunion Plaza",
        facilities: ["ac", "valet_parking", "led_screens"],
        capacity: 300,
      },
    ],
    engagement: [
      {
        name: "Promise Banquet",
        facilities: ["ac", "internet", "led_screens"],
        capacity: 300,
      },
      {
        name: "Love Knot Venue",
        facilities: ["ac", "valet_parking"],
        capacity: 250,
      },
      {
        name: "Celebration Hall",
        facilities: ["ac", "valet_parking", "led_screens"],
        capacity: 400,
      },
      {
        name: "Dreamland Banquet",
        facilities: ["ac", "internet", "led_screens"],
        capacity: 350,
      },
    ],
    reception: [
      {
        name: "Grand Celebration Center",
        facilities: ["ac", "valet_parking", "led_screens"],
        capacity: 600,
      },
      {
        name: "Royal Reception Hall",
        facilities: ["ac", "internet", "led_screens"],
        capacity: 500,
      },
      {
        name: "Majestic Manor",
        facilities: ["ac", "valet_parking", "internet"],
        capacity: 700,
      },
      {
        name: "Elite Events Plaza",
        facilities: ["ac", "valet_parking", "led_screens"],
        capacity: 550,
      },
    ],
    conference: [
      {
        name: "Tech Park Hall",
        facilities: ["ac", "internet", "led_screens"],
        capacity: 200,
      },
      {
        name: "Business Center",
        facilities: ["ac", "valet_parking", "internet"],
        capacity: 150,
      },
      {
        name: "Corporate Plaza",
        facilities: ["ac", "internet", "led_screens"],
        capacity: 300,
      },
      {
        name: "Executive Summit Hall",
        facilities: ["ac", "valet_parking", "led_screens"],
        capacity: 250,
      },
    ],
  };

  // DOM Elements
  const eventTypeSelect = document.getElementById("eventType");
  const venueSelect = document.getElementById("venue");
  const facilitiesSelect = document.getElementById("facilities");
  const guestCount = document.getElementById("guestCount");
  const eventForm = document.getElementById("eventForm");
  const bookingSummary = document.getElementById("bookingSummary");
  const summaryContent = document.getElementById("summaryContent");

  // Update venue options based on user input
  function updateVenueOptions() {
    const selectedEvent = eventTypeSelect.value;
    const selectedFacility = facilitiesSelect.value;
    const guests = parseInt(guestCount.value) || 0;

    // Clear current venue options
    venueSelect.innerHTML = "<option value=''>Select venue</option>";

    // Populate options
    if (venues[selectedEvent]) {
      venues[selectedEvent]
        .filter((venue) => {
          const meetsCapacity = venue.capacity >= guests;
          const meetsFacility =
            !selectedFacility || venue.facilities.includes(selectedFacility);
          return meetsCapacity && meetsFacility;
        })
        .forEach((venue) => {
          const option = document.createElement("option");
          option.value = venue.name;
          const facilities = venue.facilities
            .map((f) => f.replace(/_/g, " "))
            .join(", ");
          option.textContent = `${venue.name} (${facilities}) - Capacity: ${venue.capacity}`;
          venueSelect.appendChild(option);
        });
    }
  }

  // Event Listeners for dynamic updates
  eventTypeSelect.addEventListener("change", updateVenueOptions);
  facilitiesSelect.addEventListener("change", updateVenueOptions);
  guestCount.addEventListener("change", updateVenueOptions);

  // Handle form submission
  eventForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = {
      firstName: document.getElementById("first_name").value.trim(),
      lastName: document.getElementById("last_name").value.trim(),
      phone: document.getElementById("phone").value.trim(),
      email: document.getElementById("email").value.trim(),
      guestCount: parseInt(guestCount.value) || 0,
      eventType: eventTypeSelect.value,
      venue: venueSelect.value,
      catering: document.getElementById("catering").value,
      decoration: document.getElementById("decoration").value,
      entertainment: document.getElementById("entertainment").value,
      eventDate: document.getElementById("eventDate").value.trim(),
    };

    if (!formData.venue) {
      alert("Please select a venue.");
      return;
    }

    fetch("/api/events", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    }).then((response) => response.json());

    const pricing = {
      catering: {
        indian: 500,
        continental: 700,
        chinese: 600,
        italian: 800,
        mexican: 900,
        japanese: 1000,
        thai: 750,
        vegan_special: 850,
      },
      decoration: { simple: 5000, premium: 10000, luxury: 20000 },
      entertainment: { music: 8000, dance: 12000, comedy: 15000 },
    };

    const costs = {
      catering: pricing.catering[formData.catering] * formData.guestCount || 0,
      decoration: pricing.decoration[formData.decoration] || 0,
      entertainment: pricing.entertainment[formData.entertainment] || 0,
      venue: Math.floor(Math.random() * 20000) + 5000,
    };

    const subtotal = Object.values(costs).reduce(
      (total, cost) => total + cost,
      0
    );
    const tax = subtotal * 0.18;
    const serviceCharge = formData.guestCount > 100 ? 7500 : 3500;
    const convenienceFee = 350;
    const securityDeposit = Math.floor(Math.random() * 1000) + 2500;
    const grandTotal =
      subtotal + tax + serviceCharge + convenienceFee + securityDeposit;

    // Display booking summary
    summaryContent.innerHTML = `
      <h3 class="text-xl font-bold mb-4">Booking Summary</h3>
      <div class="space-y-2">
        <p><strong>Customer:</strong> ${formData.firstName} ${
      formData.lastName
    }</p>
        <p><strong>Contact:</strong> ${formData.contactInfo}</p>
        <p><strong>Event Type:</strong> ${formData.eventType}</p>
        <p><strong>Venue:</strong> ${formData.venue}</p>
        <p><strong>Event Date:</strong> ${formData.eventDate}</p>
        <p><strong>Number of Guests:</strong> ${formData.guestCount}</p>
        <div class="mt-4">
          <h4 class="font-bold">Cost Breakdown</h4>
          <p>Catering (${
            formData.catering
          }): ₹${costs.catering.toLocaleString()}</p>
          <p>Decoration (${
            formData.decoration
          }): ₹${costs.decoration.toLocaleString()}</p>
          <p>Entertainment (${
            formData.entertainment
          }): ₹${costs.entertainment.toLocaleString()}</p>
          <p>Venue: ₹${costs.venue.toLocaleString()}</p>
          <p>Tax (18%): ₹${tax.toLocaleString()}</p>
          <p>Service Charge: ₹${serviceCharge.toLocaleString()}</p>
          <p>Convenience Fee: ₹${convenienceFee}</p>
          <p>Security Deposit: ₹${securityDeposit.toLocaleString()}</p>
        </div>
        <p class="text-xl font-bold mt-4">Grand Total: ₹${grandTotal.toLocaleString()}</p>
      </div>
    `;

    bookingSummary.classList.remove("hidden");
  });

  // Proceed to billing
  document.getElementById("proceedBilling").addEventListener("click", () => {
    alert("Proceeding to payment gateway...");
  });
});
