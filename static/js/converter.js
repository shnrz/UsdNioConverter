var input = document.getElementById("amount");
var input_label = document.getElementById("amount-label");
var result_label = document.getElementById("result-label");
var rate = document.getElementById("rate");

function handleInput(val) {
   var result = document.getElementById("result");
   if (!isNaN(val) && val != null && val != "" && val > 0) {
      var usdnio = document.getElementById("usdnio");
      var niousd = document.getElementById("niousd");
      if (usdnio.checked) {
         result.value = (parseFloat(val) * parseFloat(rate.innerText)).toFixed(2).toString();
      } else if (niousd.checked) {
         result.value = (parseFloat(val) / parseFloat(rate.innerText)).toFixed(2).toString();
      }
   } else {
      result.value = "0";
   }
}

usdnio.addEventListener("change", handleRadioClick);
niousd.addEventListener("change", handleRadioClick);

function handleRadioClick() {
   if (usdnio.checked) {
      input_label.innerText = "Monto: (USD $ dólares)";
      result_label.innerText = "Equivalente a: (NIO C$ córdobas)";
   } else if (niousd.checked) {
      input_label.innerText = "Monto: (NIO C$ córdobas)";
      result_label.innerText = "Equivalente a: (USD $ dólares)";
   }
   handleInput(parseFloat(input.value));
}
