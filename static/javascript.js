/*
##### NOTES #####

Ethan Ryoo taught me the basic syntax of Javascript including how to make
variables, functions and most importantly, the document.getElementsBy....()
methods. I learnt from the Internet and some of my friends about the usage of
localStorage which allowed me to implement this slice of JS into my project.
This was my first time ever using Javascript and I'm quite happy with it. :D

* The syntax of the for loop was honestly the trickiest thing as it is quite
different from Python!

##### NOTES #####
*/

// This code block allows checkboxes to be checked without submitting a form
// and persists the state of a checkbox on page reload or server turning off.
let checkboxes = document.getElementsByClassName("checkboxes");

function save() {
  // This function saves checked checkboxes to localStorage.
  for (let checkbox of checkboxes) {
    if (checkbox.id.startsWith("Daily")) {
      localStorage.setItem("checkbox" + checkbox.id, checkbox.checked);
    } else if (checkbox.id.startsWith("Weekly")) {
      localStorage.setItem("checkbox" + checkbox.id, checkbox.checked);
    }
  }
}

for (let checkbox of checkboxes) {
  if (localStorage.length > 0) {
    var checked = JSON.parse(localStorage.getItem("checkbox" + checkbox.id));
    if (checked) {
      checkbox.checked = checked;
    }
  }
}

window.addEventListener("change", save);

// The code block below automatically unchecks boxes depending on if the task
// resets daily or weekly.
const ResetHour = 20;
const ResetMinute = 0;
const ResetSecond = 0;
const weeklyResetDay = 3;

setInterval(reset, 1000);

function reset() {
  /* This function repeatedly sets the current Day, Hour, Minute and Second
    every second and matches it to our constants declared above. If they match,
    the checkbox is removed from localStorage and reset to default settings.
    */
  var currentDate = new Date();
  var currentDay = currentDate.getDay();
  var currentHour = currentDate.getHours();
  var currentMinute = currentDate.getMinutes();
  var currentSecond = currentDate.getSeconds();

  if (
    currentHour == ResetHour &&
    currentMinute == ResetMinute &&
    currentSecond == ResetSecond
  ) {
    for (let checkbox of checkboxes) {
      if (checkbox.id.startsWith("Daily")) {
        localStorage.removeItem("checkbox" + checkbox.id);
      }
    }
    location.reload();
  }

  if (
    currentDay == weeklyResetDay &&
    currentHour == ResetHour &&
    currentMinute == ResetMinute &&
    currentSecond == ResetSecond
  ) {
    for (let checkbox of checkboxes) {
      if (checkbox.id.startsWith("Weekly")) {
        localStorage.removeItem("checkbox" + checkbox.id);
      }
    }
    location.reload();
  }
}
