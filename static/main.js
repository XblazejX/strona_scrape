document.addEventListener("DOMContentLoaded", function () {
  const formSection = document.getElementById("form-section");
  const tabsSection = document.getElementById("tabs-section");
  const loader = document.getElementById("loader");

  // Przyciski zakładek
  const instagramTab = document.getElementById("instagram-tab");
  const youtubeTab = document.getElementById("youtube-tab");
  const tiktokTab = document.getElementById("tiktok-tab");
  const twitchTab = document.getElementById("twitch-tab");

  // Zakładki zawierające dane
  const instagramContent = document.getElementById("instagram-content");
  const youtubeContent = document.getElementById("youtube-content");
  const tiktokContent = document.getElementById("tiktok-content");
  const twitchContent = document.getElementById("twitch-content");

  // Funkcja wysyłająca dane z formularza do backendu
  function sendData() {
      const instagramUsername = document.getElementById("input-instagram").value;
      const youtubeUsername = document.getElementById("input-youtube").value;
      const tiktokUsername = document.getElementById("input-tiktok").value;
      const twitchUsername = document.getElementById("input-twitch").value;

      // Pokaż loader
      loader.style.display = "block";
      formSection.style.display = "none";  // Ukryj formularz

      const data = {
          instagram: instagramUsername,
          youtube: youtubeUsername,
          tiktok: tiktokUsername,
          twitch: twitchUsername
      };

      // Wyślij dane do backendu
      fetch("/run-scraper", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(responseData => {
          // Ukryj loader
          loader.style.display = "none";
          tabsSection.style.display = "block";  // Pokaż zakładki

          // Zaktualizuj zakładki i dane w tabach
          if (responseData.instagram) {
              instagramTab.style.display = "inline-block";
              instagramContent.style.display = "block";
              document.getElementById("instagram-name").textContent = responseData.instagram.name;
              document.getElementById("instagram-link").href = responseData.instagram.url;
          }
          if (responseData.youtube) {
              youtubeTab.style.display = "inline-block";
              youtubeContent.style.display = "block";
              document.getElementById("youtube-name").textContent = responseData.youtube.name;
              document.getElementById("youtube-link").href = responseData.youtube.url;
          }
          if (responseData.tiktok) {
              tiktokTab.style.display = "inline-block";
              tiktokContent.style.display = "block";
              document.getElementById("tiktok-name").textContent = responseData.tiktok.name;
              document.getElementById("tiktok-link").href = responseData.tiktok.url;
          }
          if (responseData.twitch) {
              twitchTab.style.display = "inline-block";
              twitchContent.style.display = "block";
              document.getElementById("twitch-name").textContent = responseData.twitch.name;
              document.getElementById("twitch-link").href = responseData.twitch.url;
          }

          // Domyślnie otwieramy pierwszą zakładkę (np. Instagram)
          openTab("instagram");
      })
      .catch(error => {
          console.error("Error:", error);
          loader.style.display = "none";
          formSection.style.display = "block";  // Pokaż formularz, jeśli wystąpił błąd
      });
  }

  // Obsługuje kliknięcie przycisku
  document.querySelector("button").addEventListener("click", function () {
      sendData();
  });

  // Funkcja otwierająca odpowiednią zakładkę
  function openTab(platform) {
      // Lista platform
      const platforms = ['instagram', 'youtube', 'tiktok', 'twitch'];
      
      // Ukrywamy wszystkie zawartości
      platforms.forEach(function (platformName) {
          document.getElementById(platformName + '-content').style.display = 'none';
          document.getElementById(platformName + '-tab').classList.remove("active");
      });

      // Pokazujemy odpowiednią zakładkę i jej treść
      document.getElementById(platform + '-content').style.display = 'block';
      document.getElementById(platform + '-tab').classList.add("active");
  }

  // Nasłuchujemy na kliknięcia poszczególnych zakładek
  instagramTab.addEventListener("click", function () {
      openTab("instagram");
  });
  youtubeTab.addEventListener("click", function () {
      openTab("youtube");
  });
  tiktokTab.addEventListener("click", function () {
      openTab("tiktok");
  });
  twitchTab.addEventListener("click", function () {
      openTab("twitch");
  });

  // Exportowanie funkcji do globalnego zakresu
  window.openTab = openTab;
});
