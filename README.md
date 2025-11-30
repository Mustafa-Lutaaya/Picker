# Picker 

Being a Web-Dev-Fundamentals end of semester Final Project aside, Picker is a warehouse management dashboard designed to help Pickers / Commissioners sort goods in "Pallet-Loading" correct order.

## Description

Once it retrieves the day's loading lists from Dispo, it sorts them in "Pallet-Loading" order i.e. from biggest size to lowest size.

The Picker can then decide to either print the sorte3d list out or just use the dashboard on a tablet to do work.


## Features

- **Date-Based Search** - Search for loading lists by delivery date and date validation
- **Smart Date Validation** - Prevents selection of past dates, today's date, and dates beyond the next valid delivery window
- **Pallet Organization** - View only important pallet information including customer name and total weight
- **Item Details** - Display only important information for each item including storage location, dimensions, type, direction, and quantity
- **Item Sorting** - Sorts goods by type , then by height and width for optimal warehouse organization
- **Print Functionality** - Generates clean, printer-friendly lists of sorted goods for pickers
- **Real-Time Display** - Live date and time display in German format (24-hour clock)
- **Responsive Design** - Fully responsive layout for desktop, tablet, and mobile devices
- **Error Handling** - Comprehensive error messages and loading states during API calls


## Tech Stack

- **HTML5** - App structure
- **CSS3** - Custom styling with flexbox, media queries, and print styles
- **JavaScript (ES6+)** - Modern JavaScript with functions & classes
- **Fetch API** - For asynchronous API calls to backend services
- **Object-Oriented Programming** - Ware and Pallet classes for data management


## Setup

1. **Backend API**
   - The application connects to: `https://klappt-holz.onrender.com/ladelist`

2. **Font Setup**
   - Required fonts: `clacon2.ttf` and `unifont-17.0.03.otf`

3. **Open in Browser**
   - Open `index.html` in a web browser
   - No build process or dependencies required


## Usage Guide
- Enter a date

- Click 'Such'

- See pallets + items on the left

- Click 'Sortirien'

- See sorted list on the right

- Click 'Drucken'

### Understanding the Display

- **Pallet Header** - Shows pallet number, customer name, and total weight
- **Item Details**
  - Line 1: Item number, storage location, mark, type (Tür/Zarge)
  - Line 2: Direction, dimensions (width × height), wall thickness (if applicable), quantity

---
**Language**: German (DE)  
**Theme**: Dark mode with purple accent colors.

Designed by Mustafa Lutaaya