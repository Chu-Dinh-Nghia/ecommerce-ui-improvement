var boxClass = "movingDiv";
function outputBox(num) {
  var box = "<div class='" + boxClass + "' id='div" + num + "'>This is div " + num + "</div>";
  return box;
}
var boxes = "";
for (var count = 1; count < 6; count++) boxes += outputBox(count);
document.getElementById("boxes").innerHTML = boxes;
document.getElementById("scope").textContent = "Biến box là biến cục bộ của outputBox; typeof window.box = " + typeof window.box + ".";
