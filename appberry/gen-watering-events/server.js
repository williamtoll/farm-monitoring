// server.js
const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Serve static files (like FullCalendar CSS and JS)
app.use('/', express.static(path.join(__dirname, 'frontend')));

// Serve the frontend HTML
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/index.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`Frontend running at http://localhost:${PORT}`);
});