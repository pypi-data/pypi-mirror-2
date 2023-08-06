// Hide .portal-bounty-program container BEFORE it will be loaded
// This will be done only for browser with javascript support.
$("<style type='text/css'>.portal-bounty-program .hidden{display:none;}</style>").appendTo("head");

function getRandomSubset(array, choice_num) {
    // Return randomly selected *choice_num* elements from the array.
    // Solution is based on the Fisher-Yates (Knuth) algorithm
    // (http://en.wikipedia.org/wiki/Fisher–Yates_shuffle).
    if (array.length <= choice_num)
        choice_num = array.length;

    var tmp, current, top = array.length;
    for(top=array.length-1; top>0 && top>=array.length-choice_num; --top) {
	current = Math.round(Math.random() * top);
	tmp = array[current];
	array[current] = array[top];
	array[top] = tmp;
    }
    return array.slice(array.length-choice_num,array.length)
};

$(document).ready(function() {
    var container = $(".portal-bounty-program ul");
    container.append( 
        $(getRandomSubset(container.children("li"), 5)).detach()
          .each(function(){
              $(this).removeClass('hidden');
        })
    ) 
});
