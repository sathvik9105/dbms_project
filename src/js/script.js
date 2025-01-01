document.addEventListener("DOMContentLoaded", () => {
  // Venue options for each event type
  const venues = {
    birthday: [
      { name: "Noma Convention", facilities: ["ac", "valet_parking"], capacity: 200 },
      { name: "Balaji Function Hall", facilities: ["non_ac", "internet"], capacity: 150 },
      { name: "Grand Paradise", facilities: ["ac", "internet", "led_screens"], capacity: 300 },
      { name: "Sunshine Hall", facilities: ["non_ac", "valet_parking"], capacity: 100 }
    ],
    wedding: [
      { name: "Royal Orchid Palace", facilities: ["ac", "valet_parking", "led_screens"], capacity: 500 },
      { name: "Vivanta Taj", facilities: ["ac", "internet", "led_screens"], capacity: 400 },
      { name: "The Oberoi Venue", facilities: ["ac", "valet_parking", "internet"], capacity: 600 },
      { name: "Leela Banquet Hall", facilities: ["ac", "valet_parking", "internet"], capacity: 450 }
    ],
    house_warming: [
      { name: "Cozy Corner", facilities: ["ac", "internet"], capacity: 100 },
      { name: "Home Sweet Home", facilities: ["non_ac", "valet_parking"], capacity: 80 },
      { name: "Garden Paradise", facilities: ["non_ac", "internet"], capacity: 120 },
      { name: "Urban Nest", facilities: ["ac", "valet_parking"], capacity: 150 }
    ],
    baby_shower: [
      { name: "Little Angels Hall", facilities: ["ac", "internet"], capacity: 100 },
      { name: "Tiny Tots Paradise", facilities: ["ac", "valet_parking"], capacity: 120 },
      { name: "Stork's Corner", facilities: ["non_ac", "internet"], capacity: 80 },
      { name: "Baby Bliss Center", facilities: ["ac", "led_screens"], capacity: 150 }
    ],
    reunion: [
      { name: "Memory Lane Hall", facilities: ["ac", "internet", "led_screens"], capacity: 200 },
      { name: "Nostalgia Palace", facilities: ["ac", "valet_parking"], capacity: 250 },
      { name: "Friends Forever Center", facilities: ["non_ac", "internet"], capacity: 180 },
      { name: "Reunion Plaza", facilities: ["ac", "valet_parking", "led_screens"], capacity: 300 }
    ],
    engagement: [
      { name: "Promise Banquet", facilities: ["ac", "internet", "led_screens"], capacity: 300 },
      { name: "Love Knot Venue", facilities: ["ac", "valet_parking"], capacity: 250 },
      { name: "Celebration Hall", facilities: ["ac", "valet_parking", "led_screens"], capacity: 400 },
      { name: "Dreamland Banquet", facilities: ["ac", "internet", "led_screens"], capacity: 350 }
    ],
    reception: [
      { name: "Grand Celebration Center", facilities: ["ac", "valet_parking", "led_screens"], capacity: 600 },
      { name: "Royal Reception Hall", facilities: ["ac", "internet", "led_screens"], capacity: 500 },
      { name: "Majestic Manor", facilities: ["ac", "valet_parking", "internet"], capacity: 700 },
      { name: "Elite Events Plaza", facilities: ["ac", "valet_parking", "led_screens"], capacity: 550 }
    ],
    conference: [
      { name: "Tech Park Hall", facilities: ["ac", "internet", "led_screens"], capacity: 200 },
      { name: "Business Center", facilities: ["ac", "valet_parking", "internet"], capacity: 150 },
      { name: "Corporate Plaza", facilities: ["ac", "internet", "led_screens"], capacity: 300 },
      { name: "Executive Summit Hall", facilities: ["ac", "valet_parking", "led_screens"], capacity: 250 }
    ]
  };

  const eventTypeSelect = document.getElementById("eventType");
  const venueSelect = document.getElementById("venue");
  const facilitiesSelect = document.getElementById("facilities");
  const guestCount = document.getElementById("guestCount");
  const eventForm = document.getElementById("eventForm");
  const bookingSummary = document.getElementById("bookingSummary");
  const summaryContent = document.getElementById("summaryContent");

  function updateVenueOptions() {
    const selectedEvent = eventTypeSelect.value;
    const selectedFacility = facilitiesSelect.value;
    const guests = parseInt(guestCount.value) || 0;

    venueSelect.innerHTML = "<option value=''>Select venue</option>";

    if (selectedEvent) {
      fetch(`/api/venue-options?event_type=${selectedEvent}&facility=${selectedFacility}&guest_count=${guests}`)
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            data.venues.forEach(venue => {
              const option = document.createElement("option");
              option.value = venue.name;
              const facilities = venue.facilities.map(f => f.replace(/_/g, ' ')).join(', ');
              option.textContent = `${venue.name} (${facilities}) - Capacity: ${venue.capacity}`;
              venueSelect.appendChild(option);
            });
          } else {
            alert("Error fetching venues: " + data.error);
          }
        })
        .catch(err => alert("An error occurred: " + err));
    }
  }

  eventTypeSelect.addEventListener("change", updateVenueOptions);
  facilitiesSelect.addEventListener("change", updateVenueOptions);
  guestCount.addEventListener("change", updateVenueOptions);

  eventForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = {
      customer_name: document.getElementById("customerName").value,
      contact_info: document.getElementById("contactInfo").value,
      address: document.getElementById("address").value,
      guest_count: parseInt(document.getElementById("guestCount").value),
      event_type: eventTypeSelect.value,
      venue: venueSelect.value,
      catering: document.getElementById("catering").value,
      decoration: document.getElementById("decoration").value,
      entertainment: document.getElementById("entertainment").value,
      event_date: document.getElementById("eventDate").value
    };

    if (!formData.venue) {
      alert("Please select a venue");
      return;
    }

    try {
      const response = await fetch('/api/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!response.ok) throw new Error('Failed to submit booking');

      const result = await response.json();
      alert('Booking submitted successfully!');
      eventForm.reset();
    } catch (error) {
      alert('Error submitting booking: ' + error.message);
    }
  });
});
