function set_slogan() {
  var slogans = [
    'Husk lige de ristede løg!',
    'Det er bare en burger!',
    'Hvorfor oste-pive når du kan oste-skive?',
    'Aubergine i min burger?  Hvorfor ikke!',
    'burge: verbum (burger, burgede, burget)',
    '50000 burgere, tak!'
  ],
      slogan = slogans[Math.floor(Math.random() * slogans.length)];

  document.getElementById('slogan').innerHTML = slogan;
}

window.onload = function() {
  set_slogan();

  window.onfocus = set_slogan;
};
