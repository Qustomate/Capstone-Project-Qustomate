const mysql = require("mysql");

// buat konfigurasi koneksi database
const dbconn = mysql.createConnection({
    host: "34.101.211.200",
    user: "root",
    password: "001",
    database: "qustomate"
});

// buat koneksi ke database
dbconn.connect((err) => {
    if (err) throw err;
    console.log("Database connected.");
});

module.exports = dbconn;