# Temperature Log Visualization Software Specification

## 1. Overview

This specification describes a web-based visualization tool for temperature log data. The application allows users to load, visualize, and analyze temperature data from log files with an interactive time-series graph featuring zoom capabilities.

## 2. Input Data Format

### 2.1 Log File Structure
- Plain text file format (.log or .txt)
- One measurement per line
- Line format: `YYYY-MM-DD_HH:mm:ss  temp=XX.X'C`
  - Date and time separated by underscore
  - Two spaces between timestamp and temperature
  - Temperature in Celsius with one decimal place
  - Temperature format: "temp=" prefix and "'C" suffix

Example log entry:
```
2025-02-03_10:33:35  temp=52.1'C
```

## 3. User Interface Requirements

### 3.1 Control Elements
1. File Selection Button
   - Label: "Select File"
   - Icon: File upload symbol
   - Opens native file system dialog
   - Accepts .log and .txt files

2. Reset Zoom Button
   - Label: "Reset Zoom"
   - Icon: Zoom out symbol
   - Initially disabled
   - Enabled only when view is zoomed
   - Returns view to full data range when clicked

### 3.2 Information Display
1. File Information Banner
   - Shows selected filename
   - Displays total number of data points loaded
   - When zoomed: Shows number of visible data points

### 3.3 Graph Display
1. Main Chart Area
   - Width: Responsive, fills container
   - Height: 600 pixels
   - Border: 1 pixel, light gray
   - Border radius: 8 pixels
   - Padding: 16 pixels

2. Axes
   - X-axis: Time
     - Labels rotated -45 degrees
     - Maximum 10 time labels visible
     - Automatically adjusts label density based on data range
   - Y-axis: Temperature
     - Label: "Temperature (°C)"
     - Vertical orientation (-90 degrees)
     - Positioned on left side
     - Scale adjusts to data range

3. Data Line
   - Color: Red
   - No data points displayed (continuous line)
   - Tooltips show exact values on hover

## 4. Interaction Specifications

### 4.1 File Loading
1. On file selection:
   - Clear previous data
   - Parse new file content
   - Display full data range
   - Reset any active zoom
   - Update file information display
   - Handle and display any parsing errors

### 4.2 Zoom Functionality
1. Zoom Selection
   - Activated by mouse down on chart area
   - Blue semi-transparent overlay (color: #8884d8, opacity: 0.3)
   - Overlay must appear immediately on mouse down
   - Overlay extends from initial click point to current mouse position
   - Selection area must be visible in both zoomed and unzoomed states

2. Zoom Execution
   - Triggered on mouse up
   - View updates to show only selected time range
   - Both axes scale to fit selected data
   - Minimum zoom range: 2 data points

3. Zoom Reset
   - Returns to full data range
   - Maintains same data resolution
   - Disables reset button if no zoom active

## 5. Data Processing

### 5.1 Data Parsing
1. Parse each line:
   - Extract timestamp (convert to Date object)
   - Extract temperature value (convert to float)
   - Skip empty lines
   - Skip malformed lines (log warning)
   - Maintain original data point order

2. Data Storage Format
   ```typescript
   interface DataPoint {
     name: string;          // Formatted date string
     temperature: number;   // Temperature value
     originalIndex: number; // Position in original dataset
   }
   ```

### 5.2 Zoom Data Management
1. Maintain two data sets:
   - Complete dataset (all points)
   - Zoomed dataset (visible points)
2. Track zoom state:
   - Start and end indices
   - Original indices for nested zooming

## 6. Performance Requirements

1. Loading
   - Handle files with 10,000+ data points
   - Support real-time file updates
   - Maintain responsive UI during load

2. Interaction
   - Smooth zoom selection overlay
   - Immediate response to zoom reset
   - Fluid pan and zoom operations

## 7. Error Handling

1. File Loading Errors
   - Display user-friendly error messages
   - Maintain application state on error
   - Clear invalid data

2. Data Parsing Errors
   - Skip invalid lines
   - Continue processing valid data
   - Log parsing errors (not visible to user)

## 8. Constraints

1. Browser Security
   - File access only through user selection
   - No direct filesystem access
   - Fresh file read required for updates

2. Display
   - Support modern web browsers
   - Responsive design
   - Minimum width: 800 pixels
   - Minimum height: 600 pixels
