var carouselBox = document.querySelector('.carouselbox');
// Let CSS know to condense box size to only one item in the list
carouselBox.classList.add('active');

var nextButton = carouselBox.querySelector('.next');
var prevButton = carouselBox.querySelector('.prev');
var addButton = document.querySelector('.addItem');

var listItems = carouselBox.querySelectorAll('.content li');
var currentItemIndex = 0;

function addListItem() {
document.querySelector('.carouselbox').querySelector('.content').innerHTML += '<li>' + (listItems.length + 1) + '</li>'

// Update references to reflect new item, probably not the best way to handle this
listItems = carouselBox.querySelectorAll('.content li');
currentItem = listItems[currentItemIndex];
}

// Initially populate list with numbers 1 through 5
for (var i = 0; i < 5; i++) {
addListItem();
}

// Set add button to append to the list items
addButton.addEventListener('click', function(ev) {
addListItem();
});

// Navigate through the carousel
function navigate(moveForward) {
// Stop current list item from being displayed
currentItem.classList.remove('current');

if (moveForward) {
currentItemIndex++
} else {
currentItemIndex--;
}

// If we're moving forward and there is no next item, loop back around
if (moveForward && !listItems[currentItemIndex]) { 
currentItemIndex = 0;
}

// If we're moving backwards and there is no previous item, loop back around
if (!moveForward && currentItemIndex < 0) { 
currentItemIndex = listItems.length - 1; 
}

// Set new current item by modifying its class list so CSS knows to display it
currentItem = listItems[currentItemIndex];
currentItem.classList.add('current');
}

// Set up buttons to navigate the carousel
nextButton.addEventListener('click', function(ev) {
navigate(true);
});
prevButton.addEventListener('click', function(ev) {
navigate(false);
});

// Show the current element initially
var currentItem = listItems[currentItemIndex];
currentItem.classList.add('current');