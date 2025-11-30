// Function to display the date
function Heute(){
    // Creates a new Date object containing the current date & time
    const Today = new Date();

    // Finds the HTML element with id="time" and sets its content.
    document.getElementById("date").innerHTML =Today.toLocaleDateString( //  toLocaleTimeString() formats the Date according to a specific language/region
        // Formats the date using German rules
        "de-DE", {
            // Format options to show a full weekday name, 4-digit year, full month name and numeric day of the month
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric" 
        }
    );
}
Heute() // Function call to display on page load

// An Arrow Function to display the current time 
const Uhrzeit = () => {

    // Creates a new Date object containing the current date & time
    const Now = new Date(); 
    
    // Finds the HTML element with id="time" and updates its content.
    document.getElementById("time").innerHTML = Now.toLocaleTimeString( //  toLocaleTimeString() converts the Date object into a formatted time string based on a chosen language/region.
        // "de-DE" means German formatting thus 24-hour clock & German separators
        "de-DE", {
            // Format options to show hours, minutes and seconds as 2 digits
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit"
        });
};

Uhrzeit() // Function Call to display on page load
setInterval(Uhrzeit, 1000); // Calls the function every 1000 milliseconds / 1 second to update in real time

// Event Listening on Form submit
document.getElementById("dataForm").addEventListener("submit", function(event){
    event.preventDefault(); // Prevents form from reload during submit

    const inputDate = document.getElementById("deliveryDate").value;

    // Ensures a date is entered
    if(!inputDate){
        alert("Bitte gib das Datum ein");
        return;
    }

    // Converts input string into a Date Object & initializes a new onject for now
    const selectedDate = new Date(inputDate);
    const today = new Date();

    // Zeroes out the time part of the date to enforce comparisons only by day
    today.setHours(0,0,0,0);
    selectedDate.setHours(0,0,0,0);

    const weekDay = today.getDay(); // Returns a number for todays weekday

    // Weekend Automatic Handling
    let validDate = new Date(today);

    if(weekDay === 5){
        validDate.setDate(today.getDate() + 3);
    } else {
        validDate.setDate(today.getDate() + 1);
    }

    // Date Validation Checks 
    // If the selected date is in the past
    if (selectedDate < today){
        alert("Datum liegt in der Vergangenheit. Nicht erlaubt.");
        return;
    // If the selected date is today
    } else if (selectedDate.getTime() === today.getTime()){
        alert("Wähle das richtige Lieferdatum. Heute ist nicht erlaubt.");
        return;
    // If the selected date is later than the next valid delivery day
    } else if  (selectedDate.getTime() > validDate.getTime()) {
        alert("Datum liegt zu weit in der Zukunft.");
        return;
    // If the selected date is earlier than the next valid delivery day
    } else if (selectedDate.getTime() < validDate.getTime()) {
        alert("Falsches Datum gewählt. Wähle den nächsten gültigen Liefertermin.");
        return;
    } else {
        alert("Gültiges Lieferdatum");
    }
})