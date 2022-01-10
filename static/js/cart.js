var updatebtn1 = document.getElementsByClassName("updated-cart1");
var removebtn = document.getElementsByClassName("remove-cart");

var ColorSelector = document.getElementById("SingleOptionSelector-0");
var SizeSelector = document.getElementById("SingleOptionSelector-1");

CartUpdate(updatebtn1);
CartUpdate(removebtn);

function CartUpdate(updatedbtn) {
  var i;

  for (i = 0; i < updatedbtn.length; i++) {
    updatedbtn[i].addEventListener("click", function () {
      var productId = this.dataset.productId;
      var action = this.dataset.action;

      if (User === "AnonymousUser") {
        console.log("User is not logged in");
      } else {
        let product_size = SizeSelector.value;
        let product_color = ColorSelector.value;
        let quantity;

        if (this.id == "add-item1") {
          quantity = document.getElementById("quantity" + productId).value;
          UpdateOrder(productId, quantity, action, product_size, product_color);
        }
        else if (this.id == "remove-item2") {
          quantity = 1;
          UpdateOrder(productId, quantity, action, product_size, product_color);
        } else {
          quantity = 1;
          UpdateOrder(productId, quantity, action, product_size, product_color);
        }
      }
    });
  }
}

// Sent data database
function UpdateOrder(productId, quantity, action, product_size, product_color) {
  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      productId: productId,
      quantity: quantity,
      action: action,
      product_size: product_size,
      product_color: product_color,
    }),
  })
    .then((response) => {
      location.reload();
    })
}
