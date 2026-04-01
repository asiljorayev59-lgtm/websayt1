const express = require("express")
const fs = require("fs")
const path = require("path")

const app = express()

app.use(express.json())
app.use(express.static("public"))

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

// AUTO CHECK
setInterval(()=>{

  let history = JSON.parse(fs.readFileSync("./history.json"))
  let now = new Date()

  history.forEach(trade=>{

    if(trade.result !== "WAIT") return

    let openTime = new Date(trade.time)
    let diff = (now - openTime)/1000

    let tfTime = 3600
    if(trade.tf==="H4") tfTime=14400
    if(trade.tf==="D1") tfTime=86400

    if(diff < tfTime) return

    let priceNow = trade.entry + (Math.random()*100 - 50)

    if(trade.signal==="BUY"){
      trade.result = priceNow > trade.entry ? "WIN":"LOSS"
    }

    if(trade.signal==="SELL"){
      trade.result = priceNow < trade.entry ? "WIN":"LOSS"
    }

  })

  fs.writeFileSync("./history.json", JSON.stringify(history,null,2))

},60000)

// STATS
app.get("/stats",(req,res)=>{
  let h = JSON.parse(fs.readFileSync("./history.json"))

  function calc(tf){
    let f = h.filter(x=>x.tf===tf)
    return {
      win:f.filter(x=>x.result==="WIN").length,
      loss:f.filter(x=>x.result==="LOSS").length
    }
  }

  res.json({
    H1:calc("H1"),
    H4:calc("H4"),
    D1:calc("D1")
  })
})

app.listen(3000,()=>console.log("SERVER RUNNING 🚀"))
