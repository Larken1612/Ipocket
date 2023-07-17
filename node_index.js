const { exec } = require('child_process')
const bodyParser = require('body-parser')
const express = require('express')
const cors = require('cors')
const fs = require('fs')
const app = express()
const port = 8000

app.use(bodyParser.json())
app.use(cors())

const jsonFilePath = './input.json'
const pythonFilePath = './generator.py'

app.get('/', (req, res) => {
    res.send('Oke xong')
})
  
app.post('/', (req, res) => {
    const inputData = req.body

    const jsonDataString = JSON.stringify(inputData)
    
    fs.writeFileSync(jsonFilePath, jsonDataString, 'utf-8')

    console.log(inputData)

    pyProcess = exec(`python ${pythonFilePath}`)

    pyProcess.on('exit', (code, signal) => {
      if (code === 0) {
        res.send('Chạy file python thành công')
      } else {
        res.status(500).send('Chạy file python không thành công')
      }
    })
})

app.listen(port, () => console.log('App listening at port 8000'))