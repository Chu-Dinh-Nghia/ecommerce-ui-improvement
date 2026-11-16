var countries = [
  { name: "Bahamas", iso: "BS", capital: "Nassau", population: 393248 },
  { name: "Canada", iso: "CA", capital: "Ottawa", population: 38929902 },
  { name: "Germany", iso: "DE", capital: "Berlin", population: 84358845 },
  { name: "Spain", iso: "ES", capital: "Madrid", population: 48592809 },
  { name: "United Kingdom", iso: "GB", capital: "London", population: 68599599 },
  { name: "United States", iso: "US", capital: "Washington, D.C.", population: 340110988 }
];
var html = "";
for (var i = 0; i < countries.length; i++) {
  var c = countries[i];
  var temp = "name";
  html += "<article class='country'><h3><img src='flags/" + c.iso + ".png' alt='Cờ " + c.name + "'> " + c[temp] + "</h3>";
  for (var propertyName in c) html += "<strong>" + propertyName + ":</strong> " + c[propertyName] + "<br>";
  html += "</article>";
}
document.getElementById("countries").innerHTML = html;
