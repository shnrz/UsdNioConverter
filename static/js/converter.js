var input = document.getElementById("amount");
var input_label = document.getElementById("amount-label");
var result_label = document.getElementById("result-label");
var rate = document.getElementById("rate");
var usdnio = document.getElementById("usdnio");
var niousd = document.getElementById("niousd");

// function formatToCurrency(num){
//    return (num).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
// }

function handleInput(val) {
   var result = document.getElementById("result");
   if (!isNaN(val) && val != null && val != "" && val > 0) {
      // var amount = parseFloat(val.replace(",",""));
      // input.value = formatToCurrency(amount);
      let formatter = new Intl.NumberFormat('en-US', { localeMatcher: 'best fit', maximumFractionDigits: 2 });
      if (usdnio.checked) {
         result.value = formatter.format((parseFloat(val) * parseFloat(rate.innerText)));
      } else if (niousd.checked) {
         result.value = formatter.format((parseFloat(val) / parseFloat(rate.innerText)));
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
