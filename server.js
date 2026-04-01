const express = require("express")
const fs = require("fs")
const path = require("path")

const app = express()

app.use(express.json())
app.use(express.static("public"))

// 🔥 ROOT
app.get("/", (req,res)=>{
  res.sendFile(path.join(__dirname,"public","index.html"))
})

// 🔥 SIGNAL API
app.get("/signal", (req,res)=>{
  delete require.cache[require.resolve("./signals.json")]
  const data = require("./signals.json")
  res.json(data)
})

// 🔥 HISTORY GET
app.get("/history", (req,res)=>{
  const data = JSON.parse(fs.readFileSync("./history.json"))
  res.json(data)
})

// 🔥 SAVE SIGNAL
app.post("/save", (req,res)=>{
  let history = JSON.parse(fs.readFileSync("./history.json"))

  history.unshift(req.body)

  fs.writeFileSync("./history.json", JSON.stringify(history,null,2))

  res.json({msg:"saved"})
})

// 🔥 RESULT CHECK (✔️ ❌)
app.post("/check", (req,res)=>{

  let history = JSON.parse(fs.readFileSync("./history.json"))

  let last = history[0]
  if(!last) return res.json({msg:"no data"})

  let price = req.body.price

  if(last.signal == "BUY"){
    last.result = price > last.entry ? "WIN" : "LOSS"
  }

  if(last.signal == "SELL"){
    last.result = price < last.entry ? "WIN" : "LOSS"
  }

  fs.writeFileSync("./history.json", JSON.stringify(history,null,2))

  res.json(last)
})

app.listen(3000, ()=> console.log("SERVER RUNNING 🚀"))
