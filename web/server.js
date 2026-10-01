// Panel admin de VulnShop en Express, con vulnerabilidades intencionales.
const express = require('express');
const { exec } = require('child_process');
const _ = require('lodash');

const app = express();
app.use(express.json());

// Ejecución de código arbitrario
app.get('/admin/eval', (req, res) => {
  const result = eval(req.query.code);
  res.send(String(result));
});

// Command injection
app.get('/admin/logs', (req, res) => {
  exec('tail -n 50 /var/log/' + req.query.file, (err, stdout) => {
    res.send(stdout);
  });
});

// XSS reflejado
app.get('/admin/welcome', (req, res) => {
  res.send('<h1>Bienvenido ' + req.query.user + '</h1>');
});

// Open redirect
app.get('/admin/redirect', (req, res) => {
  res.redirect(req.query.url);
});

// Prototype pollution (lodash 4.17.15)
app.post('/admin/settings', (req, res) => {
  const settings = _.merge({}, req.body);
  res.json(settings);
});

app.listen(3000, () => console.log('admin en :3000'));
