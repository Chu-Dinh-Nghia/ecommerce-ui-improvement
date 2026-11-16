var sampleOrder = {};
sampleOrder["product"] = "Self Portrait in a Straw Hat";
sampleOrder["price"] = 15.0;
sampleOrder["quantity"] = 2;
sampleOrder["total"] = function () { return this.price * this.quantity; };
document.getElementById("access").textContent = "Object rỗng + bracket notation: " + sampleOrder.product + " · total() = $" + sampleOrder.total();
function Order(product, price, quantity) {
  this.product = product;
  this.price = price;
  this.quantity = quantity;
  this.total = function () { return this.price * this.quantity; };
  this.output = function () {
    return "<p><strong>Product:</strong> " + this.product + "<br><strong>Price:</strong> $" + this.price.toFixed(2) +
      "<br><strong>Quantity:</strong> " + this.quantity + "<br><strong>Total:</strong> $" + this.total().toFixed(2) + "</p>";
  };
}
var example1 = new Order("Self Portrait in a Straw Hat", 15, 2);
var example2 = new Order("Untitled #23", 10, 4);
document.getElementById("orders").innerHTML = example1.output() + example2.output();
