const result = document.getElementById("result");
result.innerHTML = "this text was written from JS<br>Count = 1<br>Count = 2";
var count = 2;
var output = "Count đã tăng lên " + count + " sau phép count++.";
result.insertAdjacentHTML("beforeend", "<p>" + output + "</p>");
