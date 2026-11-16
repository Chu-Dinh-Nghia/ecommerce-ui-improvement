var count = 2;
var output = "Count = " + count;
var temp = count * 7;
document.getElementById("result").textContent = output + " · temp = " + temp;
document.getElementById("inspect").addEventListener("click", function () {
  console.log("script within the page", { count: count, output: output, temp: temp });
  console.warn("Đây là cảnh báo minh họa từ Exercise 8.5.");
  console.error("Đây là lỗi demo được tạo có chủ đích.");
});
document.getElementById("error").addEventListener("click", function () {
  try { throw new Error("Lỗi minh họa: hãy kiểm tra stack trace trong Console."); }
  catch (error) { console.error(error); }
});
