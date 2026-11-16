var daysOfWeek = ["Mon", "Tues", "Wed", "Thur", "Fri"];
daysOfWeek.push("Sat");
daysOfWeek.unshift("Sun");
document.getElementById("days").textContent = daysOfWeek.join(" · ");
var html = "<table><thead><tr>";
for (var i = 0; i < daysOfWeek.length; i++) html += "<th>" + daysOfWeek[i] + "</th>";
html += "</tr></thead><tbody>";
for (var day = 1; day <= 30; day++) {
  if ((day - 1) % 7 === 0) html += "<tr>";
  html += "<td>" + day + "</td>";
  if (day % 7 === 0) html += "</tr>";
}
if (30 % 7 !== 0) { for (var blank = 0; blank < 7 - (30 % 7); blank++) html += "<td></td>"; html += "</tr>"; }
html += "</tbody></table>";
document.getElementById("calendar").innerHTML = html;
