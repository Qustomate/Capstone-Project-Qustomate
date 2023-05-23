const express = require("express");
const router = express.Router();

const db = require("../config/database");

router.get('/user/:id', (req, res) => {
    const id_user = req.params.id;
    const sql = 'SELECT * FROM user WHERE id_user = ?';
  
    db.query(sql, [id_user], (err, result) => {
      if (err) {
        throw err;
      }
      res.json(result);
    });
  });
  
  router.get('/', (req, res) => {
    res.send('Hello World!')
  })


module.exports = router;