var stringOne = new String("Test");
var stringTwo = "Test";
var stringThree = "Test";
var stringFour = new String("Test");
var dateOne = new Date();
document.getElementById("result").innerHTML =
  "typeof stringOne = " + typeof stringOne + "<br>typeof stringThree = " + typeof stringThree +
  "<br>stringOne == stringTwo: " + (stringOne == stringTwo) +
  "<br>stringOne == stringFour: " + (stringOne == stringFour) +
  "<br>stringOne === stringTwo: " + (stringOne === stringTwo) +
  "<br>stringTwo === stringThree: " + (stringTwo === stringThree) +
  "<p>Date hiện tại: " + dateOne.toLocaleString("vi-VN") + "</p>Math.PI = " + Math.PI +
  "<br>Math.sqrt(4) = " + Math.sqrt(4) + "<br>Math.random() = " + Math.random();
