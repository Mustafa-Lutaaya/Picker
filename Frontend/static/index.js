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
