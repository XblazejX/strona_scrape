document.addEventListener("DOMContentLoaded", function () {
  const startSection = document.getElementById("start-section");
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

  let baseFolder = ""; // nazwa folderu ustawiona w showForm

  // === NOWA FUNKCJA: przejście z ekranu startowego do formularza ===
  window.showForm = function () {
    baseFolder = document.getElementById("initial-name").value.trim();
    if (!baseFolder) {
      alert("Proszę podać nazwę.");
      return;
    }
    startSection.style.display = "none";
    formSection.style.display = "block";
  };

  // Funkcja wysyłająca dane z formularza do backendu
  window.sendData = function () {
    const instagramUsername = document.getElementById("input-instagram").value;
    const youtubeUsername = document.getElementById("input-youtube").value;
    const tiktokUsername = document.getElementById("input-tiktok").value;
    const twitchUsername = document.getElementById("input-twitch").value;

    // Pokaż loader
    loader.style.display = "block";
    formSection.style.display = "none";

    const data = {
      folder: baseFolder,
      instagram: instagramUsername,
      youtube: youtubeUsername,
      tiktok: tiktokUsername,
      twitch: twitchUsername
    };

    fetch("/run-scraper", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(profileData => {
      loader.style.display = "none";
      tabsSection.style.display = "block";

      if (profileData.instagram) {
        instagramTab.style.display = "inline-block";
        instagramContent.style.display = "block";
        document.getElementById("instagram-name").textContent = profileData.instagram.name;
        document.getElementById("instagram-link").href = profileData.instagram.url;
        instagramContent.querySelector('.profile-img').src = `/static/${baseFolder}/instagram.jpg`;
      }
      if (profileData.youtube) {
        youtubeTab.style.display = "inline-block";
        youtubeContent.style.display = "block";
        document.getElementById("youtube-name").textContent = profileData.youtube.name;
        document.getElementById("youtube-link").href = profileData.youtube.url;
        youtubeContent.querySelector('.profile-img').src = `/static/${baseFolder}/youtube.jpg`;
      }
      if (profileData.tiktok) {
        tiktokTab.style.display = "inline-block";
        tiktokContent.style.display = "block";
        document.getElementById("tiktok-name").textContent = profileData.tiktok.name;
        document.getElementById("tiktok-link").href = profileData.tiktok.url;
        tiktokContent.querySelector('.profile-img').src = `/static/${baseFolder}/tiktok.jpg`;
      }
      if (profileData.twitch) {
        twitchTab.style.display = "inline-block";
        twitchContent.style.display = "block";
        document.getElementById("twitch-name").textContent = profileData.twitch.name;
        document.getElementById("twitch-link").href = profileData.twitch.url;
        twitchContent.querySelector('.profile-img').src = `/static/${baseFolder}/twitch.jpg`;
      }

      openTab("instagram");
    })
    .catch(error => {
      console.error("Error:", error);
      loader.style.display = "none";
      formSection.style.display = "block";
    });
  };

  // Funkcja otwierająca odpowiednią zakładkę
  window.openTab = function (platform) {
    [
      'instagram',
      'youtube',
      'tiktok',
      'twitch'
    ].forEach(platformName => {
      document.getElementById(`${platformName}-content`).style.display = 'none';
      document.getElementById(`${platformName}-tab`).classList.remove('active');
    });

    document.getElementById(`${platform}-content`).style.display = 'block';
    document.getElementById(`${platform}-tab`).classList.add('active');
  };

  // Nasłuchiwanie kliknięć zakładek
  instagramTab.addEventListener('click', () => openTab('instagram'));
  youtubeTab.addEventListener('click', () => openTab('youtube'));
  tiktokTab.addEventListener('click', () => openTab('tiktok'));
  twitchTab.addEventListener('click', () => openTab('twitch'));
});
