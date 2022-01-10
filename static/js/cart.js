var updatebtn1 = document.getElementsByClassName("updated-cart1");
var updatebtn2 = document.getElementsByClassName("updated-cart2");
var removebtn = document.getElementsByClassName("remove-cart");

var ColorSelector = document.getElementById("SingleOptionSelector-0");
var SizeSelector = document.getElementById("SingleOptionSelector-1");

CartUpdate(updatebtn1);
CartUpdate(updatebtn2);
CartUpdate(removebtn);

function CartUpdate(updatedbtn) {
  var i, j;

  for (i = 0; i < updatedbtn.length; i++) {
    updatedbtn[i].addEventListener("click", function () {
      var productId = this.dataset.productId;
      var action = this.dataset.action;

      if (User === "AnonymousUser") {
        console.log("User is not logged in");
      } else {
        let quantity, qty;

        let add_cart = document.getElementById("add-cart1");
        let add_cart2 = document.getElementById("add-cart2");
        let add_cart3 = document.getElementById("add-cart3");
        let add_cart4 = document.getElementById("add-cart4");
        let remove_cart = document.getElementById("remove-cart-button");
        let remove_cart2 = document.getElementById("remove-cart-button2");

        if (this.id == "add-item1") {
          quantity = document.getElementById("quantity" + productId).value;
          AddCart(add_cart, add_cart2, remove_cart, (qty = quantity), this.id);
        } else if (this.id == "add-item2") {
          quantity = document.getElementById("quantity2" + productId).value;
          AddCart(add_cart3, add_cart4, remove_cart, (qty = quantity), this.id);
        } else if (this.id == "remove-item2") {
          quantity = 1;
          RemoveCart(add_cart3, add_cart4, remove_cart2);
        } else {
          quantity = 1;
          RemoveCart(add_cart3, add_cart4, remove_cart);
        }

        let product_size = SizeSelector.value;
        let product_color = ColorSelector.value;

        UpdateOrder(productId, quantity, action, product_size, product_color);
      }
    });
  }
}

// Add cart
function AddCart(add_cart1, add_cart2, remove_cart, qty, itemId) {
  remove_cart.classList.remove("d-none");
  add_cart1.classList.add("d-none");
  add_cart2.classList.add("d-none");
  AddMiniCart(qty, itemId);
}

// Add minicart item cart sidebar
function AddMiniCart(qty, itemId) {
  let minicart_qty1 = document.querySelector(".minicart-qty1").innerText;
  let add_qty = parseInt(minicart_qty1) + 1;

  document.querySelector(".minicart-qty1").innerText = add_qty;
  document.querySelector(".minicart-qty2").innerText = add_qty;

  var regex = /\d+/g;
  var now_price = newPrice.match(regex);

  let add_total = Number(totalPrice) + qty * parseInt(now_price[0]);

  document.querySelector(".minicart-total1").innerText = "$" + add_total;
  document.querySelector(".minicart-total2").innerText = "$" + add_total;

  if (itemId == "add-item2") {
    document.querySelector(".minicart-drop-total-price").innerText =
      "$" + add_total;
  } else if (itemId == "add-item1") {
    document.getElementById("minicartEmpty").classList.add("d-none");

    document.getElementById("minicartDropFixed").classList.remove("d-none");

    document.querySelector(".minicart-drop-total-price").innerText =
      "$" + add_total;
  }
 
  document.getElementById("minicartItem").classList.remove("d-none");
  const img = document.getElementById("minicartItemImg");
  img.setAttribute("data-src", imageurl);
  document.getElementById("minicartTitle").innerText = title;
  document.getElementById("minicartQty").innerText = qty;
  document.getElementById("minicartOld").innerText = oldPrice;
  document.getElementById("minicartNew").innerText = newPrice;
}

// Remove cart
function RemoveCart(add_cart1, add_cart2, remove_cart) {
  remove_cart.classList.add("d-none");
  add_cart1.classList.remove("d-none");
  add_cart2.classList.remove("d-none");
  RemoveItem();
}

// Remove minicart item from cart sidebar
function RemoveItem() {
  
  document.querySelector("#minicartItem").classList.add("d-none");

  let minicart_qty1 = document.querySelector(".minicart-qty1").innerText;
  let add_qty = parseInt(minicart_qty1) - 1;

  document.querySelector(".minicart-qty1").innerText = add_qty;
  document.querySelector(".minicart-qty2").innerText = add_qty;

  document.querySelector(".minicart-total1").innerText = "$" + totalPrice;
  document.querySelector(".minicart-total2").innerText = "$" + totalPrice;

  document.querySelector(".minicart-drop-total-price").innerText =
    "$" + totalPrice;
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
      // location.reload();
      console.log(response);
    })
    .then((data) => {
      console.log(data);
    });
}
