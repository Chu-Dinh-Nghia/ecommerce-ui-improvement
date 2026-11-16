var isCanadian = true;
function calculateTax(amount, taxRate) { return amount * taxRate(); }
function calculateTotal(price, quantity) {
  var amount = price * quantity;
  return amount + calculateTax(amount, function () { return isCanadian ? 0.05 : 0; });
}
document.getElementById("calculate").addEventListener("click", function () {
  var price = Number(document.getElementById("price").value);
  var quantity = Number(document.getElementById("quantity").value);
  document.getElementById("result").textContent = "Tổng gồm thuế 5%: $" + calculateTotal(price, quantity).toFixed(2);
});
document.getElementById("calculate").click();
