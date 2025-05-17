document.addEventListener("DOMContentLoaded", function () {
  const startSection = document.getElementById("start-section");
  const formSection  = document.getElementById("form-section");
  const tabsSection  = document.getElementById("tabs-section");
  const loader       = document.getElementById("loader");

  const instagramTab = document.getElementById("instagram-tab");
  const youtubeTab   = document.getElementById("youtube-tab");
  const tiktokTab    = document.getElementById("tiktok-tab");
  const twitchTab    = document.getElementById("twitch-tab");

  const instagramContent = document.getElementById("instagram-content");
  const youtubeContent   = document.getElementById("youtube-content");
  const tiktokContent    = document.getElementById("tiktok-content");
  const twitchContent    = document.getElementById("twitch-content");

  let baseFolder = "";

  // Na start pokaż tylko prośbę o nazwę użytkownika
  startSection.style.display = "block";
  formSection.style.display  = "none";
  tabsSection.style.display  = "none";
  loader.style.display       = "none";

  window.showForm = function () {
    baseFolder = document.getElementById("initial-name").value.trim();
    if (!baseFolder) {
      alert("Proszę podać nazwę.");
      return;
    }

    fetch("/check-folder", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ folder: baseFolder })
    })
    .then(res => res.json())
    .then(({ exists, available }) => {
      if (exists) {
        startSection.style.display = "none";
        formSection.style.display  = "none";
        tabsSection.style.display  = "block";

        // Ukryj wszystkie zakładki i treści na start
        ["instagram", "youtube", "tiktok", "twitch"].forEach(p => {
          document.getElementById(`${p}-tab`).style.display = "none";
          document.getElementById(`${p}-content`).style.display = "none";
        });

        // Załaduj dane z pliku dane.js dynamicznie, aby mieć profileData
        const script = document.createElement("script");
        script.src = `/static/${baseFolder}/dane.js`;
        script.onload = () => {
          // Po załadowaniu profileData pokaz taby i uzupełnij dane
          available.forEach(platform => {
            const tabBtn  = document.getElementById(`${platform}-tab`);
            const content = document.getElementById(`${platform}-content`);
            const imgEl   = content.querySelector(".profile-img");
            const nameEl  = document.getElementById(`${platform}-name`);
            const linkEl  = document.getElementById(`${platform}-link`);

            tabBtn.style.display     = "inline-block";
            content.style.display    = "block";
            imgEl.src                = `/static/${baseFolder}/${platform}.jpg`;

            if (window.profileData && window.profileData[platform]) {
              nameEl.textContent = window.profileData[platform].name;
              linkEl.href = window.profileData[platform].url;
              linkEl.target = "_blank";
            } else {
              nameEl.textContent = "";
              linkEl.href = "#";
            }
          });

          if (available.length) openTab(available[0]);
        };
        script.onerror = () => {
          alert("Nie udało się załadować danych profilu.");
        };
        document.body.appendChild(script);

      } else {
        startSection.style.display = "none";
        formSection.style.display  = "flex";
        tabsSection.style.display  = "none";
      }
    })
    .catch(err => {
      console.error("Błąd podczas sprawdzania folderu:", err);
      alert("Wystąpił błąd. Spróbuj ponownie.");
    });
  };

  window.sendData = function () {
    const instagramUsername = document.getElementById("input-instagram").value.trim();
    const youtubeUsername   = document.getElementById("input-youtube").value.trim();
    const tiktokUsername    = document.getElementById("input-tiktok").value.trim();
    const twitchUsername    = document.getElementById("input-twitch").value.trim();

    if (!instagramUsername && !youtubeUsername && !tiktokUsername && !twitchUsername) {
      alert("Proszę podać przynajmniej jedną nazwę użytkownika.");
      return;
    }

    loader.style.display      = "block";
    formSection.style.display = "none";

    const data = {
      folder:    baseFolder,
      instagram: instagramUsername || null,
      youtube:   youtubeUsername || null,
      tiktok:    tiktokUsername || null,
      twitch:    twitchUsername || null
    };

    fetch("/run-scraper", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(profileData => {
      loader.style.display      = "none";
      tabsSection.style.display = "block";

      // Ukryj wszystkie zakładki i treści na start
      ["instagram", "youtube", "tiktok", "twitch"].forEach(p => {
        document.getElementById(`${p}-tab`).style.display = "none";
        document.getElementById(`${p}-content`).style.display = "none";
      });

      if (profileData.instagram) {
        instagramTab.style.display              = "inline-block";
        instagramContent.style.display          = "block";
        document.getElementById("instagram-name").textContent = profileData.instagram.name;
        document.getElementById("instagram-link").href        = profileData.instagram.url;
        document.getElementById("instagram-link").target      = "_blank";
        instagramContent.querySelector(".profile-img").src    = `/static/${baseFolder}/instagram.jpg`;
      }
      if (profileData.youtube) {
        youtubeTab.style.display             = "inline-block";
        youtubeContent.style.display         = "block";
        document.getElementById("youtube-name").textContent = profileData.youtube.name;
        document.getElementById("youtube-link").href        = profileData.youtube.url;
        document.getElementById("youtube-link").target      = "_blank";
        youtubeContent.querySelector(".profile-img").src    = `/static/${baseFolder}/youtube.jpg`;
      }
      if (profileData.tiktok) {
        tiktokTab.style.display              = "inline-block";
        tiktokContent.style.display          = "block";
        document.getElementById("tiktok-name").textContent = profileData.tiktok.name;
        document.getElementById("tiktok-link").href        = profileData.tiktok.url;
        document.getElementById("tiktok-link").target      = "_blank";
        tiktokContent.querySelector(".profile-img").src    = `/static/${baseFolder}/tiktok.jpg`;
      }
      if (profileData.twitch) {
        twitchTab.style.display              = "inline-block";
        twitchContent.style.display          = "block";
        document.getElementById("twitch-name").textContent = profileData.twitch.name;
        document.getElementById("twitch-link").href        = profileData.twitch.url;
        document.getElementById("twitch-link").target      = "_blank";
        twitchContent.querySelector(".profile-img").src    = `/static/${baseFolder}/twitch.jpg`;
      }

      // Otwórz pierwszą dostępną zakładkę
      const firstPlatform = ["instagram", "youtube", "tiktok", "twitch"].find(p => profileData[p]);
      if (firstPlatform) openTab(firstPlatform);
    })
    .catch(err => {
      console.error("Error:", err);
      loader.style.display      = "none";
      formSection.style.display = "flex";
      alert("Wystąpił błąd podczas pobierania danych.");
    });
  };

  window.openTab = function (platform) {
    ["instagram","youtube","tiktok","twitch"].forEach(p => {
      document.getElementById(`${p}-content`).style.display = "none";
      document.getElementById(`${p}-tab`).classList.remove("active");
    });
    document.getElementById(`${platform}-content`).style.display = "block";
    document.getElementById(`${platform}-tab`).classList.add("active");
  };

  instagramTab.addEventListener("click", () => openTab("instagram"));
  youtubeTab.addEventListener("click", () => openTab("youtube"));
  tiktokTab.addEventListener("click", () => openTab("tiktok"));
  twitchTab.addEventListener("click", () => openTab("twitch"));
});
