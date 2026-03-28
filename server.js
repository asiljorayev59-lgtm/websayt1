const express = require("express")
const fs = require("fs")

const app = express()
app.use(express.json())
app.use(express.static("public"))

// 🔥 SIGNAL API
app.get("/signal", (req,res)=>{
  delete require.cache[require.resolve("./signals.json")]
  const data = require("./signals.json")
  res.json(data)
})

// 🔥 HISTORY API
app.get("/history", (req,res)=>{
  const data = JSON.parse(fs.readFileSync("./history.json"))
  res.json(data)
})

// 🔥 SAVE HISTORY
app.post("/save", (req,res)=>{
  let history = JSON.parse(fs.readFileSync("./history.json"))

  history.unshift(req.body)

  fs.writeFileSync("./history.json", JSON.stringify(history,null,2))

  res.json({msg:"saved"})
})

app.listen(3000,()=>console.log("SERVER RUNNING"))
