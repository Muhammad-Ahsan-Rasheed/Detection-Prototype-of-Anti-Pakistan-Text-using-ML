  
           $(document).ready(function() {

            var counters = $(".count");
            var countersQuantity = counters.length;
            var counter = [];
            
            for (i = 0; i < countersQuantity; i++) {
              counter[i] = parseInt(counters[i].innerHTML);
            }
            
            var count = function(start, value, id) {
              var localStart = start;
              setInterval(function() {
                if (localStart < value) {
                  localStart++;
                  counters[id].innerHTML = localStart;
                }
              }, 40);
            }
            
            for (j = 0; j < countersQuantity; j++) {
              count(0, counter[j], j);
            }
            });


            
  $('.count').each(function () {
         $(this).prop('Counter',0).animate({
         Counter: $(this).text()
         }, {
         duration: 3300,
         easing: 'swing',
         step: function (now) {
             $(this).text(Math.ceil(now));
         }
         });
         });
         /*******/
