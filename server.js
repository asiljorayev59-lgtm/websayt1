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


// 🔥 SAVE SIGNAL (DUPLICATE BLOK)
app.post("/save", (req,res)=>{

  let history = JSON.parse(fs.readFileSync("./history.json"))

  let last = history[0]

  // ❌ agar oxirgi signal bir xil bo‘lsa saqlamaydi
  if(last && last.signal === req.body.signal){
    return res.json({msg:"duplicate signal ignored"})
  }

  let newSignal = {
    signal: req.body.signal,
    entry: req.body.entry,
    time: new Date().toISOString(),
    result: "WAIT"
  }

  history.unshift(newSignal)

  fs.writeFileSync("./history.json", JSON.stringify(history,null,2))

  res.json({msg:"saved"})
})


// 🔥 AUTO RESULT CHECK (H4 SYSTEM)
setInterval(()=>{

  let history = JSON.parse(fs.readFileSync("./history.json"))

  if(history.length === 0) return

  let last = history[0]

  // faqat tekshirilmagan signalni tekshiradi
  if(last.result !== "WAIT") return

  let now = new Date()
  let signalTime = new Date(last.time)

  let diff = (now - signalTime) / 1000 // sekund

  // ⏱ 4 soat = 14400 sekund
  if(diff < 14400) return

  // 🔥 REAL PRICE (hozircha fake, keyin API qo‘shamiz)
  let priceNow = last.entry + (Math.random()*100 - 50)

  if(last.signal === "BUY"){
    last.result = priceNow > last.entry ? "WIN" : "LOSS"
  }

  if(last.signal === "SELL"){
    last.result = priceNow < last.entry ? "WIN" : "LOSS"
  }

  fs.writeFileSync("./history.json", JSON.stringify(history,null,2))

  console.log("RESULT UPDATED:", last)

}, 60000) // har 1 minut tekshiradi lekin 4 soat bo‘lmaguncha ishlamaydi


// 🔥 STATISTICS API
app.get("/stats", (req,res)=>{

  let h = JSON.parse(fs.readFileSync("./history.json"))

  let win = h.filter(x=>x.result==="WIN").length
  let loss = h.filter(x=>x.result==="LOSS").length

  let total = win + loss

  let accuracy = total ? ((win/total)*100).toFixed(2) : 0

  res.json({
    win,
    loss,
    accuracy
  })
})


app.listen(3000, ()=> console.log("SERVER RUNNING 🚀"))
