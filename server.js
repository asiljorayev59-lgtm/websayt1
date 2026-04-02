const express = require("express")
const fs = require("fs")
const path = require("path")

// 🔥 ENG MUHIM — APP BU YERDA
const app = express()

app.use(express.json())
app.use(express.static("public"))

// ROOT
app.get("/", (req,res)=>{
  res.sendFile(path.join(__dirname,"public","index.html"))
})

// SIGNAL
app.get("/signal",(req,res)=>{
  delete require.cache[require.resolve("./signals.json")]
  res.json(require("./signals.json"))
})

// HISTORY
app.get("/history",(req,res)=>{
  res.json(JSON.parse(fs.readFileSync("./history.json")))
})

// SAVE
app.post("/save",(req,res)=>{

  let history = JSON.parse(fs.readFileSync("./history.json"))

  let last = history[0]

  if(last && last.signal === req.body.signal && last.tf === req.body.tf){
    return res.json({msg:"duplicate"})
  }

  history.unshift({
    tf:req.body.tf,
    signal:req.body.signal,
    entry:req.body.entry,
    time:new Date().toISOString(),
    result:"WAIT"
  })

  fs.writeFileSync("./history.json", JSON.stringify(history,null,2))

  res.json({msg:"saved"})
})

// SERVER START
app.listen(3000,()=>{
  console.log("SERVER RUNNING 🚀")
})
