// LibreWolf user.js – von chezmoi verwaltet.
// Liegt als ~/.librewolf/user.js und wird von allen Profilen per Symlink
// eingebunden. Änderungen: Datei editieren, dann `chezmoi apply` + commit,
// danach LibreWolf neu starten.

// Beispiel: Downloads immer erst fragen
user_pref("browser.download.useDownloadDir", false);

// Beispiel: Suchleiste in die Symbolleiste
user_pref("browser.search.widget.inNavBar", true);

// Beispiel: Telemetrie aus
user_pref("toolkit.telemetry.enabled", false);

// Beispiel: Doppelte Tabs verhindern
user_pref("browser.urlbar.maxRichResults", 10);
